from __future__ import annotations

import argparse
import ipaddress
import json
import socket
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_HTML_BYTES = 8 * 1024 * 1024
MAX_REDIRECTS = 5


def validate_url(url: str, allow_private: bool = False) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL deve usar http/https e possuir hostname.")
    if parsed.username or parsed.password:
        raise ValueError("URL com credenciais embutidas nao e aceita.")
    if allow_private:
        return
    if parsed.hostname.lower() == "localhost":
        raise ValueError("Hosts locais/privados sao bloqueados por padrao.")

    try:
        addresses = [ipaddress.ip_address(parsed.hostname)]
    except ValueError:
        try:
            addresses = [
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(
                    parsed.hostname,
                    parsed.port or (443 if parsed.scheme == "https" else 80),
                )
            ]
        except socket.gaierror as exc:
            raise ValueError(f"Hostname nao resolvido: {parsed.hostname}") from exc

    for addr in addresses:
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_multicast
            or addr.is_reserved
            or addr.is_unspecified
        ):
            raise ValueError(f"Endereco local/privado bloqueado: {addr}")


def make_session() -> requests.Session:
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        status=2,
        backoff_factor=0.4,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
    )
    current = requests.Session()
    current.mount("http://", HTTPAdapter(max_retries=retry))
    current.mount("https://", HTTPAdapter(max_retries=retry))
    return current


def fetch_html(url: str, allow_private: bool = False) -> tuple[requests.Response, bytes]:
    current_url = url
    client = make_session()
    for _ in range(MAX_REDIRECTS + 1):
        validate_url(current_url, allow_private=allow_private)
        response = client.get(
            current_url,
            timeout=(8, 30),
            headers={"User-Agent": "Mozilla/5.0 TesseractCreativeLab/2.0"},
            allow_redirects=False,
            stream=True,
        )
        if response.is_redirect or response.is_permanent_redirect:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise RuntimeError("Redirect sem header Location.")
            current_url = urljoin(current_url, location)
            continue

        response.raise_for_status()
        chunks = []
        total = 0
        for chunk in response.iter_content(64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_HTML_BYTES:
                response.close()
                raise RuntimeError(
                    f"HTML excede limite de {MAX_HTML_BYTES // 1024 // 1024} MB."
                )
            chunks.append(chunk)
        return response, b"".join(chunks)
    raise RuntimeError(f"Excesso de redirects (>{MAX_REDIRECTS}).")


def jsonld_items(soup: BeautifulSoup) -> list[object]:
    items: list[object] = []
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or tag.get_text())
            items.extend(data if isinstance(data, list) else [data])
        except (json.JSONDecodeError, TypeError):
            continue
    return items


def find_product(items: list[object]) -> dict[str, object]:
    queue = list(items)
    while queue:
        obj = queue.pop(0)
        if isinstance(obj, dict):
            typ = obj.get("@type")
            if typ == "Product" or (isinstance(typ, list) and "Product" in typ):
                return obj
            graph = obj.get("@graph")
            if isinstance(graph, list):
                queue.extend(graph)
        elif isinstance(obj, list):
            queue.extend(obj)
    return {}


def offer_dicts(value: object) -> list[dict[str, object]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return [value] if isinstance(value, dict) else []


def offer_value(offer: dict[str, object], key: str) -> object | None:
    value = offer.get(key)
    if value not in (None, ""):
        return value
    specification = offer.get("priceSpecification")
    if isinstance(specification, dict) and key == "price":
        value = specification.get("price")
        if value not in (None, ""):
            return value
    return None


def unique(values: list[object]) -> list[object]:
    result = []
    seen = set()
    for value in values:
        marker = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if marker not in seen:
            seen.add(marker)
            result.append(value)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Captura evidencia comercial basica de uma pagina de produto."
    )
    ap.add_argument("url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-private-network", action="store_true")
    args = ap.parse_args()

    try:
        response, body = fetch_html(
            args.url, allow_private=args.allow_private_network
        )
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        ap.error(str(exc))

    encoding = response.encoding or "utf-8"
    html = body.decode(encoding, errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    product = find_product(jsonld_items(soup))
    offers = offer_dicts(product.get("offers"))
    if (
        len(offers) == 1
        and str(offers[0].get("@type", "")).lower() == "aggregateoffer"
    ):
        nested = offer_dicts(offers[0].get("offers"))
        if nested:
            offers = nested

    def og(key: str) -> str:
        tag = soup.find("meta", property=key)
        return tag.get("content", "") if tag else ""

    brand = product.get("brand") or ""
    if isinstance(brand, dict):
        brand = brand.get("name", "")
    if not isinstance(brand, str):
        brand = str(brand)

    raw_images = product.get("image") or []
    images = raw_images if isinstance(raw_images, list) else [raw_images]
    gallery = [
        str(item)
        for item in images
        if isinstance(item, (str, int, float)) and str(item)
    ]

    prices = unique(
        [
            value
            for offer in offers
            if (value := offer_value(offer, "price")) is not None
        ]
    )
    currencies = unique(
        [
            offer.get("priceCurrency")
            for offer in offers
            if offer.get("priceCurrency")
        ]
    )
    availability = unique(
        [
            offer.get("availability")
            for offer in offers
            if offer.get("availability")
        ]
    )

    notes = []
    if len(prices) > 1:
        notes.append(
            "Multiplos precos encontrados; commercial.price foi omitido para evitar escolher variante silenciosamente."
        )
    if not product:
        notes.append(
            "Product JSON-LD nao encontrado; titulo/imagem podem vir de Open Graph."
        )
    content_type = response.headers.get("Content-Type", "")
    if content_type and "html" not in content_type.lower():
        notes.append(f"Content-Type inesperado: {content_type}")

    result = {
        "schema_version": 1,
        "requested_url": args.url,
        "source_url": response.url,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "http": {"status": response.status_code, "content_type": content_type},
        "product": {
            "name": str(product.get("name") or og("og:title") or ""),
            "sku": str(product.get("sku") or ""),
            "brand": brand,
            "availability": str(availability[0])
            if len(availability) == 1
            else "",
        },
        "commercial": {
            "price": prices[0] if len(prices) == 1 else None,
            "price_currency": str(currencies[0])
            if len(currencies) == 1
            else None,
            "old_price": None,
            "discount_percent": None,
            "pix_price": None,
            "installments": None,
            "installment_value": None,
            "coupon": None,
            "shipping": None,
        },
        "media": {
            "main_image": gallery[0] if gallery else og("og:image"),
            "gallery": gallery,
        },
        "evidence": {
            "jsonld_product_found": bool(product),
            "offer_count": len(offers),
            "price_candidates": prices,
            "currency_candidates": currencies,
            "availability_candidates": availability,
        },
        "notes": " ".join(notes)
        or "Dados extraidos automaticamente; confirme condicoes criticas antes de uso criativo.",
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "
",
        encoding="utf-8",
    )
    print(out)


if __name__ == "__main__":
    main()

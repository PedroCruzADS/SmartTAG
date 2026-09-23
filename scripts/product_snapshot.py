from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

def jsonld_items(soup):
    items=[]
    for tag in soup.find_all('script', attrs={'type':'application/ld+json'}):
        try:
            data=json.loads(tag.string or tag.get_text())
            items.extend(data if isinstance(data,list) else [data])
        except Exception:
            pass
    return items

def find_product(items):
    queue=list(items)
    while queue:
        obj=queue.pop(0)
        if isinstance(obj,dict):
            typ=obj.get('@type')
            if typ=='Product' or (isinstance(typ,list) and 'Product' in typ):
                return obj
            graph=obj.get('@graph')
            if isinstance(graph,list): queue.extend(graph)
        elif isinstance(obj,list): queue.extend(obj)
    return {}

def main():
    ap=argparse.ArgumentParser(description='Capture basic product truth from a product page.')
    ap.add_argument('url')
    ap.add_argument('--out', required=True)
    args=ap.parse_args()

    r=requests.get(args.url, timeout=30, headers={'User-Agent':'Mozilla/5.0 TesseractCreativeLab/1.0'})
    r.raise_for_status()
    soup=BeautifulSoup(r.text,'html.parser')
    p=find_product(jsonld_items(soup))
    offers=p.get('offers') or {}
    if isinstance(offers,list): offers=offers[0] if offers else {}

    def og(key):
        tag=soup.find('meta', property=key)
        return tag.get('content','') if tag else ''

    brand=p.get('brand') or ''
    if isinstance(brand,dict): brand=brand.get('name','')
    images=p.get('image') or []
    gallery=images if isinstance(images,list) else ([images] if images else [])

    result={
      'source_url': args.url,
      'captured_at': datetime.now(timezone.utc).isoformat(),
      'product': {
        'name': p.get('name') or og('og:title'),
        'sku': p.get('sku') or '',
        'brand': brand,
        'availability': offers.get('availability','') if isinstance(offers,dict) else ''
      },
      'commercial': {
        'price': offers.get('price') if isinstance(offers,dict) else None,
        'price_currency': offers.get('priceCurrency') if isinstance(offers,dict) else None,
        'old_price': None, 'discount_percent': None, 'pix_price': None,
        'installments': None, 'installment_value': None, 'coupon': None, 'shipping': None
      },
      'media': {'main_image': gallery[0] if gallery else og('og:image'), 'gallery': gallery},
      'notes': 'Dados extraidos automaticamente. Condicoes ausentes precisam ser confirmadas antes de uso criativo.'
    }

    out=Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()

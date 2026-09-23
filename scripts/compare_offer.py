import argparse, json
from pathlib import Path

FIELDS = [
 ('product.name','product','name'),
 ('product.sku','product','sku'),
 ('commercial.price','commercial','price'),
 ('commercial.old_price','commercial','old_price'),
 ('commercial.discount_percent','commercial','discount_percent'),
 ('commercial.pix_price','commercial','pix_price'),
 ('commercial.installments','commercial','installments'),
 ('commercial.installment_value','commercial','installment_value'),
 ('commercial.coupon','commercial','coupon'),
 ('commercial.shipping','commercial','shipping'),
 ('product.availability','product','availability'),
]

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('old')
    ap.add_argument('new')
    args=ap.parse_args()
    a,b=load(args.old),load(args.new)
    changed=[]
    for label,section,key in FIELDS:
        av=(a.get(section) or {}).get(key)
        bv=(b.get(section) or {}).get(key)
        if av != bv:
            changed.append((label,av,bv))
    if not changed:
        print('Nenhuma mudanca comercial monitorada.')
        return
    print('Mudancas encontradas:')
    for label,av,bv in changed:
        print(f'- {label}: {av!r} -> {bv!r}')

if __name__=='__main__':
    main()

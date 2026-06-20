# -*- coding: utf-8 -*-
import sys, io, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import server

def show(label, obj):
    print(f'--- {label} ---')
    print(json.dumps(obj, ensure_ascii=False, indent=2))
    print()

show('lookup_isbn(978-1-4920-5635-5)', server.lookup_isbn('978-1-4920-5635-5'))
time.sleep(1.0)
show('lookup_isbn(9780134685991)', server.lookup_isbn('9780134685991'))
time.sleep(1.0)
r = server.search_books('design patterns', 3)
print('--- search_books(design patterns, 3) --- provider=', r.get('provider'), 'count=', r['count'])
for b in r['results']:
    print('  -', b.get('title'), '/', b.get('authors'), '/', b.get('isbn_13'))

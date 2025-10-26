#!/usr/bin/env python3
import sys,os,re,difflib
root='.'
home=os.path.join(root,'home.html')
if not os.path.exists(home):
    print('home.html not found',file=sys.stderr); sys.exit(1)
with open(home,'r',encoding='utf-8') as f:
    h=f.read()
#makes header-></nav> block
m=re.search(r'<header[\s\S]*?</nav>', h, flags=re.I)
if not m:
    print('header/nav block not found in home.html',file=sys.stderr); sys.exit(1)
canon=m.group(0).strip().splitlines()
# find html files
files=[]
for dirpath,dirs,filenames in os.walk('.'):
    for fn in filenames:
        if fn.lower().endswith('.html'):
            files.append(os.path.join(dirpath,fn))
files=sorted(files)
print('Comparing header/nav block from home.html against',len(files),'HTML files')
failed=0
for path in files:
    with open(path,'r',encoding='utf-8') as f:
        txt=f.read()
    mm=re.search(r'<header[\s\S]*?</nav>', txt, flags=re.I)
    if not mm:
        print('\n[NO BLOCK] ',path)
        failed+=1
        continue
    block=mm.group(0).strip().splitlines()
    if block==canon:
        print('\n[OK] ',path)
    else:
        print('\n[MISMATCH] ',path)
        diff=list(difflib.unified_diff(canon, block, fromfile='home.html(header->nav)', tofile=path+'(header->nav)', lineterm=''))
        for line in diff:
            print(line)
        failed+=1
print('\nDone. Mismatched files:', failed)
if failed>0:
    sys.exit(2)
else:
    sys.exit(0)

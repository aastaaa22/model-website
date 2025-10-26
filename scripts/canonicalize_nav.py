#!/usr/bin/env python3
import re,sys,os
root='.'
home=os.path.join(root,'home.html')
if not os.path.exists(home):
    print('home.html not found',file=sys.stderr); sys.exit(1)
with open(home,'r',encoding='utf-8') as f:
    home_txt = f.read()
m = re.search(r'(<header[\s\S]*?</nav>)', home_txt, flags=re.I)
if not m:
    print('Could not find header/nav in home.html', file=sys.stderr); sys.exit(1)
canon = m.group(1)
# target files: all html except home.html and files that already match
targets=[]
for dirpath,dirs,files in os.walk('.'):
    for fn in files:
        if fn.lower().endswith('.html'):
            p=os.path.join(dirpath,fn)
            if os.path.normpath(p)==os.path.normpath(home):
                continue
            targets.append(p)
changed=[]
for p in sorted(targets):
    txt=open(p,'r',encoding='utf-8').read()
    mm = re.search(r'(<header[\s\S]*?</nav>)', txt, flags=re.I)
    if not mm:
        print('SKIP (no header/nav):', p)
        continue
    block = mm.group(1)
    if block.strip()==canon.strip():
        print('OK:',p)
        continue
    new = txt.replace(block, canon)
    with open(p,'w',encoding='utf-8') as f:
        f.write(new)
    changed.append(p)
    print('Updated:',p)
print('Done. Updated', len(changed),'files.')

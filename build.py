#!/usr/bin/env python3
"""Make artifact review copies: inline styles.css, embed images as data URIs, strip the document shell."""
import re,base64,sys,os
OUT=sys.argv[1] if len(sys.argv)>1 else 'build'
os.makedirs(OUT,exist_ok=True)
css=open('styles.css').read()
def datauri(path):
    if not os.path.exists(path): return None
    return 'data:image/jpeg;base64,'+base64.b64encode(open(path,'rb').read()).decode()
for f in ['index.html','services.html','audit.html','about.html','contact.html']:
    s=open(f).read()
    head=re.search(r'<head>(.*?)</head>',s,re.S).group(1)
    body=re.search(r'<body>(.*?)</body>',s,re.S).group(1)
    head=re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>|<link rel="preload"[^>]*>','',head)
    head=head.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'</style>')
    for m in set(re.findall(r'assets/[\w\-]+\.jpg',head+body)):
        small='/private/tmp/claude-501/-Users-beckysciullo-projects-say-yes/a68a3aa4-6c2f-4ff5-9a5a-05c3c9a4c16f/scratchpad/photos/hero-art.jpg' if 'hero-paper-planes' in m else m
        d=datauri(small) or datauri(m)
        if d: head=head.replace(m,d); body=body.replace(m,d)
    open(os.path.join(OUT,f),'w').write(head+body)
    print('built',f)

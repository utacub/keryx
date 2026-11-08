# Applies the UTAC Keryx 0.6.11 change to the built UTAC_Keryx_v0.6.10_local.html (Marc, 2026-11-08):
# the "Editar carpeta" button leaves the folder path bar; a folder is edited from its parent folder in edit mode.
# Usage: python3 patch0611.py UTAC_Keryx_v0.6.10_local.html UTAC_Keryx_v0.6.11_local.html
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.10(?![:\d])','0.6.11',s)
rep(" const edit=button(tr('Editar carpeta','Editar carpeta'),()=>editFolder(phraseFolder),'flat','edit');bar.append(el('span',{class:'spacer'}),edit);\n","\n")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

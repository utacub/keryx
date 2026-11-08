# Applies the UTAC Keryx 0.6.13 change to the built UTAC_Keryx_v0.6.12_local.html (Marc, 2026-11-08):
# the "Més eines" main button shows a tools (wrench) icon instead of the edit pencil.
# Usage: python3 patch0613.py UTAC_Keryx_v0.6.12_local.html UTAC_Keryx_v0.6.13_local.html
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.12(?![:\d])','0.6.13',s)
rep("PATHS.folder='M3 6h6l2 2h10v11H3z';","PATHS.folder='M3 6h6l2 2h10v11H3z';PATHS.tools='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z';")
rep("editingDialog,'more-tools','edit')","editingDialog,'more-tools','tools')")
rep("['more','more-tools','edit']","['more','more-tools','tools']")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

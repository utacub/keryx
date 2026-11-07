# Applies the UTAC Keryx 0.6.5 change to the built UTAC_Keryx_v0.6.4_local.html:
# the "Comencem amb Keryx" first-use window no longer opens; Keryx starts on the main screen.
# Language, access method and voice stay in the header and in Ajustos.
# Usage: python3 patch065.py UTAC_Keryx_v0.6.4_local.html UTAC_Keryx_v0.6.5_local.html
# GPL-3.0-or-later.
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:60],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.4(?!:)','0.6.5',s)
rep("scheduleFitMessage();if(firstUse)welcome();\n})();",
    "scheduleFitMessage();/* 0.6.5: no first-use window; the first visit is marked as set up. */if(firstUse){firstUse=false;persist();}\n})();")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

# Applies the UTAC Keryx 0.7.3 change to index.html of 0.7.2 (Marc, 2026-11-08):
# on phones (touch screen whose short side is 600 px or less) the message buttons default to below the message;
# other devices keep them on the right. Profiles on a phone that still have the old default (right) move below once;
# settings.actionsDefault=3 marks it, so a later choice in Settings is kept.
# Usage: python3 patch073.py index.html index.html.new
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.7\.2(?![:\d])','0.7.3',s)
rep("  const defaults = () => ({",
    "  /* 0.7.3: a phone is a touch screen whose short side is 600 CSS px or less. */\n  const phoneDevice=()=>{try{return matchMedia('(pointer:coarse)').matches&&Math.min(screen.width,screen.height)<=600;}catch{return false;}};\n  const defaults = () => ({")
rep("actionsPosition:'right',actionsDefault:2,","actionsPosition:phoneDevice()?'bottom':'right',actionsDefault:3,")
rep("    if(raw.actionsDefault!==2&&s.actionsPosition==='bottom')s.actionsPosition='right';s.actionsDefault=2;",
    "    if(raw.actionsDefault!==3){if(phoneDevice()){if(s.actionsPosition==='right')s.actionsPosition='bottom';}else if(raw.actionsDefault!==2&&s.actionsPosition==='bottom')s.actionsPosition='right';}s.actionsDefault=3;")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

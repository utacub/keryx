# Applies the UTAC Keryx 0.6.5 change to the built UTAC_Keryx_v0.6.4_local.html:
# the "Comencem amb Keryx" first-use window no longer opens; Keryx starts on the main screen.
# Language, access method and voice stay in the header and in Ajustos.
# The version number also shows in small type next to the logo.
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
# --- header buttons (Marc, 2026-11-07): Install shows only its icon, at the size of the other icon buttons;
# Info looks like a button, as Settings does.
rep('<button id="info-button" class="icon-only flat" aria-haspopup="dialog"></button><button id="install-button" class="install-button" type="button" hidden></button>',
    '<button id="info-button" class="icon-only soft" aria-haspopup="dialog"></button><button id="install-button" class="icon-only install-button" type="button" hidden></button>')
a=s.index('.install-button{display:inline-flex'); b=s.index('/* Small phones: a narrower logo')
s=s[:a]+""".install-button{background:var(--primary);border-color:var(--primary);color:var(--primaryText)}
.install-button span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
"""+s[b:]

# --- version number in small type next to the logo (Marc, 2026-11-07)
i=s.index('<img class="brand brand-positive"')
s=s[:i]+'<span class="brand-wrap">'+s[i:]
i=s.index('class="brand brand-negative"'); j=s.index('alt="UTAC Keryx">',i)+len('alt="UTAC Keryx">')
s=s[:j]+'<span class="brand-version" title="Versió 0.6.5">0.6.5</span></span>'+s[j:]
CSS="""
/* 0.6.5: version next to the logo. The logo box now fits the drawing, and the number sits at its bottom right. */
.brand-wrap{display:inline-flex;align-items:flex-end;gap:5px;flex:none}
.header-inner img.brand{width:auto!important;aspect-ratio:2752/742}
.brand-version{margin-bottom:.12em;font-size:11px;line-height:1;font-weight:600;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
@media(max-width:400px){.brand-wrap{gap:3px}.brand-version{font-size:10px}.header-inner{gap:2px;padding-inline:8px}.header-control{gap:2px}.header-inner .brand{height:26px!important}}\n@media(max-width:350px){.header-inner .brand{height:22px!important}.brand-version{font-size:9px}.header-control{gap:0}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

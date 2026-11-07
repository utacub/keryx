# Applies the UTAC Keryx 0.6.7 change to the built UTAC_Keryx_v0.6.6_local.html:
# Documents tab, narrower rows so that at least four documents fit on one page (Marc, 2026-11-07).
# Usage: python3 patch067.py UTAC_Keryx_v0.6.6_local.html UTAC_Keryx_v0.6.7_local.html
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:70],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.6(?!:)','0.6.7',s)
# At least 4 documents per page (up to 10), about 44 px per row instead of 70.
rep("const list=docsAll();const size=Math.max(1,Math.min(5,Math.floor((n.clientHeight||200)/70)));",
    "const list=docsAll();const size=Math.max(4,Math.min(10,Math.floor(((n.clientHeight||200)+4)/44)));")
CSS="""
/* 0.6.7: narrower document rows, at least four per page */
#docs-grid{gap:4px}
#docs-grid .history-row{border-radius:8px}
#docs-grid .history-row .history-text{font-size:14px;padding:2px 10px;min-height:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block;line-height:1.2}
#docs-grid .history-row button{min-height:0;padding-block:0}
@media(max-width:600px),(max-height:500px){[data-scan-group="documents-actions"]>p{display:none}[data-scan-group="documents-actions"]{justify-content:flex-end}[data-scan-group="documents-actions"] button{white-space:nowrap}
#docs-grid .history-row small{display:none}#docs-grid .history-row button:last-child>span:not(.icon){position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}#docs-grid .history-row button:last-child{padding-inline:12px}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

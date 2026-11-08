# Applies the UTAC Keryx 0.7.2 fixes to index.html of 0.7.1 (final audit before release, 2026-11-08):
# - Word prediction: an F key chosen for a proposal no longer reaches the browser when that proposal is not shown
#   (F5 reloaded the page and the message was lost; F1 opened the browser help, F3 the find bar).
# - Header: the logo scales with the window width, so the Install button is no longer cut off at 412 px
#   (common Android phones), 352-356 px and 300-312 px.
# - Accessible names of the panel buttons and the language button contain their visible text (WCAG 2.5.3).
# - Information: «Claude (0.6.1 i posteriors)» is translated in Basque, Galician, English and French.
# - Version 0.7.2, 8 November 2026, in every language.
# Usage: python3 patch072.py index.html index.html.new
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)

# Version and date (the comment about switch scanning keeps its real version, 0.6.8)
rep("Switch scanning was removed in 0.7.1.","Switch scanning was removed in 0.6.8.")
s=re.sub(r'(?<!/\* )0\.7\.1(?![:\d])','0.7.2',s)
for a,b in [("Versió 0.7.2 · 7 de novembre de 2026","Versió 0.7.2 · 8 de novembre de 2026"),
            ("Versión 0.7.2 · 7 de noviembre de 2026","Versión 0.7.2 · 8 de noviembre de 2026"),
            ("0.7.2 bertsioa · 2026ko azaroaren 7a","0.7.2 bertsioa · 2026ko azaroaren 8a"),
            ("Versión 0.7.2 · 7 de novembro de 2026","Versión 0.7.2 · 8 de novembro de 2026"),
            ("Version 0.7.2 · 7 November 2026","Version 0.7.2 · 8 November 2026"),
            ("Version 0.7.2 · 7 novembre 2026","Version 0.7.2 · 8 novembre 2026")]:
    assert a in s,a; s=s.replace(a,b)

# Prediction keys: an F key assigned to a proposal is always kept from the browser while proposals are in use
rep("const P=prefs().predict;if(!P.enabled||!predictLast.length||$('suggestions').hidden||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;\n let i=-1;if(P.keys[0]&&e.key===P.keys[0])i=0;else{const k=P.keys.indexOf(e.key,1);if(k>0)i=k-1;}\n if(i<0||i>=predictLast.length)return;",
    "const P=prefs().predict;if(!P.enabled||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;\n /* 0.7.2: an F key chosen for a proposal never reaches the browser (F5 would reload and lose the message, F1 opens help, F3 find). */\n const fkey=/^F\\d+$/.test(e.key)&&P.keys.includes(e.key)&&predictActive();\n if(!predictLast.length||$('suggestions').hidden){if(fkey)e.preventDefault();return;}\n let i=-1;if(P.keys[0]&&e.key===P.keys[0])i=0;else{const k=P.keys.indexOf(e.key,1);if(k>0)i=k-1;}\n if(i<0||i>=predictLast.length){if(fkey)e.preventDefault();return;}")

# Accessible names include the visible text
rep("trigger.setAttribute('aria-label',tr('Idioma','Idioma')+': '+languageName(prefs().lang));",
    "trigger.setAttribute('aria-label',tr('Idioma','Idioma')+': '+languageName(prefs().lang)+' ('+prefs().lang.toUpperCase()+')');")
rep("toggle.setAttribute('aria-label',tr('Minimitzar el panell inferior','Minimizar el panel inferior'));toggle.title=toggle.getAttribute('aria-label');",
    "toggle.setAttribute('aria-label',tr('Amagar panell','Ocultar panel'));toggle.title=tr('Minimitzar el panell inferior','Minimizar el panel inferior');")
rep("restore.setAttribute('aria-label',tr('Desplegar el panell inferior','Desplegar el panel inferior'));restore.title=restore.getAttribute('aria-label');",
    "restore.setAttribute('aria-label',tr('Mostrar panell','Mostrar panel'));restore.title=tr('Desplegar el panell inferior','Desplegar el panel inferior');")

CSS="""
/* 0.7.2: the logo scales with the window width, so the header buttons always fit (412 px phones cut off Install) */
@media(max-width:600px){.header-inner .brand{height:min(35px,calc((100vw - 300px)/3.71))!important}.header-control{flex:none}}
@media(max-width:400px){.header-inner .brand{height:min(24px,calc((100vw - 278px)/3.71))!important}}
@media(max-width:350px){.header-inner .brand{height:min(21px,calc((100vw - 236px)/3.71))!important}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]

T={" i ":[" eta "," e "," and "," et "],"posteriors":["ondorengoak","posteriores","later","suivantes"]}
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(['eu','gl','en','fr']):
    key='"'+lang+'":{'; k=s.index(key,i)+len(key)
    s=s[:k]+''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())+s[k:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

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
# --- Catalan text review (Marc, 2026-11-07). Each Catalan string is also the key of the eu/gl/en/fr dictionaries,
# so it is replaced everywhere it appears.
def repall(a,b):
    global s
    assert s.count(a)>=1,a[:60]; s=s.replace(a,b)
CA={
 # Shift key: the Catalan label is «Maj», as «Mayús» is the Spanish one.
 "tr('Majús','Mayús')":"tr('Maj','Mayús')",
 '"Majús":"':'"Maj":"',
 "Majús + Tab torna enrere":"Maj + Tab torna enrere",
 "Pots seleccionar text amb Majús i les fletxes":"Pots seleccionar text amb Maj i les fletxes",
 # The app can now be installed.
 "Encara pendents: instal·lació PWA, serveis":"Encara pendents: serveis",
 # Missing object.
 "No queda lloc lliure. Fes més petit o amaga un altre botó.":"No queda lloc lliure. Fes més petit un altre botó o amaga’l.",
 # Possessive with a thing; a pronoun reads better.
 "Arrossega un botó per moure’l, o la seva cantonada per canviar-ne la mida.":"Arrossega un botó per moure’l, o arrossega’n la cantonada per canviar-ne la mida.",
 "Llegeix la frase en fer punt, interrogació, exclamació o prémer Intro.":"Llegeix la frase en escriure un punt, un interrogant o una exclamació, o en prémer Intro.",
 "Recuperar els esborranys quan torni a obrir":"Recuperar els esborranys quan torni a obrir Keryx",
 "Inclou l’editor, veu del navegador i veus descarregables, presentació de text, 90 missatges":"Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges",
 "No tots els sistemes ofereixen tots sis idiomes.":"No tots els sistemes ofereixen els sis idiomes.",
 "Cal una còpia Keryx de format 1":"Cal una còpia de Keryx de format 1",
 "Identitat gràfica aprovada: logotip Keryx i original d’UTAC aportat per Marc Coronas.":"Identitat gràfica aprovada: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas.",
 "llicència GPL-3.0-o-posterior per al codi":"llicència GPL-3.0 o posterior per al codi",
}
for a,b in CA.items(): repall(a,b)
# Same correction in the other languages of the "still pending" list.
for a,b in [("instalación PWA, servicios","servicios"),("PWA instalazioa, ahots","ahots"),("instalación PWA, servizos","servizos"),("PWA installation, additional","additional"),("installation PWA, services","services")]: repall(a,b)

# --- «Per què es diu Keryx» in the Information window (Marc, 2026-11-07): short, from the planning document, section 1.1.
import os, json as _j
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from name_section import H, P, REFS
J=lambda x:_j.dumps(x,ensure_ascii=False)
sec="el('h3',{},tr(%s,%s)),"%(J(H['ca']),J(H['es']))+"".join("el('p',{},tr(%s,%s)),"%(J(p['ca']),J(p['es'])) for p in P)
rep("el('h3',{},tr('Projecte i crèdits','Proyecto y créditos'))", sec+"el('h3',{},tr('Projecte i crèdits','Proyecto y créditos'))")
rep("const refs=[['UTAC. (2026). LECAA Docs", "const refs=["+"".join("[%s,%s],"%(J(t),J(u)) for t,u in REFS)+"['UTAC. (2026). LECAA Docs")
for lang in ['eu','gl','en','fr']:
    ins=J(H['ca'])+':'+J(H[lang])+','+''.join(J(p['ca'])+':'+J(p[lang])+',' for p in P)
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')

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
s=s[:j]+'<span class="brand-version" title="Versió 0.6.5"><span>v.\u00a00.6.5</span></span></span>'+s[j:]
CSS="""
/* 0.6.5: version next to the logo. The logo box now fits the drawing, and the number sits at its bottom right. */
.brand-wrap{display:inline-flex;align-items:stretch;gap:5px;flex:none}
.header-inner img.brand{width:auto!important;aspect-ratio:2752/742}
/* The number sits on the baseline of the word Keryx, which is at 65.2 % of the logo height (measured on the brand SVG). */
.brand-version{padding-left:1ch;display:grid;grid-template-rows:65.2fr 34.8fr;align-items:end;font-size:10px;line-height:1;font-weight:600;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
.brand-version::after{content:""}
.brand-version>span{transform:translateY(.24em)}
@media(max-width:400px){.brand-wrap{gap:3px}.brand-version{font-size:9px}.header-inner{gap:2px;padding-inline:6px}.header-control{gap:2px}.header-inner .brand{height:24px!important}}
@media(max-width:350px){.header-inner .brand{height:21px!important}.brand-version{font-size:8px}.header-control{gap:0}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

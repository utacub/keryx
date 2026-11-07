# Applies the UTAC Keryx 0.6.2 changes to the built UTAC_Keryx_v0.6.1_local.html.
# Usage: python3 patch062.py UTAC_Keryx_v0.6.1_local.html UTAC_Keryx_v0.6.2_local.html
# GPL-3.0-or-later.
import sys, re, json, os
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:60],n); s=s.replace(a,b)
# Version strings change; the "/* 0.6.1 ..." comments that date earlier changes stay as they are.
s=re.sub(r'(?<!/\* )0\.6\.1(?!b)','0.6.2',s)

# --- translations for new strings
T={'eu':{"Posició dels botons principals":"Botoi nagusien kokapena","Sota el missatge":"Mezuaren azpian","A l’esquerra del missatge":"Mezuaren ezkerrean","A la dreta del missatge":"Mezuaren eskuinean","Parlar, Aturar, Mostrar i Nou missatge. Parlar sempre és el botó més gran.":"Hitz egin, Gelditu, Erakutsi eta Mezu berria. Hitz egin botoia beti da handiena."},
   'gl':{"Posició dels botons principals":"Posición dos botóns principais","Sota el missatge":"Debaixo da mensaxe","A l’esquerra del missatge":"Á esquerda da mensaxe","A la dreta del missatge":"Á dereita da mensaxe","Parlar, Aturar, Mostrar i Nou missatge. Parlar sempre és el botó més gran.":"Falar, Deter, Mostrar e Nova mensaxe. Falar sempre é o botón máis grande."},
   'en':{"Posició dels botons principals":"Main buttons position","Sota el missatge":"Below the message","A l’esquerra del missatge":"Left of the message","A la dreta del missatge":"Right of the message","Parlar, Aturar, Mostrar i Nou missatge. Parlar sempre és el botó més gran.":"Speak, Stop, Show and New message. Speak is always the largest button."},
   'fr':{"Posició dels botons principals":"Position des boutons principaux","Sota el missatge":"Sous le message","A l’esquerra del missatge":"À gauche du message","A la dreta del missatge":"À droite du message","Parlar, Aturar, Mostrar i Nou missatge. Parlar sempre és el botó més gran.":"Parler, Arrêter, Afficher et Nouveau message. Parler est toujours le plus grand bouton."}}
for lang,d in T.items():
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False)+',' for k,v in d.items())
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')

# --- new preference: actionsPosition = bottom | left | right
rep("theme:'light',fontSize:30,controlSize:1,","theme:'light',fontSize:30,controlSize:1,actionsPosition:'bottom',")
rep("layout:['qwerty','abc'],","layout:['qwerty','abc'],actionsPosition:['bottom','left','right'],")
rep("rangeField(tr('Mida dels controls','Tamaño de los controles'),'controlSize',1,1.4,.1,x=>Math.round(x*100)+'%'),",
    "rangeField(tr('Mida dels controls','Tamaño de los controles'),'controlSize',1,1.4,.1,x=>Math.round(x*100)+'%'),"
    "field(tr('Posició dels botons principals','Posición de los botones principales'),selectControl([['bottom',tr('Sota el missatge','Debajo del mensaje')],['left',tr('A l’esquerra del missatge','A la izquierda del mensaje')],['right',tr('A la dreta del missatge','A la derecha del mensaje')]],p.actionsPosition||'bottom',v=>{set('actionsPosition',v);applyAppearance();}),tr('Parlar, Aturar, Mostrar i Nou missatge. Parlar sempre és el botó més gran.','Hablar, Detener, Mostrar y Nuevo mensaje. Hablar siempre es el botón más grande.')),")

# --- apply: actions position, and the focus ring takes the theme's primary colour
rep("document.documentElement.style.setProperty('--message-size',prefs().fontSize+'px');",
    "document.documentElement.style.setProperty('--focus',theme.colors.primary);$('composer').dataset.actions=prefs().actionsPosition||'bottom';if(typeof scheduleFitMessage==='function')scheduleFitMessage();"
    "document.documentElement.style.setProperty('--message-size',prefs().fontSize+'px');")
rep("--accent:#98db27;--focus:#155ab5;","--accent:#98db27;--focus:#0a5509;")

# --- the Information window and the licences it opens scroll instead of being split into pages (Marc, 2026-11-07)
rep("[button(tr('Tornar a l’ajuda','Volver a la ayuda'),helpDialog,'primary')])","[button(tr('Tornar a l’ajuda','Volver a la ayuda'),helpDialog,'primary')],'scroll-dialog')")
rep("button(tr('Tancar','Cerrar'),closeDialog,'primary')])","button(tr('Tancar','Cerrar'),closeDialog,'primary')],'scroll-dialog')")
rep("[button(tr('Tornar','Volver'),licencesDialog,'primary')])","[button(tr('Tornar','Volver'),licencesDialog,'primary')],'scroll-dialog')")
rep("body,[button(tr('Tornar','Volver'),helpDialog,'primary')])","body,[button(tr('Tornar','Volver'),helpDialog,'primary')],'scroll-dialog')")
rep("()=>shortcutsDialog(()=>keyboardManual(back)),'','settings'),button(tr('Tornar','Volver'),back,'primary')])","()=>shortcutsDialog(()=>keyboardManual(back)),'','settings'),button(tr('Tornar','Volver'),back,'primary')],'scroll-dialog')")

# --- CSS
css=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'css_add.css'),encoding='utf-8').read()
# Low landscape windows with the panel open: Speak takes the whole first row instead of a quarter.
rep(" .main:not([data-view=closed]) .composer-actions{grid-template-columns:1fr 1fr;gap:5px}",
    " .main:not([data-view=closed]) .composer-actions{grid-template-columns:repeat(3,minmax(0,1fr));gap:5px}.main:not([data-view=closed]) .composer-actions .speak{grid-column:1/-1}")
i=s.rindex('</style>'); s=s[:i]+css+s[i:]

open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

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
T={'eu':{"Posició dels botons principals":"Botoi nagusien kokapena","Sota el missatge":"Mezuaren azpian","A l’esquerra del missatge":"Mezuaren ezkerrean","A la dreta del missatge":"Mezuaren eskuinean","Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.":"Hitz egin, Gelditu, Erakutsi, Hitza ezabatu, Dena ezabatu eta Mezu berria. Hitz egin botoia beti da handiena.","Esborrar-ho tot":"Dena ezabatu","Missatge esborrat. Desfer el recupera.":"Mezua ezabatu da. Desegin-ek berreskuratzen du."},
   'gl':{"Posició dels botons principals":"Posición dos botóns principais","Sota el missatge":"Debaixo da mensaxe","A l’esquerra del missatge":"Á esquerda da mensaxe","A la dreta del missatge":"Á dereita da mensaxe","Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.":"Falar, Deter, Mostrar, Borrar palabra, Borralo todo e Nova mensaxe. Falar sempre é o botón máis grande.","Esborrar-ho tot":"Borralo todo","Missatge esborrat. Desfer el recupera.":"Mensaxe borrada. Desfacer recupéraa."},
   'en':{"Posició dels botons principals":"Main buttons position","Sota el missatge":"Below the message","A l’esquerra del missatge":"Left of the message","A la dreta del missatge":"Right of the message","Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.":"Speak, Stop, Show, Delete word, Clear all and New message. Speak is always the largest button.","Esborrar-ho tot":"Clear all","Missatge esborrat. Desfer el recupera.":"Message cleared. Undo brings it back."},
   'fr':{"Posició dels botons principals":"Position des boutons principaux","Sota el missatge":"Sous le message","A l’esquerra del missatge":"À gauche du message","A la dreta del missatge":"À droite du message","Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.":"Parler, Arrêter, Afficher, Effacer le mot, Tout effacer et Nouveau message. Parler est toujours le plus grand bouton.","Esborrar-ho tot":"Tout effacer","Missatge esborrat. Desfer el recupera.":"Message effacé. Annuler le récupère."}}
for lang,d in T.items():
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False)+',' for k,v in d.items())
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')

# --- new preference: actionsPosition = bottom | left | right
rep("theme:'light',fontSize:30,controlSize:1,","theme:'light',fontSize:30,controlSize:1,actionsPosition:'bottom',")
rep("layout:['qwerty','abc'],","layout:['qwerty','abc'],actionsPosition:['bottom','left','right'],")
rep("rangeField(tr('Mida dels controls','Tamaño de los controles'),'controlSize',1,1.4,.1,x=>Math.round(x*100)+'%'),",
    "rangeField(tr('Mida dels controls','Tamaño de los controles'),'controlSize',1,1.4,.1,x=>Math.round(x*100)+'%'),"
    "field(tr('Posició dels botons principals','Posición de los botones principales'),selectControl([['bottom',tr('Sota el missatge','Debajo del mensaje')],['left',tr('A l’esquerra del missatge','A la izquierda del mensaje')],['right',tr('A la dreta del missatge','A la derecha del mensaje')]],p.actionsPosition||'bottom',v=>{set('actionsPosition',v);applyAppearance();}),tr('Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.','Hablar, Detener, Mostrar, Borrar palabra, Borrarlo todo y Nuevo mensaje. Hablar siempre es el botón más grande.')),")

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

# --- Delete word moves from the small tools row into the main buttons, next to a new Clear all (bin) button (Marc, 2026-11-07)
rep(" add(tr('Paraula','Palabra'),()=>deleteText(true),'backspace','delete-word-short').setAttribute('aria-label',tr('Esborrar paraula','Borrar palabra'));\n","")
rep("backspace:'M9 5h12v14H9l-7-7 7-7Zm3 4 6 6m0-6-6 6',","backspace:'M9 5h12v14H9l-7-7 7-7Zm3 4 6 6m0-6-6 6',trash:'M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6m4-6v6',")
rep("n.append(speak,stop,show,fresh);",
    "const word=button(tr('Esborrar paraula','Borrar palabra'),()=>deleteText(true),'erase delete-word','backspace');word.id='delete-word';word.dataset.edit='true';word.title=tr('Esborrar paraula','Borrar palabra');"
    "const wipe=button(tr('Esborrar-ho tot','Borrarlo todo'),clearAllText,'erase clear-all','trash');wipe.id='clear-all';wipe.dataset.edit='true';wipe.title=tr('Esborrar-ho tot','Borrarlo todo');"
    "n.append(speak,stop,show,word,wipe,fresh);")
rep("function newMessage(){",
    "function clearAllText(){if(!$('message').value)return;stopTypingFeedback();speech.stop();setMessage('',0);restoreInputFocus();notify(tr('Missatge esborrat. Desfer el recupera.','Mensaje borrado. Deshacer lo recupera.'));}\nfunction newMessage(){")

# --- CSS
css=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'css_add.css'),encoding='utf-8').read()
# Low landscape windows with the panel open: Speak takes the whole first row, the other five share the second.
rep(" .main:not([data-view=closed]) .composer-actions{grid-template-columns:1fr 1fr;gap:5px}",
    " .main:not([data-view=closed]) .composer-actions{grid-template-columns:repeat(5,minmax(0,1fr));gap:5px}.main:not([data-view=closed]) .composer-actions .speak{grid-column:1/-1}")
i=s.rindex('</style>'); s=s[:i]+css+s[i:]

open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

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
    "field(tr('Posició dels botons principals','Posición de los botones principales'),selectControl([['bottom',tr('Sota el missatge','Debajo del mensaje')],['left',tr('A l’esquerra del missatge','A la izquierda del mensaje')],['right',tr('A la dreta del missatge','A la derecha del mensaje')]],p.actionsPosition||'bottom',v=>{set('actionsPosition',v);applyAppearance();}),tr('Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.','Hablar, Detener, Mostrar, Borrar palabra, Borrarlo todo y Nuevo mensaje. Hablar siempre es el botón más grande.')),button(tr('Edició dels botons principals','Edición de los botones principales'),()=>actionEditor(),'','edit'),")

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

# --- editor of the main buttons (Marc, 2026-11-07)
T2={
 "Edició dels botons principals":["Botoi nagusien edizioa","Edición dos botóns principais","Edit main buttons","Modifier les boutons principaux"],
 "Toca un botó de la graella per seleccionar-lo. Després mou-lo, canvia’n la mida o toca una casella buida per portar-l’hi. Parlar sempre és visible i sempre és el botó més gran.":["Ukitu sareta botoi bat hautatzeko. Gero mugitu, aldatu tamaina edo ukitu gelaxka huts bat hara eramateko. Hitz egin beti dago ikusgai eta beti da botoirik handiena.","Toca un botón da grella para seleccionalo. Despois móveo, cambia o seu tamaño ou toca unha casa baleira para levalo alí. Falar sempre está visible e sempre é o botón máis grande.","Tap a button in the grid to select it. Then move it, resize it, or tap an empty cell to put it there. Speak is always shown and is always the largest button.","Touchez un bouton de la grille pour le sélectionner. Ensuite, déplacez-le, changez sa taille ou touchez une case vide pour l’y mettre. Parler est toujours visible et toujours le plus grand bouton."],
 "Graella dels botons":["Botoien sareta","Grella dos botóns","Button grid","Grille des boutons"],
 "Columna lateral · 2 × 5":["Alboko zutabea · 2 × 5","Columna lateral · 2 × 5","Side column · 2 × 5","Colonne latérale · 2 × 5"],
 "Sota el missatge · 12 × 2":["Mezuaren azpian · 12 × 2","Debaixo da mensaxe · 12 × 2","Below the message · 12 × 2","Sous le message · 12 × 2"],
 "Seleccionat: ":["Hautatua: ","Seleccionado: ","Selected: ","Sélectionné : "],
 "amagat":["ezkutatua","oculto","hidden","masqué"],
 "Esquerra":["Ezkerrera","Esquerda","Left","Gauche"],
 "Dreta":["Eskuinera","Dereita","Right","Droite"],
 "Amunt":["Gora","Arriba","Up","Haut"],
 "Avall":["Behera","Abaixo","Down","Bas"],
 "Més ample":["Zabalagoa","Máis ancho","Wider","Plus large"],
 "Més estret":["Estuagoa","Máis estreito","Narrower","Plus étroit"],
 "Més alt":["Altuagoa","Máis alto","Taller","Plus haut"],
 "Més baix":["Baxuagoa","Máis baixo","Shorter","Moins haut"],
 "Botons visibles":["Ikusgai dauden botoiak","Botóns visibles","Visible buttons","Boutons visibles"],
 "Sempre visible.":["Beti ikusgai.","Sempre visible.","Always shown.","Toujours visible."],
 "Restablir":["Berrezarri","Restablecer","Reset","Réinitialiser"],
 "Cancel·lar":["Utzi","Cancelar","Cancel","Annuler"],
 "Desar":["Gorde","Gardar","Save","Enregistrer"],
 "Casella buida":["Gelaxka hutsa","Casa baleira","Empty cell","Case vide"],
 "No hi cap dins de la graella.":["Ez da saretan sartzen.","Non cabe na grella.","It does not fit in the grid.","Il ne tient pas dans la grille."],
 "Aquest lloc ja l’ocupa ":["Leku hau honek hartzen du: ","Este lugar xa o ocupa ","This place is taken by ","Cette place est occupée par "],
 "Parlar ha de ser més gran que la resta de botons.":["Hitz egin botoiak besteak baino handiagoa izan behar du.","Falar ten que ser máis grande que o resto de botóns.","Speak must be larger than the other buttons.","Parler doit être plus grand que les autres boutons."],
 "Aquest botó està amagat.":["Botoi hau ezkutatuta dago.","Este botón está oculto.","This button is hidden.","Ce bouton est masqué."],
 "No queda lloc lliure. Fes més petit o amaga un altre botó.":["Ez dago leku librerik. Txikitu edo ezkutatu beste botoi bat.","Non queda sitio libre. Fai máis pequeno ou oculta outro botón.","There is no free space. Make another button smaller or hide it.","Il n’y a plus de place. Réduisez ou masquez un autre bouton."],
 "S’ha recuperat la disposició inicial. Desa per aplicar-la.":["Hasierako antolamendua berreskuratu da. Gorde aplikatzeko.","Recuperouse a disposición inicial. Garda para aplicala.","The initial layout is back. Save to apply it.","La disposition initiale est rétablie. Enregistrez pour l’appliquer."],
 "Botons principals desats.":["Botoi nagusiak gorde dira.","Botóns principais gardados.","Main buttons saved.","Boutons principaux enregistrés."],
 "Mou, canvia de mida, mostra o amaga cada botó.":["Mugitu, aldatu tamaina, erakutsi edo ezkutatu botoi bakoitza.","Move, cambia o tamaño, mostra ou oculta cada botón.","Move, resize, show or hide each button.","Déplacez, redimensionnez, affichez ou masquez chaque bouton."],
}
for i,lang in enumerate(['eu','gl','en','fr']):
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v[i],ensure_ascii=False)+',' for k,v in T2.items() if k not in ('Desar','Cancel·lar') or ('"%s":'%k) not in s.split('"%s":{'%lang,1)[1][:200000])
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')
# core: keep a valid saved layout through reloads and backups
rep("    return s;\n  }\n  function validateBackup(raw) {",
    "    s.actionLayouts=actionLayouts(raw.actionLayouts);\n    return s;\n  }\n"
    "  function actionLayouts(raw){const out={side:null,bottom:null};if(!raw||typeof raw!=='object'||Array.isArray(raw))return out;const grids={side:[2,5],bottom:[12,2]};for(const k of ['side','bottom']){const L=raw[k];if(!L||typeof L!=='object'||Array.isArray(L))continue;const [C,R]=grids[k];const o={};let ok=true;for(const id of ['speak','stop','show','word','clear','new']){const v=L[id];if(!Array.isArray(v)||v.length!==5||!v.every(Number.isInteger)){ok=false;break;}const [x,y,w,h,on]=v;if(x<0||y<0||w<1||h<1||x+w>C||y+h>R||(on!==0&&on!==1)){ok=false;break;}o[id]=v.slice();}if(ok&&o.speak[4]===1)out[k]=o;}return out;}\n"
    "  function validateBackup(raw) {")
# app: the editor, applied after the buttons are drawn and when the position changes
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'action_editor.js'),encoding='utf-8').read()
rep("function clearAllText(){","%s\nfunction clearAllText(){"%js.strip())
rep("n.append(speak,stop,show,word,wipe,fresh);","n.append(speak,stop,show,word,wipe,fresh);applyActionLayout();")
rep("$('composer').dataset.actions=prefs().actionsPosition||'bottom';","$('composer').dataset.actions=prefs().actionsPosition||'bottom';if(typeof applyActionLayout==='function')applyActionLayout();")

# --- CSS
css=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'css_add.css'),encoding='utf-8').read()
# Low landscape windows with the panel open: Speak takes the whole first row, the other five share the second.
rep(" .main:not([data-view=closed]) .composer-actions{grid-template-columns:1fr 1fr;gap:5px}",
    " .main:not([data-view=closed]) .composer-actions{grid-template-columns:repeat(5,minmax(0,1fr));gap:5px}.main:not([data-view=closed]) .composer-actions .speak{grid-column:1/-1}")
i=s.rindex('</style>'); s=s[:i]+css+s[i:]

open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

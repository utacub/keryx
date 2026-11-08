# Applies the UTAC Keryx 0.6.8 change to the built UTAC_Keryx_v0.6.7_local.html (Marc, 2026-11-08):
# - removes switch access (scanning with one or two switches) and every option that belongs to it;
# - removes Keryx's own on-screen keyboard (panel tab, keyboard in dialogs, settings);
# - text always arrives through the system: any physical keyboard or the operating system's on-screen keyboard;
#   the message never sets inputmode="none", and a character typed while a button has the focus goes to the message;
# - the keyboard access manual moves from Information to the end of Settings -> Access;
# - in Information, "Origen i institucions" moves up, just below "Per què es diu Keryx".
# Usage: python3 patch068.py UTAC_Keryx_v0.6.7_local.html UTAC_Keryx_v0.6.8_local.html
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.7(?!:)','0.6.8',s)

# ---------- Settings model: only direct access and dwell remain; no own keyboard ----------
rep("for(const k of ['readLetters','readWords','readSentences','keyboard','uppercase',",
    "for(const k of ['readLetters','readWords','readSentences','uppercase',")
rep("access:['direct','scan1','scan2','dwell']","access:['direct','dwell']")
# Old shortcut check against switch keys is gone.
rep("if(access.startsWith('scan')&&[selectKey,nextKey].includes(value.replace(/^Shift\\+/,'')))return 'switch';","")
rep("return prefs().shortcutsEnabled&&(!prefs().access.startsWith('scan')||![prefs().selectKey,prefs().nextKey].includes(value.replace(/^Shift\\+/,'')))?value:'';",
    "return prefs().shortcutsEnabled?value:'';")
rep("error.textContent=problem==='switch'?tr('Aquesta tecla està reservada per als commutadors. Tria’n una altra.','Esta tecla está reservada para los conmutadores. Elige otra.'):tr('Aquesta drecera ja està assignada a una altra acció.','Este atajo ya está asignado a otra acción.');",
    "error.textContent=tr('Aquesta drecera ja està assignada a una altra acció.','Este atajo ya está asignado a otra acción.');")

# ---------- The message always accepts the system keyboards ----------
rep("$('message').inputMode=(prefs().keyboard||prefs().access!=='direct')?'none':'text';}",
    "$('message').inputMode='text';}")
rep("document.addEventListener('focusin',e=>{if(e.target.matches('textarea,input[type=text],input[type=search],input:not([type])')){activeTarget=e.target;if($('dialog').open&&prefs().access!=='direct'){e.target.inputMode='none';showDialogKeyboard();}}});",
    "document.addEventListener('focusin',e=>{if(e.target.matches('textarea,input[type=text],input[type=search],input:not([type])'))activeTarget=e.target;});")
# After an action the caret goes back to the message in every access mode, so the system keyboard keeps writing there.
rep("function restoreInputFocus(n=$('message')){if(prefs().access==='direct'){n.focus({preventScroll:true});if(n===$('message'))n.setSelectionRange(conversation().start,conversation().end);}activeTarget=n;}",
    "function restoreInputFocus(n=$('message')){n.focus({preventScroll:true});if(n===$('message'))n.setSelectionRange(conversation().start,conversation().end);activeTarget=n;}")

# ---------- Panel: no Keyboard tab ----------
rep("for(const [id,ca,es,ic]of [['keyboard','Teclat','Teclado','keyboard'],['quick',","for(const [id,ca,es,ic]of [['quick',")
rep("activeView=id;panelOpen=true;listPage=0;historyPage=0;if(id==='keyboard'){prefs().keyboard=true;persist();applyAppearance();}renderWorkspace();",
    "activeView=id;panelOpen=true;listPage=0;historyPage=0;renderWorkspace();")
rep(" if(activeView==='keyboard'){renderKeyboard(n,$('message'));return;}\n"," if(activeView==='keyboard')activeView='quick';\n")

# ---------- Dialogs: no own keyboard ----------
rep('<div id="dialog-keyboard" class="dialog-keyboard" hidden></div>','')
rep("$('dialog-body').classList.remove('rotate-message');$('dialog-keyboard').hidden=true;clear($('dialog-keyboard'));",
    "$('dialog-body').classList.remove('rotate-message');")
i=s.index(" if(editable){const toggle=button(tr('Teclat','Teclado')"); j=s.index('\n',i)
assert "toggle.id='dialog-keyboard-toggle'" in s[i:j]
s=s[:i]+s[j+1:]
rep(" const editable=dialogItems.some(n=>n.matches('input[type=text],textarea:not([readonly]),input[type=search]')||n.querySelector('input[type=text],textarea:not([readonly]),input[type=search]'));\n","")
rep("fn?.();$('dialog-keyboard').hidden=true;activeTarget=$('message');","fn?.();activeTarget=$('message');")
rep("if(userAction){const anchor=dialogPages[index]?.firstElementChild;activeTarget=null;if(!$('dialog-keyboard').hidden){$('dialog-keyboard').hidden=true;clear($('dialog-keyboard'));reflowDialog(anchor);return;}}\n",
    "if(userAction)activeTarget=null;\n")
i=s.index("function hideDialogKeyboard(){"); j=s.index("\n}\n",s.index("function showDialogKeyboard(){"))+3
s=s[:i]+s[j:]
rep(" activeTarget=input;if(prefs().access!=='direct')showDialogKeyboard();\n"," activeTarget=input;\n")

# ---------- Remove the on-screen keyboard renderer ----------
i=s.index("// On-screen keyboard works in the composer and in editable dialog fields.\n"); j=s.index("// Switch scanning: a single active surface")
seg=s[i:j]; assert seg.count('function renderKeyboard(')==1 and 'container.append(keyboard);}' in seg
s=s[:i]+s[j:]
rep("renderKeyboard=stableRender(renderKeyboard);","")
i=s.index("function prepareScreenKeyboards(){"); j=s.index("function syncKeyboard(){",i); assert s[i:j].count('function ')==1; s=s[:i]+s[j:]
rep("prepareHistoryGrid();prepareScreenKeyboards();","prepareHistoryGrid();")

# ---------- Access: direct (touch, mouse, any keyboard) or dwell; no scanning ----------
rep("// Switch scanning: a single active surface, optional groups, and predictable escape.\nlet accessRunning=false,scanTimer=null,scanLevel='groups',scanIndex=-1,scanItems=[],selectedGroup=null,scanTurns=0,dwellTarget=null,",
    "// Pointer dwell. Switch scanning was removed in 0.6.8.\nlet accessRunning=false,dwellTarget=null,")
def cut(start,end_marker):
    global s
    i=s.index(start); j=s.index(end_marker,i); s=s[:i]+s[j:]
cut("function removeHighlights(){","function resetAccess(){")
rep("function resetAccess(){clearTimeout(scanTimer);scanTimer=null;cancelDwell();dwellBlocked=true;removeHighlights();scanLevel='groups';selectedGroup=null;scanIndex=-1;scanTurns=0;if(accessRunning&&prefs().access.startsWith('scan')){scanItems=getScanItems();nextScan();}}",
    "function resetAccess(){cancelDwell();dwellBlocked=true;}")
rep("accessRunning=true;panelOpen=true;if(prefs().access.startsWith('scan')){prefs().keyboard=true;activeView='keyboard';renderWorkspace();applyAppearance();}renderAccess();resetAccess();}",
    "accessRunning=true;panelOpen=true;renderAccess();resetAccess();}")
rep("function pauseAccess(render=true){accessRunning=false;clearTimeout(scanTimer);scanTimer=null;cancelDwell();removeHighlights();if(render)renderAccess();}",
    "function pauseAccess(render=true){accessRunning=false;cancelDwell();if(render)renderAccess();}")
cut("function scheduleScan(){","function activateControl(n){")
# A text field chosen by dwell gets the focus, so the system keyboard writes there.
rep("if(n.matches('textarea,input[type=text],input[type=search],input:not([type])')){n.focus({preventScroll:true});activeTarget=n;if(n.readOnly){n.select();return;}n.inputMode='none';if($('dialog').open)showDialogKeyboard();else if(n.type==='search'){searchDialog();}else{activeTarget=n;activeView='keyboard';panelOpen=true;renderWorkspace();renderKeyboard($('workspace-body'),n);}return;}n.click();}",
    "if(n.matches('textarea,input[type=text],input[type=search],input:not([type])')){n.focus({preventScroll:true});activeTarget=n;if(n.readOnly)n.select();else if(!$('dialog').open&&n.type==='search')searchDialog();return;}n.click();}")
i=s.index("const isScan=prefs().access.startsWith('scan');const hint=isScan?"); j=s.index("tr('Mantén el punter sobre un botó",i)
s=s[:i]+"const hint="+s[j:]
rep(" if(accessRunning&&prefs().access.startsWith('scan')&&(k===prefs().selectKey||(prefs().access==='scan2'&&k===prefs().nextKey))){e.preventDefault();e.stopPropagation();if(e.repeat)return;k===prefs().selectKey?selectScan():nextScan();return;}\n","")
rep("if(accessRunning){e.preventDefault();e.stopImmediatePropagation();if(prefs().access.startsWith('scan')&&scanLevel==='items')resetAccess();else pauseAccess();return;}}",
    "if(accessRunning){e.preventDefault();e.stopImmediatePropagation();pauseAccess();return;}}")
# Undo and redo in the message: AltGr combinations (Ctrl+Alt on Windows) are characters, not commands.
rep("if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'&&e.target===$('message'))","if((e.ctrlKey||e.metaKey)&&!e.altKey&&typeof e.key==='string'&&e.key.toLowerCase()==='z'&&e.target===$('message'))")
rep("if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='y'&&e.target===$('message'))","if((e.ctrlKey||e.metaKey)&&!e.altKey&&typeof e.key==='string'&&e.key.toLowerCase()==='y'&&e.target===$('message'))")
rep(" if(e.altKey||$('dialog').open||accessRunning&&prefs().access.startsWith('scan'))return;"," if(e.altKey||$('dialog').open)return;")

# Settings -> Access
i=s.index(" content.append(button(tr('Dreceres del teclat físic','Atajos del teclado físico'),()=>shortcutsDialog(),'soft','keyboard'));let mode=p.access;")
j=s.index("}else if(tab==='writing'){",i)
ACCESS=r""" content.append(el('p',{class:'notice'},tr('Keryx funciona amb qualsevol teclat físic connectat i amb el teclat en pantalla del sistema operatiu. No té teclat propi.','Keryx funciona con cualquier teclado físico conectado y con el teclado en pantalla del sistema operativo. No tiene teclado propio.')),button(tr('Dreceres del teclat físic','Atajos del teclado físico'),()=>shortcutsDialog(),'soft','keyboard'));let mode=p.access;const modeSelect=selectControl([['direct',tr('Tacte, ratolí o teclat físic','Tacto, ratón o teclado físico')],['dwell',tr('Punter amb permanència','Puntero con permanencia')]],mode,v=>mode=v);
 content.append(field(tr('Mètode d’accés','Método de acceso'),modeSelect),el('p',{class:'notice'},tr('La permanència s’activa amb el botó del final i Esc la pausa. Utilitza el punter del sistema; aquesta versió no fa calibratge ocular. Per escriure, fes servir el teclat en pantalla del sistema.','La permanencia se activa con el botón del final y Esc la pausa. Utiliza el puntero del sistema; esta versión no realiza calibración ocular. Para escribir, usa el teclado en pantalla del sistema.')),rangeField(tr('Temps de permanència','Tiempo de permanencia'),'dwellMs',300,5000,100,x=>(x/1000).toFixed(1)+' s'),rangeField(tr('Filtre de repetició del mateix botó','Filtro de repetición del mismo botón'),'repeatMs',0,2000,100,x=>x?x+' ms':tr('Desactivat','Desactivado')));
 content.append(button(tr('Aplicar i provar l’accés','Aplicar y probar el acceso'),()=>{p.access=mode;persist();closeDialog();renderAll();startAccess();},'primary'));
 const manual=el('div',{class:'keyboard-manual',id:'keyboard-manual'},el('h3',{},tr('Manual d’accés amb teclat','Manual de acceso con teclado')),...keyboardManualBody());content.append(manual);
"""
s=s[:i]+ACCESS+s[j:]
# Settings -> Writing: no own keyboard option
rep(",check(tr('Fer servir el teclat de pantalla propi','Usar el teclado de pantalla propio'),p.keyboard,v=>{set('keyboard',v);applyAppearance();})","")
# Old first-use window (not opened since 0.6.5) keeps only the remaining access methods
rep(",['scan1',tr('Un commutador (F8)','Un conmutador (F8)')],['scan2',tr('Dos commutadors (F9 i F8)','Dos conmutadores (F9 y F8)')]]","]")

# ---------- Keyboard manual: content shared, shown at the end of Settings -> Access ----------
rep("function keyboardManual(back=helpDialog){\n const section=(title,content)=>el('div',{class:'manual-section'},el('h3',{},title),el('p',{class:'prose'},content));\n const body=[el('p',{class:'welcome-intro'},",
    "function keyboardManualBody(){\n const section=(title,content)=>el('div',{class:'manual-section'},el('h4',{},title),el('p',{class:'prose'},content));\n const body=[el('p',{class:'prose'},")
rep("tr('A la barra Teclat, Respostes, Favorits, Frases i Historial, fes servir ← i → per triar una pestanya. Prem Intro o Espai per obrir-la. Tab entra al contingut. Els apartats dels ajustos funcionen igual. Inici i Fi van al primer i al darrer element del bloc.','En la barra Teclado, Respuestas, Favoritos, Frases e Historial, utiliza ← y → para elegir una pestaña. Pulsa Intro o Espacio para abrirla. Tab entra en el contenido. Los apartados de ajustes funcionan igual. Inicio y Fin van al primer y al último elemento del bloque.')",
    "tr('A la barra Respostes, Favorits, Frases, Historial i Documents, fes servir ← i → per triar una pestanya. Prem Intro o Espai per obrir-la. Tab entra al contingut. Els apartats dels ajustos funcionen igual. Inici i Fi van al primer i al darrer element del bloc.','En la barra Respuestas, Favoritos, Frases, Historial y Documentos, utiliza ← y → para elegir una pestaña. Pulsa Intro o Espacio para abrirla. Tab entra en el contenido. Los apartados de ajustes funcionan igual. Inicio y Fin van al primer y al último elemento del bloque.')")
rep("section(tr('8. Commutadors i dreceres','8. Conmutadores y atajos'),tr('Amb l’escombratge actiu, les tecles de seleccionar i avançar tenen prioritat, i les dreceres de conversa queden en pausa. Esc torna al grup o pausa l’escombratge. Per recuperar el teclat convencional, pausa l’escombratge. No cal activar cap escombratge per navegar amb Tab i fletxes.','Con el barrido activo, las teclas de seleccionar y avanzar tienen prioridad, y los atajos de conversación quedan en pausa. Esc vuelve al grupo o pausa el barrido. Para recuperar el teclado convencional, pausa el barrido. No hace falta activar el barrido para navegar con Tab y flechas.'))",
    "section(tr('8. Qualsevol teclat','8. Cualquier teclado'),tr('Keryx no té teclat propi: escriu amb el teclat físic que tinguis connectat o amb el teclat en pantalla del sistema operatiu, amb la seva distribució, els accents i les tecles mortes. Si el focus és en un botó i escrius una lletra, va al missatge. Amb un teclat en pantalla que tingui tecles de funció, fletxes i Tab, les dreceres i la navegació funcionen igual que amb un teclat físic.','Keryx no tiene teclado propio: escribe con el teclado físico que tengas conectado o con el teclado en pantalla del sistema operativo, con su distribución, los acentos y las teclas muertas. Si el foco está en un botón y escribes una letra, va al mensaje. Con un teclado en pantalla que tenga teclas de función, flechas y Tab, los atajos y la navegación funcionan igual que con un teclado físico.'))")
rep(" el('h3',{},tr('Dreceres d’aquest perfil','Atajos de este perfil'))];"," el('h4',{},tr('Dreceres d’aquest perfil','Atajos de este perfil'))];")
i=s.index(" openDialog(tr('Manual d’accés amb teclat','Manual de acceso con teclado'),body,[button(tr('Configurar dreceres','Configurar atajos')")
j=s.index("\n}\n",i)
s=s[:i]+" return body;\n}\n/* 0.6.8: the manual lives at the end of Settings -> Access. */\nfunction keyboardManual(){settingsDialog('access');requestAnimationFrame(()=>requestAnimationFrame(()=>{const m=$('keyboard-manual');if(!m)return;m.scrollIntoView({block:'start'});const h=m.querySelector('h3');h.tabIndex=-1;h.focus({preventScroll:true});}));"+s[j:]
rep("button(tr('Manual de teclat','Manual de teclado'),()=>keyboardManual(()=>shortcutsDialog(back)))","button(tr('Manual de teclat','Manual de teclado'),()=>keyboardManual())")

# ---------- A character typed while a button has the focus goes to the message ----------
TYPE=r"""
/* 0.6.8: any keyboard writes in the message. When the focus is on a button of the main screen and a character
   key is pressed (physical keyboard or a system on-screen keyboard that sends keys), the message takes the focus
   before the character is inserted. Space and Enter keep activating buttons; dialogs, menus and lists keep their keys. */
document.addEventListener('keydown',e=>{
 if(e.defaultPrevented||e.isComposing||composing||e.keyCode===229||typeof e.key!=='string'||e.key.length!==1||e.key===' ')return;
 if((e.ctrlKey||e.metaKey||e.altKey)&&!e.getModifierState?.('AltGraph'))return;
 const t=e.target;if($('dialog').open||themePopup||editableNative(t)||t?.closest?.('[role=menu],[role=listbox]'))return;
 const m=$('message');if(!m||m.disabled||m.readOnly||!m.getClientRects().length)return;
 m.focus({preventScroll:true});m.setSelectionRange(conversation().start,conversation().end);activeTarget=m;
});
"""
rep("document.addEventListener('keydown',physicalKeyboard);\n","document.addEventListener('keydown',physicalKeyboard);\n"+TYPE)

# ---------- Information ----------
rep("tr('Keryx és un comunicador alfabètic d’UTAC per escriure missatges, llegir-los en veu alta o mostrar-los a l’interlocutor. Inclou frases editables i opcions d’accés amb ratolí, tacte, teclat físic, permanència i commutadors.','Keryx es un comunicador alfabético de UTAC para escribir mensajes, leerlos en voz alta o mostrarlos al interlocutor. Incluye frases editables y opciones de acceso con ratón, tacto, teclado físico, permanencia y conmutadores.')",
    "tr('Keryx és un comunicador alfabètic d’UTAC per escriure missatges, llegir-los en veu alta o mostrar-los a l’interlocutor. Inclou frases editables i es fa servir amb ratolí, tacte o permanència, i amb qualsevol teclat físic o el teclat en pantalla del sistema.','Keryx es un comunicador alfabético de UTAC para escribir mensajes, leerlos en voz alta o mostrarlos al interlocutor. Incluye frases editables y se usa con ratón, tacto o permanencia, y con cualquier teclado físico o el teclado en pantalla del sistema.')")
rep("button(tr('Manual d’accés amb teclat','Manual de acceso con teclado'),()=>keyboardManual(),'primary','keyboard'),el('h3',{},tr('Com començar','Cómo empezar'))",
    "el('h3',{'data-about':'start'},tr('Com començar','Cómo empezar'))")
rep("tr('El teclat propi inclou accents, ç, ñ, l·l, apòstrofs, nombres i signes. L’escombratge selecciona grups i després caselles, o caselles directament. En controls de llista, seleccionar avança a l’opció següent; en barres, augmenta el valor i torna al mínim al final.','El teclado propio incluye acentos, ç, ñ, l·l, apóstrofos, números y signos. El barrido selecciona grupos y después casillas, o casillas directamente. En controles de lista, seleccionar avanza a la siguiente opción; en barras, aumenta el valor y vuelve al mínimo al final.')",
    "tr('Escriu amb qualsevol teclat físic connectat o amb el teclat en pantalla del sistema operatiu. El manual d’accés amb teclat és al final d’Ajustos → Accés.','Escribe con cualquier teclado físico conectado o con el teclado en pantalla del sistema operativo. El manual de acceso con teclado está al final de Ajustes → Acceso.')")
rep("tr('Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges bilingües editables, categories, favorits, perfils, còpies, teclat propi i una primera implementació d’escombratge i permanència. La compleció opcional es limita a les paraules del banc de frases.','Incluye el editor, voz del navegador y voces descargables, presentación de texto, 90 mensajes bilingües editables, categorías, favoritos, perfiles, copias, teclado propio y una primera implementación de barrido y permanencia. La compleción opcional se limita a las palabras del banco de frases.')",
    "tr('Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges bilingües editables, categories, favorits, documents, perfils, còpies i una primera implementació de la permanència. L’escriptura es fa sempre amb el teclat físic o el teclat en pantalla del sistema. La compleció opcional es limita a les paraules del banc de frases.','Incluye el editor, voz del navegador y voces descargables, presentación de texto, 90 mensajes bilingües editables, categorías, favoritos, documentos, perfiles, copias y una primera implementación de la permanencia. La escritura se hace siempre con el teclado físico o el teclado en pantalla del sistema. La compleción opcional se limita a las palabras del banco de frases.')")
# Origin and institutions: just below "Per què es diu Keryx"
rep(" content.append(el('h3',{},tr('Origen i institucions','Origen e instituciones')),",
    " const originAt=content.children.length;content.append(el('h3',{},tr('Origen i institucions','Origen e instituciones')),")
i=s.index(" const originAt=content.children.length;"); j=s.index("\n",i)
s=s[:j]+"\n {const start=content.querySelector('[data-about=start]'),moved=[...content.children].slice(originAt);if(start)for(const n of moved)content.insertBefore(n,start);}"+s[j:]

# ---------- Translations of the new texts (eu, gl, en, fr) ----------
T={
"Keryx funciona amb qualsevol teclat físic connectat i amb el teclat en pantalla del sistema operatiu. No té teclat propi.":[
 "Keryx edozein teklatu fisiko konektaturekin eta sistema eragilearen pantailako teklatuarekin dabil. Ez du teklatu propiorik.",
 "Keryx funciona con calquera teclado físico conectado e co teclado en pantalla do sistema operativo. Non ten teclado propio.",
 "Keryx works with any connected physical keyboard and with the operating system’s on-screen keyboard. It has no keyboard of its own.",
 "Keryx fonctionne avec tout clavier physique connecté et avec le clavier à l’écran du système d’exploitation. Il n’a pas de clavier propre."],
"La permanència s’activa amb el botó del final i Esc la pausa. Utilitza el punter del sistema; aquesta versió no fa calibratge ocular. Per escriure, fes servir el teclat en pantalla del sistema.":[
 "Egonaldia amaierako botoiarekin aktibatzen da, eta Esc teklak eteten du. Sistemaren erakuslea erabiltzen du; bertsio honek ez du begi-kalibraziorik egiten. Idazteko, erabili sistemaren pantailako teklatua.",
 "A permanencia actívase co botón do final e Esc ponna en pausa. Usa o punteiro do sistema; esta versión non fai calibración ocular. Para escribir, usa o teclado en pantalla do sistema.",
 "Dwell is started with the button at the end, and Esc pauses it. It uses the system pointer; this version does not calibrate eye tracking. To type, use the system on-screen keyboard.",
 "La sélection par maintien démarre avec le bouton du bas, et Échap la met en pause. Elle utilise le pointeur du système ; cette version n’effectue pas de calibrage oculaire. Pour écrire, utilisez le clavier à l’écran du système."],
"A la barra Respostes, Favorits, Frases, Historial i Documents, fes servir ← i → per triar una pestanya. Prem Intro o Espai per obrir-la. Tab entra al contingut. Els apartats dels ajustos funcionen igual. Inici i Fi van al primer i al darrer element del bloc.":[
 "Erantzunak, Gogokoak, Esaldiak, Historia eta Dokumentuak barran, erabili ← eta → fitxa bat aukeratzeko. Sakatu Sartu edo Zuriunea irekitzeko. Tab teklak edukira sartzen da. Ezarpenen atalek berdin funtzionatzen dute. Hasiera eta Amaiera blokeko lehen eta azken elementura doaz.",
 "Na barra Respostas, Favoritos, Frases, Historial e Documentos, usa ← e → para escoller unha lapela. Preme Intro ou Espazo para abrila. Tab entra no contido. Os apartados dos axustes funcionan igual. Inicio e Fin van ao primeiro e ao último elemento do bloque.",
 "In the Replies, Favourites, Phrases, History and Documents bar, use ← and → to choose a tab. Press Enter or Space to open it. Tab moves into the content. Settings sections work the same way. Home and End go to the first and last item of the block.",
 "Dans la barre Réponses, Favoris, Phrases, Historique et Documents, utilisez ← et → pour choisir un onglet. Appuyez sur Entrée ou Espace pour l’ouvrir. Tab entre dans le contenu. Les rubriques des réglages fonctionnent de la même façon. Début et Fin vont au premier et au dernier élément du bloc."],
"8. Qualsevol teclat":["8. Edozein teklatu","8. Calquera teclado","8. Any keyboard","8. N’importe quel clavier"],
"Keryx no té teclat propi: escriu amb el teclat físic que tinguis connectat o amb el teclat en pantalla del sistema operatiu, amb la seva distribució, els accents i les tecles mortes. Si el focus és en un botó i escrius una lletra, va al missatge. Amb un teclat en pantalla que tingui tecles de funció, fletxes i Tab, les dreceres i la navegació funcionen igual que amb un teclat físic.":[
 "Keryxek ez du teklatu propiorik: idatzi konektatuta duzun teklatu fisikoarekin edo sistema eragilearen pantailako teklatuarekin, haren banaketarekin, azentuekin eta tekla hilekin. Fokua botoi batean dagoela letra bat idazten baduzu, mezura doa. Funtzio-teklak, geziak eta Tab dituen pantailako teklatu batekin, lasterbideek eta nabigazioak teklatu fisiko batekin bezala funtzionatzen dute.",
 "Keryx non ten teclado propio: escribe co teclado físico que teñas conectado ou co teclado en pantalla do sistema operativo, coa súa distribución, os acentos e as teclas mortas. Se o foco está nun botón e escribes unha letra, vai á mensaxe. Cun teclado en pantalla que teña teclas de función, frechas e Tab, os atallos e a navegación funcionan igual ca cun teclado físico.",
 "Keryx has no keyboard of its own: type with the physical keyboard you have connected or with the operating system’s on-screen keyboard, with its layout, accents and dead keys. If the focus is on a button and you type a letter, it goes to the message. With an on-screen keyboard that has function keys, arrows and Tab, shortcuts and navigation work just as with a physical keyboard.",
 "Keryx n’a pas de clavier propre : écrivez avec le clavier physique connecté ou avec le clavier à l’écran du système d’exploitation, avec sa disposition, ses accents et ses touches mortes. Si le focus est sur un bouton et que vous tapez une lettre, elle va dans le message. Avec un clavier à l’écran doté de touches de fonction, de flèches et de Tab, les raccourcis et la navigation fonctionnent comme avec un clavier physique."],
"Keryx és un comunicador alfabètic d’UTAC per escriure missatges, llegir-los en veu alta o mostrar-los a l’interlocutor. Inclou frases editables i es fa servir amb ratolí, tacte o permanència, i amb qualsevol teclat físic o el teclat en pantalla del sistema.":[
 "Keryx UTACen komunikatzaile alfabetikoa da, mezuak idazteko, ozen irakurtzeko edo solaskideari erakusteko. Esaldi editagarriak ditu, eta saguarekin, ukipenarekin edo egonaldiarekin erabiltzen da, baita edozein teklatu fisikorekin edo sistemaren pantailako teklatuarekin ere.",
 "Keryx é un comunicador alfabético da UTAC para escribir mensaxes, lelas en voz alta ou mostralas ao interlocutor. Inclúe frases editables e úsase co rato, o tacto ou a permanencia, e con calquera teclado físico ou o teclado en pantalla do sistema.",
 "Keryx is an alphabetic communicator from UTAC for writing messages, reading them aloud or showing them to the other person. It includes editable phrases and is used with a mouse, touch or dwell, and with any physical keyboard or the system on-screen keyboard.",
 "Keryx est un communicateur alphabétique de l’UTAC pour écrire des messages, les lire à voix haute ou les montrer à l’interlocuteur. Il comprend des phrases modifiables et s’utilise à la souris, au toucher ou par maintien, ainsi qu’avec tout clavier physique ou le clavier à l’écran du système."],
"Escriu amb qualsevol teclat físic connectat o amb el teclat en pantalla del sistema operatiu. El manual d’accés amb teclat és al final d’Ajustos → Accés.":[
 "Idatzi edozein teklatu fisiko konektaturekin edo sistema eragilearen pantailako teklatuarekin. Teklatuarekin sartzeko eskuliburua Ezarpenak → Sarbidea ataleko amaieran dago.",
 "Escribe con calquera teclado físico conectado ou co teclado en pantalla do sistema operativo. O manual de acceso con teclado está ao final de Axustes → Acceso.",
 "Type with any connected physical keyboard or with the operating system’s on-screen keyboard. The keyboard access manual is at the end of Settings → Access.",
 "Écrivez avec tout clavier physique connecté ou avec le clavier à l’écran du système d’exploitation. Le manuel d’accès au clavier se trouve à la fin de Réglages → Accès."],
"Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges bilingües editables, categories, favorits, documents, perfils, còpies i una primera implementació de la permanència. L’escriptura es fa sempre amb el teclat físic o el teclat en pantalla del sistema. La compleció opcional es limita a les paraules del banc de frases.":[
 "Editorea, nabigatzailearen ahotsa eta ahots deskargagarriak, testuaren aurkezpena, 90 mezu elebidun editagarri, kategoriak, gogokoak, dokumentuak, profilak, kopiak eta egonaldiaren lehen inplementazio bat ditu. Beti teklatu fisikoarekin edo sistemaren pantailako teklatuarekin idazten da. Aukerako osaketa esaldi-bankuko hitzetara mugatzen da.",
 "Inclúe o editor, a voz do navegador e voces descargables, a presentación do texto, 90 mensaxes bilingües editables, categorías, favoritos, documentos, perfís, copias e unha primeira implementación da permanencia. Escríbese sempre co teclado físico ou co teclado en pantalla do sistema. A compleción opcional limítase ás palabras do banco de frases.",
 "Includes the editor, the browser voice and downloadable voices, text display, 90 editable bilingual messages, categories, favourites, documents, profiles, backups and a first implementation of dwell. Typing is always done with the physical keyboard or the system on-screen keyboard. Optional completion is limited to the words in the phrase bank.",
 "Comprend l’éditeur, la voix du navigateur et des voix téléchargeables, l’affichage du texte, 90 messages bilingues modifiables, des catégories, des favoris, des documents, des profils, des copies et une première mise en œuvre du maintien. La saisie se fait toujours avec le clavier physique ou le clavier à l’écran du système. La complétion facultative se limite aux mots de la banque de phrases."],
}
LANGS=['eu','gl','en','fr']
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(LANGS):
    key='"'+lang+'":{'
    k=s.index(key,i)+len(key)
    add=''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())
    s=s[:k]+add+s[k:]

CSS="""
/* 0.6.8: keyboard manual at the end of Settings -> Access */
.keyboard-manual{margin-top:18px;padding-top:14px;border-top:1px solid var(--line)}.keyboard-manual>h3{margin:0 0 8px}.keyboard-manual h4{margin:14px 0 4px;font-size:15px}.keyboard-manual h3:focus{outline:none}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
for bad in ['showDialogKeyboard','hideDialogKeyboard','renderKeyboard','dialog-keyboard\'','selectScan','nextScan','scan1','scan2']:
    assert bad not in s, bad
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

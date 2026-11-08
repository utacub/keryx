# Applies the UTAC Keryx 0.7.0 change to the built index.html of 0.6.14 (Marc, 2026-11-08):
# word prediction for physical keyboards. An option of Settings -> Access, off by default.
# - Engine: tools/patch-0.7.0/predict.js (inlined), lexicons lex/<lang>.json from tools/lexicon/build_lexicon.py.
# - Numbered suggestions under the message; Tab inserts the first, F1-F5 any of them, Esc hides them; all keys can be changed.
# - Learns from the messages the person speaks (not in private mode), per profile and language, in localStorage
#   'utac.keryx.predict.v1'; words outside the vocabulary are proposed after two uses; learned words can be forgotten.
# - The old "Complete words from my phrase bank" option (Writing tab) is replaced: phrases now feed the new engine.
# - No single-file edition any more (Marc, 2026-11-08): the app is the web/PWA; the portable HTML link is removed.
# Usage: python3 patch070.py index.html(0.6.14) index.html(0.7.0)
import sys, re, json, os
src, dst = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8', newline='').read()
def rep(a, b, count=1):
    global s
    n = s.count(a); assert n == count, (a[:90], n); s = s.replace(a, b)
s = re.sub(r'(?<!/\* )0\.6\.14(?![:\d])', '0.7.0', s)

# the lexicons are fetched from the same origin
rep("connect-src blob: https://cdn.jsdelivr.net", "connect-src 'self' blob: https://cdn.jsdelivr.net")

# ---- engine
engine = open(os.path.join(HERE, 'predict.js'), encoding='utf-8').read()
engine = engine.replace("if(typeof module!=='undefined')module.exports=KeryxPredict;\n", '')
rep("const KeryxI18n=(()=>{", engine + "const KeryxI18n=(()=>{")

# ---- settings (core)
rep("const SHORTCUT_KEYS=['','Primary+Enter',",
    "const PREDICT_KEYS=['','Tab','Insert','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F12'];\n"
    "  const predictDefaults=()=>({enabled:false,when:'physical',count:3,learn:true,keys:['Tab','F1','F2','F3','F4','F5']});\n"
    "  function predictSettings(raw){const s=predictDefaults();if(!raw||typeof raw!=='object'||Array.isArray(raw))return s;if(typeof raw.enabled==='boolean')s.enabled=raw.enabled;if(typeof raw.learn==='boolean')s.learn=raw.learn;s.when=['physical','always'].includes(raw.when)?raw.when:'physical';s.count=typeof raw.count==='number'&&Number.isFinite(raw.count)?Math.max(1,Math.min(5,Math.round(raw.count))):3;if(Array.isArray(raw.keys)&&raw.keys.length===6){const used=new Set();s.keys=raw.keys.map(k=>{const v=PREDICT_KEYS.includes(k)?k:'';if(!v||used.has(v))return '';used.add(v);return v;});}return s;}\n"
    "  const SHORTCUT_KEYS=['','Primary+Enter',")
rep("enabledCategories:Array.from({length:15}", "predict:predictDefaults(),enabledCategories:Array.from({length:15}")
rep("    s.actionLayouts=actionLayouts(raw.actionLayouts);\n    return s;",
    "    s.actionLayouts=actionLayouts(raw.actionLayouts);\n    s.predict=predictSettings(raw.predict);\n    return s;")
rep("SHORTCUT_KEYS,shortcutDefaults,shortcutEvent", "SHORTCUT_KEYS,PREDICT_KEYS,predictDefaults,shortcutDefaults,shortcutEvent")

# ---- app: suggestions bar, keys, learning
APP = r"""
/* 0.7.0: word prediction for physical keyboards (Settings -> Access, off by default). The system on-screen keyboards
   have their own prediction, so by default the bar only shows while a physical keyboard is being used. */
const PREDICT_KEY='utac.keryx.predict.v1';let predictStore=null,predictModels=new Map(),predictSaveTimer=0,predictHidden=false,predictLast=[],predictAutoSpace=-1,predictLearned='',predictPhrases={key:'',model:null},predictFailed=new Set();
let keyboardKind=matchMedia('(hover:hover) and (pointer:fine)').matches?'physical':'unknown',lastKeyAt=0;
function predictAll(){if(!predictStore){try{const raw=JSON.parse(localStorage.getItem(PREDICT_KEY)||'{}');predictStore=raw&&typeof raw==='object'&&!Array.isArray(raw)?raw:{};}catch{predictStore={};}}return predictStore;}
function predictModel(lang=prefs().lang){const id=profile().id,key=id+'|'+lang;if(!predictModels.has(key)){const all=predictAll();predictModels.set(key,KeryxPredict.cleanModel(all[id]?.[lang]));}return predictModels.get(key);}
function predictSave(){clearTimeout(predictSaveTimer);predictSaveTimer=setTimeout(()=>{const all=predictAll();for(const [key,m]of predictModels){const [id,lang]=key.split('|');if(!all[id]||typeof all[id]!=='object')all[id]={};all[id][lang]={u:m.u,b:m.b,t:m.t,x:m.x};}try{localStorage.setItem(PREDICT_KEY,JSON.stringify(all));}catch{notify(tr('No s’ha pogut desar el que ha après la predicció.','No se ha podido guardar lo que ha aprendido la predicción.'));}},400);}
function predictUses(value){const P=prefs().predict;return !!value&&P.enabled&&P.keys.includes(value);}
function predictPhraseModel(lang){const texts=profile().phrases.filter(p=>prefs().enabledCategories.includes(p.category)).map(p=>p.texts[lang]||'').filter(Boolean);const key=profile().id+'|'+lang+'|'+texts.length+'|'+texts.reduce((n,t)=>n+t.length,0);if(predictPhrases.key!==key)predictPhrases={key,model:KeryxPredict.phraseModel(lang,texts)};return predictPhrases.model;}
function predictLoad(lang){if(KeryxPredict.ready(lang)||predictFailed.has(lang))return;KeryxPredict.load(lang,'lex/').then(()=>{if(lang===prefs().lang)renderSuggestions();if($('predict-status'))$('predict-status').textContent=predictStatus();}).catch(()=>{predictFailed.add(lang);setTimeout(()=>predictFailed.delete(lang),30000);if($('predict-status'))$('predict-status').textContent=predictStatus();});}
function predictPrefetch(){const p=prefs();if(!p.predict.enabled)return;predictLoad(p.lang);const rest=p.enabledLanguages.filter(l=>l!==p.lang);setTimeout(()=>rest.forEach(predictLoad),3000);}
function predictActive(){const P=prefs().predict;return P.enabled&&(P.when==='always'||keyboardKind==='physical');}
function predictStatus(){const lang=prefs().lang,name=(C.LANGUAGES.find(l=>l[0]===lang)||[,lang])[1];return KeryxPredict.ready(lang)?tr('Diccionari de propostes carregat: ','Diccionario de propuestas cargado: ')+name+'.':predictFailed.has(lang)?tr('No s’ha pogut carregar el diccionari de propostes. Cal connexió la primera vegada.','No se ha podido cargar el diccionario de propuestas. Se necesita conexión la primera vez.'):tr('Carregant el diccionari de propostes…','Cargando el diccionario de propuestas…');}
function predictKeyLabel(v){return !v?tr('Sense tecla','Sin tecla'):v==='Insert'?tr('Inser','Insert'):v;}
function predictLearn(text){const P=prefs().predict;if(!P.enabled||!P.learn||privateMode||conversation().sensitive||!text.trim())return;const lang=prefs().lang,key=profile().id+'|'+lang+'|'+text.trim();if(key===predictLearned)return;predictLearned=key;KeryxPredict.learn(predictModel(lang),lang,text);predictSave();}
function applySuggestion(s){const c=conversation();if(c.start!==c.end||c.start!==s.end){renderSuggestions();return;}const after=c.text[s.end]||'';const space=/\s/.test(after)?'':' ';const r=C.replaceRange(c.text,s.start,s.end,s.value+space);stopTypingFeedback();setMessage(r.text,r.cursor);predictAutoSpace=space?r.cursor:-1;restoreInputFocus();}
function renderSuggestions(){const n=clear($('suggestions'));predictLast=[];if(composing){n.hidden=true;return;}const c=conversation(),P=prefs().predict;
 const abbr=C.suggestion(c.text,c.start,prefs().lang,[],profile().abbreviations,false);let words=[];
 if(predictActive()&&!predictHidden&&c.start===c.end){const lang=prefs().lang;if(KeryxPredict.ready(lang)){try{words=KeryxPredict.suggest({text:c.text,cursor:c.start,lang,model:predictModel(lang),phrases:predictPhraseModel(lang),count:P.count});}catch{words=[];}}else predictLoad(lang);}
 const list=[...abbr,...words.filter(w=>!abbr.some(a=>a.value===w.value))].slice(0,P.enabled?P.count:3);n.hidden=!list.length;n.classList.toggle('predicting',P.enabled);if(!list.length)return;predictLast=list;
 list.forEach((s,i)=>{const b=button(s.label,()=>applySuggestion(s),'');b.dataset.edit='true';b.title=s.kind==='abbreviation'?tr('Expandir abreviatura','Expandir abreviatura'):tr('Completar paraula','Completar palabra');
  if(P.enabled){const keys=[i===0?P.keys[0]:'',P.keys[i+1]].filter(Boolean);if(keys.length){b.prepend(...keys.map(k=>el('kbd',{'aria-hidden':'true'},predictKeyLabel(k))));b.setAttribute('aria-keyshortcuts',keys.join(' '));}}
  n.append(b);});}
const PREDICT_PUNCT=/^[,.;:!?)»…]$/u;
$('message').addEventListener('keydown',e=>{
 lastKeyAt=performance.now();
 if(e.isTrusted&&(e.keyCode===229||e.key==='Unidentified')){if(keyboardKind!=='soft'){keyboardKind='soft';renderSuggestions();}}
 else if(e.isTrusted&&typeof e.key==='string'&&e.key.length===1&&!e.ctrlKey&&!e.metaKey&&!softKeyboardLikely()){if(keyboardKind!=='physical'){keyboardKind='physical';}}
 if(e.isComposing||composing)return;
 if(e.key==='Escape'){if(predictLast.length&&!$('suggestions').hidden){predictHidden=true;renderSuggestions();}return;}
 const P=prefs().predict;if(!P.enabled||!predictLast.length||$('suggestions').hidden||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
 let i=-1;if(P.keys[0]&&e.key===P.keys[0])i=0;else{const k=P.keys.indexOf(e.key,1);if(k>0)i=k-1;}
 if(i<0||i>=predictLast.length)return;e.preventDefault();e.stopPropagation();if(e.repeat)return;keyboardInput=true;applySuggestion(predictLast[i]);
},true);
/* After an inserted word, a typed punctuation mark takes the place of the space that came with it (French keeps its space before ; : ! ?). */
$('message').addEventListener('beforeinput',e=>{const n=$('message');if(e.inputType==='insertText'&&performance.now()-lastKeyAt>80&&keyboardKind!=='soft'&&matchMedia('(any-pointer:coarse)').matches){keyboardKind='soft';}
 if(predictAutoSpace>=0&&e.inputType==='insertText'&&typeof e.data==='string'&&PREDICT_PUNCT.test(e.data)&&!(prefs().lang==='fr'&&/[;:!?»]/.test(e.data))&&n.selectionStart===n.selectionEnd&&n.selectionStart===predictAutoSpace&&n.value[predictAutoSpace-1]===' '){n.setRangeText('',predictAutoSpace-1,predictAutoSpace,'end');}
 predictAutoSpace=-1;},true);
$('message').addEventListener('input',()=>{predictHidden=false;});
let predictCaret=-1;for(const type of ['keyup','click','select'])$('message').addEventListener(type,()=>{const c=conversation();const k=c.start*100003+c.end;if(k!==predictCaret){predictCaret=k;if(type!=='keyup'||!$('suggestions').hidden||prefs().predict.enabled)renderSuggestions();}});
function predictSettingsSection(){const p=prefs(),P=p.predict;const box=el('div',{class:'predict-settings',id:'predict-settings'});const redraw=()=>{persist();renderSuggestions();const y=$('dialog-body')?.scrollTop||0;settingsDialog('access');requestAnimationFrame(()=>{if($('dialog-body'))$('dialog-body').scrollTop=y;});};
 box.append(el('h3',{},tr('Predicció de text','Predicción de texto')),check(tr('Predicció de text amb teclat físic','Predicción de texto con teclado físico'),P.enabled,v=>{P.enabled=v;if(v){for(let i=0;i<6;i++)if(P.keys[i]&&p.shortcutsEnabled&&Object.values(p.shortcuts).includes(P.keys[i]))P.keys[i]='';predictPrefetch();}redraw();},tr('Mostra propostes de paraules sota el missatge mentre escrius. Els teclats en pantalla del sistema ja porten la seva pròpia predicció.','Muestra propuestas de palabras debajo del mensaje mientras escribes. Los teclados en pantalla del sistema ya llevan su propia predicción.')));
 if(!P.enabled){content_note(box);return box;}
 box.append(field(tr('Quan es mostren les propostes','Cuándo se muestran las propuestas'),selectControl([['physical',tr('Només quan escric amb un teclat físic','Solo cuando escribo con un teclado físico')],['always',tr('Sempre, també amb el teclat en pantalla','Siempre, también con el teclado en pantalla')]],P.when,v=>{P.when=v;persist();renderSuggestions();}),tr('Keryx ho dedueix de les tecles que rep. Si no encerta, tria «Sempre».','Keryx lo deduce de las teclas que recibe. Si no acierta, elige «Siempre».')),
  field(tr('Nombre de propostes','Número de propuestas'),selectControl([1,2,3,4,5].map(n=>[String(n),String(n)]),String(P.count),v=>{P.count=Number(v);redraw();}),tr('Poques propostes es llegeixen més de pressa.','Pocas propuestas se leen más deprisa.')));
 const keyRow=el('div',{class:'predict-keys'});const labels=[[tr('Inserir la primera proposta','Insertar la primera propuesta')],...[1,2,3,4,5].map(i=>[tr('Proposta ','Propuesta ')+i])];
 const error=el('p',{class:'error-text',role:'alert'});
 labels.forEach(([label],slot)=>{if(slot>P.count)return;const sel=selectControl(C.PREDICT_KEYS.map(v=>[v,predictKeyLabel(v)]),P.keys[slot],v=>{if(v&&p.shortcutsEnabled&&Object.values(p.shortcuts).includes(v)){sel.value=P.keys[slot];error.textContent=tr('Aquesta tecla ja és una drecera del perfil.','Esta tecla ya es un atajo del perfil.');return;}error.textContent='';const other=P.keys.indexOf(v);if(v&&other>=0&&other!==slot)P.keys[other]='';P.keys[slot]=v;redraw();});
  for(const o of sel.options)if(o.value&&p.shortcutsEnabled&&Object.values(p.shortcuts).includes(o.value))o.disabled=true;sel.id='predict-key-'+slot;keyRow.append(field(label,sel));});
 box.append(el('h4',{},tr('Tecles per triar les propostes','Teclas para elegir las propuestas')),keyRow,error,el('p',{class:'notice'},tr('Cada tecla insereix la proposta d’una sola pulsació, seguida d’un espai. Esc amaga les propostes fins que tornes a escriure. Les tecles F poden requerir Fn en alguns teclats; F11 queda reservada al navegador.','Cada tecla inserta la propuesta de una sola pulsación, seguida de un espacio. Esc oculta las propuestas hasta que vuelves a escribir. Las teclas F pueden requerir Fn en algunos teclados; F11 queda reservada al navegador.')),
  button(tr('Restablir les tecles inicials','Restablecer las teclas iniciales'),()=>{P.keys=C.predictDefaults().keys;for(let i=0;i<6;i++)if(p.shortcutsEnabled&&Object.values(p.shortcuts).includes(P.keys[i]))P.keys[i]='';redraw();}));
 box.append(check(tr('Aprendre dels missatges que faig parlar','Aprender de los mensajes que hago hablar'),P.learn,v=>{P.learn=v;persist();},tr('Només en aquest dispositiu i en aquest perfil. No aprèn en mode privat. Una paraula nova es proposa després de fer-la servir dues vegades.','Solo en este dispositivo y en este perfil. No aprende en modo privado. Una palabra nueva se propone después de usarla dos veces.')),
  el('div',{class:'button-row'},button(tr('Paraules apreses','Palabras aprendidas'),()=>learnedWordsDialog(),'soft'),button(tr('Esborrar el que ha après','Borrar lo que ha aprendido'),()=>confirmDialog(tr('Esborrar el que ha après','Borrar lo que ha aprendido'),tr('S’esborraran les paraules i les combinacions apreses en aquest perfil, en totes les llengües. Les frases desades no canvien.','Se borrarán las palabras y las combinaciones aprendidas en este perfil, en todos los idiomas. Las frases guardadas no cambian.'),()=>{const id=profile().id;for(const k of [...predictModels.keys()])if(k.startsWith(id+'|'))predictModels.delete(k);delete predictAll()[id];try{localStorage.setItem(PREDICT_KEY,JSON.stringify(predictAll()));}catch{}notify(tr('Aprenentatge esborrat.','Aprendizaje borrado.'));settingsDialog('access');},()=>settingsDialog('access')),'danger')),
  el('p',{class:'notice',id:'predict-status',role:'status'},predictStatus()));predictLoad(p.lang);
 return box;
 function content_note(b){b.append(el('p',{class:'notice'},tr('Desactivada. Les abreviatures personals continuen funcionant.','Desactivada. Las abreviaturas personales siguen funcionando.')));}
}
function learnedWordsDialog(){const lang=prefs().lang,m=predictModel(lang),list=KeryxPredict.learned(m).slice(0,300);const back=()=>settingsDialog('access');
 const body=[el('p',{class:'notice'},tr('Paraules apreses en aquest perfil per a la llengua actual. «Oblidar» l’esborra i fa que no es torni a proposar.','Palabras aprendidas en este perfil para el idioma actual. «Olvidar» la borra y hace que no se vuelva a proponer.'))];
 if(!list.length)body.push(el('p',{class:'prose'},tr('Encara no ha après cap paraula. Aprèn dels missatges que fas parlar.','Todavía no ha aprendido ninguna palabra. Aprende de los mensajes que haces hablar.')));
 for(const w of list)body.push(el('div',{class:'mini-card'},el('span',{},w.word+' · '+w.uses),button(tr('Oblidar','Olvidar'),()=>{KeryxPredict.forget(m,w.key);predictSave();learnedWordsDialog();},'danger')));
 if(m.x.length)body.push(el('h4',{},tr('Paraules oblidades','Palabras olvidadas')),...m.x.map(w=>el('div',{class:'mini-card'},el('span',{},w),button(tr('Tornar a proposar','Volver a proponer'),()=>{KeryxPredict.unforget(m,w);predictSave();learnedWordsDialog();}))));
 openDialog(tr('Paraules apreses','Palabras aprendidas'),body,[button(tr('Tornar','Volver'),back,'primary')],'scroll-dialog');dialogBack=back;}
"""
i = s.index("function renderSuggestions(){")
j = s.index("\n", i)
s = s[:i] + APP.strip('\n') + s[j:]

# learning when the message is spoken (Parlar)
rep("prefs().readScope==='last'){text=(text.match(/[^.!?\\n]+[.!?]?/gu)||[]).pop()||text;}speakText(text,prefs().lang,false);}",
    "prefs().readScope==='last'){text=(text.match(/[^.!?\\n]+[.!?]?/gu)||[]).pop()||text;}predictLearn(text);speakText(text,prefs().lang,false);}")

# settings: Access gets the prediction section; Writing loses the old phrase-bank completion
rep("content.append(button(tr('Aplicar i provar l’accés','Aplicar y probar el acceso')",
    "content.append(predictSettingsSection());\n content.append(button(tr('Aplicar i provar l’accés','Aplicar y probar el acceso')")
i = s.index("check(tr('Completar paraules del meu banc de frases'")
j = s.index("el('div',{class:'setting-section'},el('h3',{},tr('Abreviatures personals'", i)
s = s[:i] + s[j:]

# profile shortcuts cannot take a key that the prediction uses
rep("C.shortcutConflict(option.value,p.shortcuts,id,p.access,p.selectKey,p.nextKey)",
    "(C.shortcutConflict(option.value,p.shortcuts,id,p.access,p.selectKey,p.nextKey)||predictUses(option.value))")
rep("const problem=C.shortcutConflict(value,p.shortcuts,id,p.access,p.selectKey,p.nextKey);",
    "const problem=C.shortcutConflict(value,p.shortcuts,id,p.access,p.selectKey,p.nextKey)||(predictUses(value)?'prediction':'');")

# load the lexicon at start and when the language changes
rep("renderAll();refreshVoices();if(matchMedia", "renderAll();predictPrefetch();refreshVoices();if(matchMedia")

# keyboard manual
rep("section(themeText(['Temes de color'",
    "section(tr('9. Predicció de text','9. Predicción de texto'),tr('Si actives la predicció a Ajustos → Accés, sota el missatge apareixen propostes numerades: la paraula que estàs escrivint o la següent. Tab insereix la primera i F1, F2, F3, F4 i F5 insereixen cadascuna, d’una sola pulsació i amb un espai al darrere. Si després escrius un signe de puntuació, ocupa el lloc d’aquest espai. Esc amaga les propostes fins que tornes a escriure. Les tecles es poden canviar.','Si activas la predicción en Ajustes → Acceso, debajo del mensaje aparecen propuestas numeradas: la palabra que estás escribiendo o la siguiente. Tab inserta la primera y F1, F2, F3, F4 y F5 insertan cada una, de una sola pulsación y con un espacio detrás. Si después escribes un signo de puntuación, ocupa el lugar de ese espacio. Esc oculta las propuestas hasta que vuelves a escribir. Las teclas se pueden cambiar.')),\n section(themeText(['Temes de color'")

# Information: no portable edition; scope text; sources, licences and references
i = s.index("if(location.protocol!=='file:')content.append(el('h3',{},tr('Versió portàtil'")
j = s.index("\n", i)
s = s[:i] + s[j+1:]
OLD_SCOPE_CA = "Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges bilingües editables, categories, favorits, documents, perfils, còpies i una primera implementació de la permanència. L’escriptura es fa sempre amb el teclat físic o el teclat en pantalla del sistema. La compleció opcional es limita a les paraules del banc de frases."
OLD_SCOPE_ES = "Incluye el editor, voz del navegador y voces descargables, presentación de texto, 90 mensajes bilingües editables, categorías, favoritos, documentos, perfiles, copias y una primera implementación de la permanencia. La escritura se hace siempre con el teclado físico o el teclado en pantalla del sistema. La compleción opcional se limita a las palabras del banco de frases."
SCOPE_CA = "Inclou l’editor, la veu del navegador i veus descarregables, la presentació del text, 90 missatges bilingües editables, categories, favorits, documents, perfils, còpies i una primera implementació de la permanència. L’escriptura es fa sempre amb el teclat físic o el teclat en pantalla del sistema. Amb teclat físic, la predicció de text opcional proposa paraules en les sis llengües i aprèn dels missatges que fas parlar."
SCOPE_ES = "Incluye el editor, voz del navegador y voces descargables, presentación de texto, 90 mensajes bilingües editables, categorías, favoritos, documentos, perfiles, copias y una primera implementación de la permanencia. La escritura se hace siempre con el teclado físico o el teclado en pantalla del sistema. Con teclado físico, la predicción de texto opcional propone palabras en los seis idiomas y aprende de los mensajes que haces hablar."
rep("tr('" + OLD_SCOPE_CA + "','" + OLD_SCOPE_ES + "')", "tr('" + SCOPE_CA + "','" + SCOPE_ES + "')")
i = s.index("el('p',{},tr('Encara pendents: serveis de veu addicionals, enregistraments, predicció lingüística completa, plantilles i sincronització.")
j = s.index("')),", i) + 4
PEND_CA = "Encara pendents: serveis de veu addicionals, enregistraments, plantilles i sincronització. La predicció de text en basc i gallec encara no proposa la paraula següent fins que aprèn dels missatges. No s’ha validat clínicament ni amb persones usuàries. Cal provar l’accés i la veu amb el dispositiu real abans de confiar-hi per a l’ús quotidià."
PEND_ES = "Todavía pendientes: servicios de voz adicionales, grabaciones, plantillas y sincronización. La predicción de texto en euskera y gallego todavía no propone la palabra siguiente hasta que aprende de los mensajes. No se ha validado clínicamente ni con personas usuarias. Hay que probar el acceso y la voz con el dispositivo real antes de confiar en ello para el uso cotidiano."
s = s[:i] + "el('p',{},tr('" + PEND_CA + "','" + PEND_ES + "'))," + s[j:]
rep("const TOOLS=[",
    "const TOOLS=[[tr('Predicció de text','Predicción de texto'),'wordfreq 3.1 (ca, es, en, fr)','Robyn Speer · CC BY-SA 4.0','https://github.com/rspeer/wordfreq'],[tr('Predicció de text','Predicción de texto'),'FrequencyWords 2018 (eu, gl)','Hermit Dave · OpenSubtitles · CC BY-SA 4.0','https://github.com/hermitdave/FrequencyWords'],[tr('Predicció de text','Predicción de texto'),'Universal Dependencies: Catalan-AnCora, Spanish-AnCora, English-EWT, French-Rhapsodie, French-ParisStories','CC BY 4.0 · CC BY-SA 4.0','https://universaldependencies.org/'],")
rep("content.append(el('h3',{},tr('Referències','Referencias')));",
    "content.append(el('p',{},tr('Els diccionaris de la predicció de text (carpeta lex/) es distribueixen amb la llicència CC BY-SA 4.0, compatible amb la GPL 3.0. Les seves fonts són a «Eines i recursos».','Los diccionarios de la predicción de texto (carpeta lex/) se distribuyen con la licencia CC BY-SA 4.0, compatible con la GPL 3.0. Sus fuentes están en «Herramientas y recursos».')));\n content.append(el('h3',{},tr('Referències','Referencias')));")
NEWREFS = [
 ["Koester, H. H., & Levine, S. P. (1994). Modeling the speed of text entry with a word prediction interface. IEEE Transactions on Rehabilitation Engineering, 2(3), 177–187.", "https://doi.org/10.1109/86.331567"],
 ["Kuhn, R., & De Mori, R. (1990). A cache-based natural language model for speech recognition. IEEE Transactions on Pattern Analysis and Machine Intelligence, 12(6), 570–583.", "https://doi.org/10.1109/34.56193"],
 ["Lison, P., & Tiedemann, J. (2016). OpenSubtitles2016: Extracting large parallel corpora from movie and TV subtitles. A Proceedings of LREC 2016 (pp. 923–929). ELRA.", None],
 ["Nivre, J., de Marneffe, M.-C., Ginter, F., Hajič, J., Manning, C. D., Pyysalo, S., Schuster, S., Tyers, F., & Zeman, D. (2020). Universal Dependencies v2: An evergrowing multilingual treebank collection. A Proceedings of LREC 2020 (pp. 4034–4043). ELRA.", "https://aclanthology.org/2020.lrec-1.497/"],
 ["Speer, R. (2022). rspeer/wordfreq: v3.0 (versió 3.0.2) [Programari]. Zenodo.", "https://doi.org/10.5281/zenodo.7199437"],
 ["Trnka, K., McCaw, J., Yarrington, D., McCoy, K. F., & Pennington, C. (2009). User interaction with word prediction: The effects of prediction quality. ACM Transactions on Accessible Computing, 1(3), Article 17.", "https://doi.org/10.1145/1497302.1497307"],
]
rep("refs.forEach(([text,url])",
    "refs.push(..." + json.dumps(NEWREFS, ensure_ascii=False) + ");refs.sort((a,b)=>a[0].localeCompare(b[0],'ca'));refs.forEach(([text,url])")

# style: key labels inside the suggestion buttons
rep(".suggestions button span{white-space:nowrap;text-overflow:ellipsis;overflow:hidden}",
    ".suggestions button span{white-space:nowrap;text-overflow:ellipsis;overflow:hidden}.suggestions button kbd{font:600 11px/1 var(--ui-font,inherit);padding:3px 5px;border-radius:5px;border:1px solid var(--line,currentColor);background:var(--surface,transparent);opacity:.8;margin-right:6px;flex-shrink:0}.suggestions.predicting button{font-size:17px;min-height:38px}.predict-keys{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}")

# ---- translations (eu, gl, en, fr)
T = json.load(open(os.path.join(HERE, 'translations.json'), encoding='utf-8'))
T[SCOPE_CA] = T.pop('@scope'); T[PEND_CA] = T.pop('@pending')
i = s.index('const KeryxI18n=(()=>{const dictionaries=') + len('const KeryxI18n=(()=>{const dictionaries=')
for li, lang in enumerate(['eu', 'gl', 'en', 'fr']):
    key = '"' + lang + '":{'; k = s.index(key, i) + len(key)
    s = s[:k] + ''.join(json.dumps(ca, ensure_ascii=False) + ':' + json.dumps(v[li], ensure_ascii=False) + ',' for ca, v in T.items()) + s[k:]
open(dst, 'w', encoding='utf-8', newline='').write(s)
print('ok', dst)

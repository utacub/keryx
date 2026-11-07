# Applies the UTAC Keryx 0.6.1 changes to the built UTAC_Keryx_v0.6.0_local.html.
# Usage: python3 patch061.py UTAC_Keryx_v0.6.0_local.html UTAC_Keryx_v0.6.1_local.html
# GPL-3.0-or-later.
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:60],n); s=s.replace(a,b)
s=s.replace('0.6.0','0.6.1')
# --- translations for new strings
T={'eu':{"Mostrar panell":"Erakutsi panela","Amagar panell":"Ezkutatu panela","Línia amunt":"Lerro bat gora","Línia avall":"Lerro bat behera","Teclat físic detectat: el panell inferior s’ha amagat.":"Teklatu fisikoa hauteman da: beheko panela ezkutatu da."},
   'gl':{"Mostrar panell":"Mostrar panel","Amagar panell":"Ocultar panel","Línia amunt":"Liña arriba","Línia avall":"Liña abaixo","Teclat físic detectat: el panell inferior s’ha amagat.":"Detectouse un teclado físico: o panel inferior ocultouse."},
   'en':{"Mostrar panell":"Show panel","Amagar panell":"Hide panel","Línia amunt":"Line up","Línia avall":"Line down","Teclat físic detectat: el panell inferior s’ha amagat.":"Physical keyboard detected: the lower panel has been hidden."},
   'fr':{"Mostrar panell":"Afficher le panneau","Amagar panell":"Masquer le panneau","Línia amunt":"Ligne précédente","Línia avall":"Ligne suivante","Teclat físic detectat: el panell inferior s’ha amagat.":"Clavier physique détecté : le panneau inférieur a été masqué."}}
import json
for lang,d in T.items():
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False)+',' for k,v in d.items())
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')
# --- panel state
rep("let panelOpen=true,listPage=0,historyPage=0;","let panelOpen=true,panelUserChoice=false,listPage=0,historyPage=0;")
rep("function setPanelOpen(open){panelOpen=open;","function setPanelOpen(open){panelOpen=open;panelUserChoice=true;")
rep("$('workspace').classList.toggle('panel-closed',!panelOpen);","$('workspace').classList.toggle('panel-closed',!panelOpen);$('main').dataset.view=panelOpen?activeView:'closed';")
rep('<button id="toggle-panel" class="icon-only flat"></button>','<button id="toggle-panel" class="panel-toggle" type="button"></button>')
rep("toggle.append(icon('down'));","toggle.append(icon('down'),el('span',{class:'toggle-label'},tr('Amagar panell','Ocultar panel')));")
rep("restore.append(icon('down'),el('span',{},tr('Desplegar el panell inferior','Desplegar el panel inferior')));",
    "restore.append(el('span',{class:'restore-pill'},icon('down'),el('span',{class:'toggle-label'},tr('Mostrar panell','Mostrar panel'))));restore.setAttribute('aria-label',tr('Desplegar el panell inferior','Desplegar el panel inferior'));restore.title=restore.getAttribute('aria-label');")
# --- more phrases per page on narrow panels
rep("function gridCapacity(n,minHeight=78){const width=n.clientWidth||700,height=n.clientHeight||200;const cols=width>=850?3:width>=430?2:1;const rows=Math.max(1,Math.min(4,Math.floor((height+9)/(minHeight*prefs().controlSize+9))));",
    "function gridCapacity(n,minHeight=78){const width=n.clientWidth||700,height=n.clientHeight||200;const cols=width>=850?3:width>=260?2:1;if(width<600||height<260)minHeight=Math.min(minHeight,50);const rows=Math.max(1,Math.min(5,Math.floor((height+9)/(minHeight*prefs().controlSize+9))));")
# --- message fit + line buttons
rep("n.append(el('span',{class:'spacer'}));",
    "n.append(el('span',{class:'spacer'}));\n {const up=add(tr('Línia amunt','Línea arriba'),()=>scrollMessageLine(-1),'down','line-up');up.setAttribute('aria-label',tr('Línia amunt','Línea arriba'));up.hidden=true;const dn=add(tr('Línia avall','Línea abajo'),()=>scrollMessageLine(1),'down','line-down');dn.setAttribute('aria-label',tr('Línia avall','Línea abajo'));dn.hidden=true;}")
rep("if($('repeat'))$('repeat').disabled=!c.last;renderSuggestions();}",
    "if($('repeat'))$('repeat').disabled=!c.last;renderSuggestions();scheduleFitMessage();}\n"
    "/* 0.6.1: the message box never grows. The type shrinks to MESSAGE_MIN px so the whole text fits; beyond that, line buttons move through it. */\n"
    "const MESSAGE_MIN=20;let fitFrame=0;function scheduleFitMessage(){cancelAnimationFrame(fitFrame);fitFrame=requestAnimationFrame(fitMessage);}\n"
    "function fitMessage(){const m=$('message');if(!m||!m.clientHeight)return;m.style.fontSize='';const base=parseFloat(getComputedStyle(m).fontSize)||30,min=Math.min(base,MESSAGE_MIN);let size=base;while(size>min&&m.scrollHeight>m.clientHeight+1){size=Math.max(min,size-2);m.style.fontSize=size+'px';}updateLineButtons();}\n"
    "function updateLineButtons(){const m=$('message'),up=$('line-up'),dn=$('line-down');if(!m||!up||!dn)return;const over=m.scrollHeight>m.clientHeight+1;m.classList.toggle('overflowing',over);if(up.hidden===over){up.hidden=dn.hidden=!over;}up.disabled=m.scrollTop<=0;dn.disabled=m.scrollTop+m.clientHeight>=m.scrollHeight-1;}\n"
    "function scrollMessageLine(d){const m=$('message'),lh=parseFloat(getComputedStyle(m).lineHeight)||parseFloat(getComputedStyle(m).fontSize)*1.35;m.scrollTop=Math.max(0,m.scrollTop+d*lh);updateLineButtons();}")
rep("$('message').addEventListener('input',handleMessageInput);","$('message').addEventListener('input',handleMessageInput);$('message').addEventListener('scroll',()=>updateLineButtons(),{passive:true});")
rep("if($('dialog').open)reflowDialog();});","if($('dialog').open)reflowDialog();placeCompactControls();fitMessage();});")
rep("layoutObserver.observe($('dialog-body'));","layoutObserver.observe($('dialog-body'));layoutObserver.observe($('message'));")

# --- quick replies paginate when the panel is low
rep("let panelOpen=true,panelUserChoice=false,listPage=0,historyPage=0;","let panelOpen=true,panelUserChoice=false,listPage=0,historyPage=0,quickPage=0;")
rep(" for(const p of list){const text=phraseText(p),b=button(text,()=>speakText(text,prefs().lang,true),'quick');",
    " const qw=n.clientWidth||700,qh=n.clientHeight||200,qcols=qw>=700?4:2,qrows=Math.max(1,Math.min(Math.ceil(list.length/qcols)||1,Math.floor((qh+6)/(50*prefs().controlSize+6)))),qsize=qcols*qrows,qcount=Math.max(1,Math.ceil(list.length/qsize));quickPage=Math.max(0,Math.min(quickPage,qcount-1));n.style.gridTemplateColumns='repeat('+qcols+',minmax(0,1fr))';n.style.gridTemplateRows='repeat('+qrows+',minmax(0,1fr))';n.dataset.page=quickPage;\n"
    " const qp=$('quick-pager');if(qp){qp.hidden=qcount<2;if(qcount>1)drawPager(qp,quickPage,qcount,null,page=>{quickPage=page;renderQuick();resetAccess();});else clear(qp);}\n"
    " list.forEach((p,i)=>{if(i<quickPage*qsize||i>=(quickPage+1)*qsize)return;const text=phraseText(p),b=button(text,()=>speakText(text,prefs().lang,true),'quick'+(i<2?' lead':' plain'));")
rep("el('div',{id:'quick-grid',class:'quick-grid','data-scan-group':'quick'}));renderQuick();return;}",
    "el('div',{id:'quick-grid',class:'quick-grid','data-scan-group':'quick'}),el('div',{id:'quick-pager',class:'pager','data-scan-group':'quick-pages',hidden:true}));renderQuick();requestAnimationFrame(()=>{if($('quick-grid'))renderQuick();});return;}")
rep("if($('phrase-grid'))renderPhraseGrid();if($('history-grid'))renderHistoryPage();","if($('phrase-grid'))renderPhraseGrid();if($('history-grid'))renderHistoryPage();if($('quick-grid'))renderQuick();")
rep("b.dataset.focusKey='quick:'+p.id;b.setAttribute('aria-label',tr('Dir: ','Decir: ')+text);n.append(b);}","b.dataset.focusKey='quick:'+p.id;b.setAttribute('aria-label',tr('Dir: ','Decir: ')+text);n.append(b);});")

# --- physical keyboard + compact controls
rep("renderAll();refreshVoices();if(firstUse)welcome();",
    "/* 0.6.1: very low windows (phones in landscape, text zoom at 200 %) move the footer buttons up, so no row is cut. */\n"
    "function placeCompactControls(){const compact=matchMedia('(max-height:520px), (max-width:600px)').matches,top=document.querySelector('.status-top'),foot=document.querySelector('.footer');for(const id of ['silent-button','private-button']){const b=$(id),target=compact?top:foot;if(b&&target&&b.parentNode!==target)target.append(b);}}\n"
    "/* 0.6.1: with a physical keyboard the lower panel starts hidden. There is no web API that reports a keyboard, so two signs are used: a mouse or trackpad as the main pointer, or real key presses in the message while no on-screen keyboard is taking up the screen. A choice made by the person always wins. */\n"
    "function softKeyboardLikely(){if(!matchMedia('(any-pointer:coarse)').matches)return false;const vv=window.visualViewport?.height||innerHeight,full=matchMedia('(orientation:landscape)').matches?Math.min(screen.width,screen.height):Math.max(screen.width,screen.height);return vv<full*0.7;}\n"
    "function hidePanelForPhysicalKeyboard(announce){if(panelUserChoice||!panelOpen||prefs().access!=='direct')return;panelOpen=false;renderWorkspace();resetAccess();if(announce)notify(tr('Teclat físic detectat: el panell inferior s’ha amagat.','Teclado físico detectado: el panel inferior se ha ocultado.'));}\n"
    "document.addEventListener('keydown',e=>{if(!e.isTrusted||e.ctrlKey||e.metaKey||e.altKey||e.isComposing||e.keyCode===229||typeof e.key!=='string'||e.key.length!==1||e.target!==$('message')||softKeyboardLikely())return;hidePanelForPhysicalKeyboard(true);},true);\n"
    "renderAll();refreshVoices();if(matchMedia('(hover:hover) and (pointer:fine)').matches)hidePanelForPhysicalKeyboard(false);placeCompactControls();scheduleFitMessage();if(firstUse)welcome();")
CSS = r"""
/* 0.6.1 — light minimized panel, high-contrast panel toggle, fixed screen at 200 % text zoom and on small phones. */
.workspace.panel-closed{background:var(--surface);border:1px solid var(--border)}
.panel-restore,.panel-restore:hover{background:var(--surface);color:var(--text);padding:3px 10px}
.restore-pill{display:inline-flex;align-items:center;gap:8px;min-height:34px;padding:5px 18px;border-radius:999px;background:var(--primary);color:var(--primaryText);border:2px solid var(--primary);font-weight:700;font-size:14px;box-shadow:0 1px 3px #0003}
.restore-pill .icon{width:20px;height:20px}
.panel-restore:hover .restore-pill{filter:brightness(1.12)}
.panel-restore:focus-visible{outline:0}.panel-restore:focus-visible .restore-pill{outline:3px solid var(--focus);outline-offset:2px}
.workspace-header>.panel-toggle,.panel-toggle{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:40px;min-width:44px;padding:5px 12px;border-radius:10px;border:2px solid var(--primary);background:var(--primary);color:var(--primaryText);font-weight:700;font-size:13px;white-space:nowrap}
.panel-toggle .icon{width:22px;height:22px}
.panel-toggle:hover{filter:brightness(1.12)}
@media(max-width:1000px){.panel-toggle .toggle-label{display:none}.workspace-header>.panel-toggle{padding:4px 8px;min-width:44px}}
.text-tools #line-up .icon{transform:rotate(180deg)}
@media(max-width:700px){.text-tools #line-up span,.text-tools #line-down span{display:none}}
#message{overflow-y:hidden}
#message.overflowing{overflow-y:auto}
@media(max-width:600px){
 .main[data-view=phrases],.main[data-view=favorites],.main[data-view=history]{grid-template-rows:24px minmax(118px,.55fr) 24px minmax(0,1.45fr) 36px}
 .workspace-header{height:50px}
 .main[data-view=phrases] .library-controls,.main[data-view=favorites] .library-controls{gap:4px}
}
@media(max-height:520px){
 body{grid-template-rows:44px minmax(0,1fr)}
 .header-inner{padding:3px 12px}.brand{height:30px;width:150px}
 .header-inner button,.lang-btn{min-height:34px}
 .main,.main.panel-collapsed{padding:4px 10px 6px;gap:4px;grid-template-rows:26px minmax(110px,.9fr) 18px minmax(0,1.1fr)}
 .main[data-view=keyboard]{grid-template-rows:26px minmax(100px,.6fr) 18px minmax(0,1.4fr)}
 .main[data-view=phrases],.main[data-view=favorites],.main[data-view=history]{grid-template-rows:26px minmax(104px,.65fr) 18px minmax(0,1.35fr)}
 .main.panel-collapsed,.main[data-view=closed]{grid-template-rows:26px minmax(110px,1fr) 18px 40px}
 .footer{display:none}
 .status-top .eyebrow,.status-top #profile-name,.status-top .subdued{display:none}
 .status-top button{min-height:24px}
 .composer-head{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
 .composer{position:relative}
 #message{padding-top:4px}
 .text-tools{min-height:26px}.text-tools button{min-height:26px}
 .composer-actions{padding:4px 7px;gap:5px}.composer-actions button{height:38px;min-height:36px}
 .composer-actions kbd{display:none}
 .voice-line{font-size:11px}
 .workspace-header{height:42px;min-height:40px;padding:3px 8px}
 .tabs button{min-height:34px}
 .workspace-body{padding:5px 8px;gap:5px}
 .quick-grid{gap:5px}.quick{padding:3px 8px}.quick>span{-webkit-line-clamp:2}
 .panel-toolbar{min-height:26px}.panel-toolbar p{display:none}
 .pager{min-height:30px}.pager button{min-height:28px}
 .panel-toggle,.workspace-header>.panel-toggle{min-height:34px}
}
@media(max-height:520px) and (max-width:700px){.composer-actions button{font-size:13px;gap:3px;padding:3px}.composer-actions .speak{font-size:15px}.composer-actions .icon{width:16px;height:16px}}
"""
import os
CSS+=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"css_add.css"),encoding="utf-8").read()
rep("</style>",CSS+"</style>")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',len(s))

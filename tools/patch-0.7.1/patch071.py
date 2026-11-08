# Applies the UTAC Keryx 0.7.1 change to index.html of 0.7.0 (Marc, 2026-11-08):
# Silenci and Mode privat move from the footer into the main message button grid (icon-only, with hover labels),
# and Silenci always shows the muted-speaker icon (highlighted when active).
# Saved button layouts get the two new buttons in their first free cells; if a layout has no room (or hides them),
# they stay in the footer, so they can always be reached.
# Usage: python3 patch071.py index.html index.html.new
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.7\.0(?![:\d])','0.7.1',s)

# Buttons and default layouts
rep("['more','more-tools','tools'],['new','new-message','new']];",
    "['more','more-tools','tools'],['new','new-message','new'],['silent','silent-button','silent'],['private','private-button','lock']];")
rep("undo:[0,4,1,1,1],redo:[1,4,1,1,1],new:[2,4,1,1,1]},bottom:{speak:[0,0,3,1,1],stop:[3,0,1,1,1],show:[4,0,1,1,1],word:[5,0,1,1,1],clear:[6,0,1,1,1],undo:[7,0,1,1,1],redo:[8,0,1,1,1],save:[9,0,1,1,1],more:[10,0,1,1,1],new:[11,0,1,1,1]}};",
    "undo:[0,4,1,1,1],redo:[1,4,1,1,1],new:[2,4,1,1,1],silent:[0,5,1,1,1],private:[1,5,1,1,1]},bottom:{speak:[0,0,3,2,1],stop:[3,0,1,1,1],show:[4,0,1,1,1],word:[5,0,1,1,1],clear:[6,0,1,1,1],undo:[7,0,1,1,1],redo:[8,0,1,1,1],save:[9,0,1,1,1],more:[10,0,1,1,1],new:[11,0,1,1,1],silent:[3,1,4,1,1],private:[7,1,5,1,1]}};")
rep("const ACTION_NARROW_BOTTOM={speak:[0,0,4,1,1],stop:[4,0,2,1,1],show:[6,0,2,1,1],save:[8,0,2,1,1],more:[10,0,2,1,1],word:[0,1,2,1,1],clear:[2,1,2,1,1],undo:[4,1,2,1,1],redo:[6,1,2,1,1],new:[8,1,4,1,1]};",
    "const ACTION_NARROW_BOTTOM={speak:[0,0,2,1,1],stop:[2,0,2,1,1],show:[4,0,2,1,1],save:[6,0,2,1,1],more:[8,0,2,1,1],silent:[10,0,2,1,1],word:[0,1,2,1,1],clear:[2,1,2,1,1],undo:[4,1,2,1,1],redo:[6,1,2,1,1],new:[8,1,2,1,1],private:[10,1,2,1,1]};")
rep("more:tr('Més eines','Más herramientas'),new:tr('Nou missatge','Nuevo mensaje')}[k];}",
    "more:tr('Més eines','Más herramientas'),new:tr('Nou missatge','Nuevo mensaje'),silent:tr('Silenci','Silencio'),private:tr('Mode privat','Modo privado')}[k];}")

# Saved layouts: the two new buttons are optional and go to the first free cells
rep("for(const id of ['speak','stop','show','word','clear','undo','redo','save','more','new']){const v=L[id];if(v===undefined&&['undo','redo','save','more'].includes(id)){o[id]=[0,0,1,1,0];if(id==='save'||id==='more')missing.push(id);continue;}",
    "for(const id of ['speak','stop','show','word','clear','undo','redo','save','more','new','silent','private']){const v=L[id];if(v===undefined&&['undo','redo','save','more','silent','private'].includes(id)){o[id]=[0,0,1,1,0];if(id!=='undo'&&id!=='redo')missing.push(id);continue;}")

# Layout: hidden silent/private fall back to the footer; footer only shown when it holds something
rep(" for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b){b.style.gridColumn='';b.style.gridRow='';b.hidden=false;}}\n if(!L){",
    " for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b){b.style.gridColumn='';b.style.gridRow='';b.hidden=false;}}\n queueMicrotask(placeStateButtons);\n if(!L){")
rep("for(const [k,id] of ACTION_BUTTONS){const b=$(id),it=L[k];if(!b)continue;if(!it||!it[4]){b.hidden=true;continue;}",
    "for(const [k,id] of ACTION_BUTTONS){const b=$(id),it=L[k];if(!b)continue;if(!it||!it[4]){if(k==='silent'||k==='private'){b.dataset.footer='true';continue;}b.hidden=true;continue;}delete b.dataset.footer;")
rep("function placeCompactControls(){const compact=matchMedia('(max-height:520px), (max-width:600px)').matches,top=document.querySelector('.status-top'),foot=document.querySelector('.footer');for(const id of ['silent-button','private-button']){const b=$(id),target=compact?top:foot;if(b&&target&&b.parentNode!==target)target.append(b);}}",
    "function placeCompactControls(){placeStateButtons();}\n"
    "/* 0.7.1: Silenci and Mode privat live in the main button grid; only a saved layout without room for them sends them back to the footer. */\n"
    "function placeStateButtons(){const compact=matchMedia('(max-height:520px), (max-width:600px)').matches,top=document.querySelector('.status-top'),foot=document.querySelector('.footer'),grid=$('composer-actions');let inFooter=false;"
    "for(const id of ['silent-button','private-button']){const b=$(id);if(!b||!grid)continue;if(b.dataset.footer==='true'){b.classList.add('flat');const target=compact?top:foot;if(target&&b.parentNode!==target)target.append(b);inFooter=inFooter||target===foot;}else{b.classList.remove('flat');if(b.parentNode!==grid){grid.append(b);applyActionLayout();}}}"
    "if(foot)foot.hidden=!inFooter;}")

# Silenci: always the muted speaker; the label says the state
rep("clear($('silent-button')).append(icon(prefs().silent?'silent':'speak'),el('span',{},prefs().silent?tr('Silenci activat','Silencio activado'):tr('Silenci','Silencio')));$('silent-button').setAttribute('aria-pressed',prefs().silent);clear($('private-button')).append(icon('lock'),el('span',{},tr('Mode privat','Modo privado')));$('private-button').setAttribute('aria-pressed',privateMode);",
    "clear($('silent-button')).append(icon('silent'),el('span',{},prefs().silent?tr('Silenci activat','Silencio activado'):tr('Silenci','Silencio')));$('silent-button').setAttribute('aria-pressed',prefs().silent);$('silent-button').setAttribute('aria-label',prefs().silent?tr('Silenci activat','Silencio activado'):tr('Silenci','Silencio'));clear($('private-button')).append(icon('lock'),el('span',{},privateMode?tr('Mode privat activat','Modo privado activado'):tr('Mode privat','Modo privado')));$('private-button').setAttribute('aria-pressed',privateMode);$('private-button').setAttribute('aria-label',privateMode?tr('Mode privat activat','Modo privado activado'):tr('Mode privat','Modo privado'));")

# The grid is rebuilt on every render: keep the two state buttons (they hold their own listeners)
rep(" const n=clear($('composer-actions'));\n const label=prefs().readScope", " const states=['silent-button','private-button'].map(id=>$(id)).filter(Boolean);const n=clear($('composer-actions'));\n const label=prefs().readScope")
rep("n.append(speak,stop,show,word,wipe,back,again,keep,more,fresh);applyActionLayout();","n.append(speak,stop,show,word,wipe,back,again,keep,more,fresh,...states.filter(b=>b.dataset.footer!=='true'));applyActionLayout();")

CSS="""
/* 0.7.1: Silenci and Mode privat in the main button grid; pressed state is highlighted */
.composer-actions #silent-button[aria-pressed=true],.composer-actions #private-button[aria-pressed=true]{background:var(--primary);color:var(--primaryText);border-color:var(--primary)}
.footer[hidden]{display:none}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
import json
T={"Mode privat activat":["Modu pribatua aktibatuta","Modo privado activado","Private mode on","Mode privé activé"]}
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(['eu','gl','en','fr']):
    key='"'+lang+'":{'; k=s.index(key,i)+len(key)
    if '"Mode privat activat":' in s[k:k+400000]:continue
    s=s[:k]+''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())+s[k:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

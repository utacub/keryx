# Applies the UTAC Keryx 0.7.4 change to index.html of 0.7.3 (2026-11-21):
# when the message buttons sit in a column (left or right) and the window is so low that a button would be
# smaller than 44 x 44 CSS px (tablet in landscape with the on-screen keyboard open, for example), the column
# widens and the buttons are laid out again in fewer, taller rows: more columns, Speak 2 x 2 when there is room.
# Otherwise nothing changes. 44 px is the WCAG 2.5.5 target size.
# Usage: python3 patch074.py index.html index.html.new
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.7\.3(?![:\d])','0.7.4',s)
# Reset any compact layout whenever the normal layout is applied, then check whether it is needed.
rep(" for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b){b.style.gridColumn='';b.style.gridRow='';b.hidden=false;}}\n queueMicrotask(placeStateButtons);",
    " for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b){b.style.gridColumn='';b.style.gridRow='';b.hidden=false;}}\n delete n.dataset.compact;n.style.gridAutoFlow='';n.parentElement?.style.removeProperty('--side-actions-w');if(!fittingActions)queueMicrotask(fitSideActions);\n queueMicrotask(placeStateButtons);")
rep("function actionLayoutProblem(L,kind,sel=''){",
r"""/* 0.7.4: buttons in a column that would be smaller than 44 x 44 px (a low window, such as a tablet in landscape with the on-screen keyboard open) are laid out again: a wider column with fewer, taller rows. Otherwise the layout stays as it is. */
const ACTION_MIN=44;let fittingActions=false;
function fitSideActions(){
 const n=$('composer-actions'),c=n?.parentElement;if(!n||!c||fittingActions)return;
 if(n.dataset.compact){fittingActions=true;try{applyActionLayout();}finally{fittingActions=false;}}
 if(actionLayoutKind()!=='side'||!n.offsetParent||!n.dataset.custom)return;
 const btns=[...n.children].filter(b=>b.tagName==='BUTTON'&&!b.hidden&&b.dataset.footer!=='true');if(!btns.length)return;
 const cs=getComputedStyle(n),padX=parseFloat(cs.paddingLeft)+parseFloat(cs.paddingRight),padY=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom),gap=parseFloat(cs.rowGap)||0,colGap=parseFloat(cs.columnGap)||gap;
 const H=n.clientHeight-padY,W=n.clientWidth-padX,rows=Math.max(1,...btns.map(b=>{const m=/(\d+) \/ span (\d+)/.exec(b.style.gridRow);return m?+m[1]+ +m[2]-1:1;})),cols=ACTION_GRID.side.cols;
 const now=Math.min((H-gap*(rows-1))/rows,(W-colGap*(cols-1))/cols);if(now>=ACTION_MIN)return;
 const maxW=c.clientWidth*0.5-padX,speak=btns.find(b=>b.id==='speak');let best=null;
 for(let C=3;C<=8;C++){
  const big=speak&&btns.length-1+4<=C*Math.ceil((btns.length+1)/C),R=Math.ceil((btns.length+(speak?(big?3:1):0))/C),rh=(H-gap*(R-1))/R;
  const cw=Math.min(Math.max(ACTION_MIN,Math.min(rh,72)),(maxW-colGap*(C-1))/C),score=Math.min(rh,cw);
  if(!best||score>best.score+0.5)best={C,R,cw,big,score};if(score>=ACTION_MIN)break;
 }
 if(!best||best.score<=now+1)return;
 n.dataset.compact=best.C;c.style.setProperty('--side-actions-w',Math.ceil(Math.max(n.offsetWidth,best.C*best.cw+colGap*(best.C-1)+padX+1))+'px');
 n.style.gridTemplateColumns='repeat('+best.C+',minmax(0,1fr))';n.style.gridTemplateRows='repeat('+best.R+',minmax(0,1fr))';n.style.gridAutoFlow='row dense';
 for(const b of btns){b.style.gridRow=b===speak&&best.big?'span 2':'';b.style.gridColumn=b===speak?'span 2':'span 1';}
}
function actionLayoutProblem(L,kind,sel=''){""")
rep("if($('dialog').open)reflowDialog();placeCompactControls();fitMessage();});",
    "if($('dialog').open)reflowDialog();placeCompactControls();fitSideActions();fitMessage();});")
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

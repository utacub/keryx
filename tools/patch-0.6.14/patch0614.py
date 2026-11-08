# Applies the UTAC Keryx 0.6.14 change to the built UTAC_Keryx_v0.6.13_local.html (Marc, 2026-11-08):
# the "Identitat gràfica…" paragraph is removed from the Information window, and Marc's name no longer appears
# anywhere in the app (the "Identitat gràfica aprovada…" sentence is also removed from the licence text, in every language).
# Also: every icon-only button shows an information label when the mouse rests on it (Marc, 2026-11-08).
# Usage: python3 patch0614.py UTAC_Keryx_v0.6.13_local.html UTAC_Keryx_v0.6.14_local.html
import sys, re
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.13(?![:\d])','0.6.14',s)
CA="Identitat gràfica: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas. Els logotips són marques de les institucions titulars i no formen part de la llicència de l’app."
ES="Identidad gráfica: logotipo de Keryx y logotipo original de UTAC, aportados por Marc Coronas. Los logotipos son marcas de las instituciones titulares y no forman parte de la licencia de la app."
rep(',el(\'p\',{},tr("'+CA+'","'+ES+'"))','')
# dictionary entries for that paragraph
key='"'+CA+'":"'
for _ in range(4):
    i=s.index(key);j=s.index('",',i+len(key))+2;s=s[:i]+s[j:]
assert CA not in s
# the remaining sentences that name Marc
while 'Coronas' in s:
    i=s.index('Coronas')
    a=s.rindex('. ',0,i)+2
    b=s.index('. ',i)+2
    assert b-a<200,s[a:b]
    s=s[:a]+s[b:]
assert 'Coronas' not in s

# Hover labels for icon-only buttons (mouse only)
JS="""
/* 0.6.14: hover labels. A button that shows only an icon (or a symbol) gets a small label after a short rest of the mouse. */
(()=>{let tip=null,timer=0,current=null;
 const visibleText=b=>{for(const n of b.querySelectorAll('span:not(.icon)')){if(!/\\p{L}{2}/u.test(n.textContent)||n.closest('svg'))continue;const r=n.getBoundingClientRect();if(r.width>2&&r.height>2&&getComputedStyle(n).clipPath==='none')return true;}for(const n of b.childNodes)if(n.nodeType===3&&/\\p{L}{2}/u.test(n.textContent))return true;return false;};
 const label=b=>(b.getAttribute('aria-label')||b.dataset.tipTitle||b.title||b.textContent||'').trim();
 const hide=()=>{clearTimeout(timer);timer=0;if(tip)tip.hidden=true;if(current&&current.dataset.tipTitle!=null){current.title=current.dataset.tipTitle;delete current.dataset.tipTitle;}current=null;};
 const show=b=>{const text=label(b);if(!text||!b.isConnected)return;if(!tip){tip=document.createElement('div');tip.id='hover-tip';tip.className='hover-tip';tip.setAttribute('role','tooltip');}
  (b.closest('dialog[open]')||document.body).append(tip);tip.textContent=text;tip.hidden=false;
  const r=b.getBoundingClientRect(),w=tip.offsetWidth,h=tip.offsetHeight;let x=r.left+r.width/2-w/2,y=r.bottom+8;
  if(y+h>innerHeight-4)y=r.top-h-8;x=Math.max(6,Math.min(x,innerWidth-w-6));tip.style.left=x+'px';tip.style.top=Math.max(4,y)+'px';};
 document.addEventListener('pointerover',e=>{if(e.pointerType!=='mouse')return;const b=e.target.closest?.('button');if(b===current)return;hide();if(!b||b.disabled||visibleText(b))return;
  current=b;if(b.title){b.dataset.tipTitle=b.title;b.removeAttribute('title');}timer=setTimeout(()=>{timer=0;if(current===b)show(b);},350);},true);
 document.addEventListener('pointerout',e=>{if(current&&!current.contains(e.relatedTarget))hide();},true);
 for(const ev of ['pointerdown','keydown','scroll','wheel'])addEventListener(ev,hide,true);addEventListener('blur',hide);
})();
"""
i=s.rindex('</script>\n</body>');s=s[:i]+JS+s[i:]
CSS="""
/* 0.6.14: hover labels for icon-only buttons */
.hover-tip{position:fixed;z-index:2147483000;max-width:min(320px,calc(100vw - 12px));padding:6px 10px;border-radius:8px;background:var(--text);color:var(--surface);font-size:13px;font-weight:600;line-height:1.3;pointer-events:none;box-shadow:0 4px 16px #0004;white-space:normal}
.hover-tip[hidden]{display:none}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

# Applies the UTAC Keryx 0.6.4 changes (installable PWA) to the built UTAC_Keryx_v0.6.3_local.html.
# Usage: python3 patch064.py UTAC_Keryx_v0.6.3_local.html UTAC_Keryx_v0.6.4_local.html
# The web edition also needs manifest.webmanifest, sw.js and icons/ next to index.html.
# GPL-3.0-or-later.
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:60],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.3(?!:)','0.6.4',s)

T={"Instal·lar":["Instalatu","Instalar","Install","Installer"],
 "Instal·lar Keryx":["Instalatu Keryx","Instalar Keryx","Install Keryx","Installer Keryx"],
 "Keryx s’ha instal·lat.":["Keryx instalatu da.","Keryx instalouse.","Keryx has been installed.","Keryx a été installé."],
 "Un cop instal·lat, Keryx s’obre com una aplicació, en una finestra pròpia, i funciona sense connexió. Les veus que ja hagis descarregat continuen disponibles.":["Instalatu ondoren, Keryx aplikazio gisa irekitzen da, bere leihoan, eta konexiorik gabe dabil. Deskargatutako ahotsek erabilgarri jarraitzen dute.","Unha vez instalado, Keryx ábrese como unha aplicación, nunha xanela propia, e funciona sen conexión. As voces que xa descargaches seguen dispoñibles.","Once installed, Keryx opens as an app in its own window and works without a connection. Voices you have already downloaded stay available.","Une fois installé, Keryx s’ouvre comme une application, dans sa propre fenêtre, et fonctionne sans connexion. Les voix déjà téléchargées restent disponibles."],
 "A l’iPhone o l’iPad, amb Safari: toca el botó Comparteix (el quadrat amb una fletxa cap amunt) i després «Afegeix a la pantalla d’inici».":["iPhone edo iPad-en, Safarirekin: ukitu Partekatu botoia (gora begirako gezia duen karratua) eta gero «Gehitu hasierako pantailan».","No iPhone ou no iPad, con Safari: toca o botón Compartir (o cadrado cunha frecha cara arriba) e despois «Engadir á pantalla de inicio».","On iPhone or iPad, in Safari: tap the Share button (the square with an arrow pointing up), then “Add to Home Screen”.","Sur iPhone ou iPad, dans Safari : touchez le bouton Partager (le carré avec une flèche vers le haut), puis « Sur l’écran d’accueil »."],
 "Aquest navegador no ofereix la instal·lació directament. Obre el menú del navegador i tria «Instal·la l’aplicació» o «Afegeix a la pantalla d’inici». Si no hi apareix, obre Keryx amb Chrome, Edge o Safari.":["Nabigatzaile honek ez du instalazioa zuzenean eskaintzen. Ireki nabigatzailearen menua eta aukeratu «Instalatu aplikazioa» edo «Gehitu hasierako pantailan». Agertzen ez bada, ireki Keryx Chrome, Edge edo Safarirekin.","Este navegador non ofrece a instalación directamente. Abre o menú do navegador e escolle «Instalar aplicación» ou «Engadir á pantalla de inicio». Se non aparece, abre Keryx con Chrome, Edge ou Safari.","This browser does not offer installation directly. Open the browser menu and choose “Install app” or “Add to Home screen”. If it is not there, open Keryx in Chrome, Edge or Safari.","Ce navigateur ne propose pas l’installation directement. Ouvrez le menu du navigateur et choisissez « Installer l’application » ou « Ajouter à l’écran d’accueil ». Si l’option n’apparaît pas, ouvrez Keryx avec Chrome, Edge ou Safari."],
 "Aquest fitxer s’ha obert des de l’ordinador i no es pot instal·lar. Per instal·lar Keryx, obre’l des de la web:":["Fitxategi hau ordenagailutik ireki da eta ezin da instalatu. Keryx instalatzeko, ireki webgunetik:","Este ficheiro abriuse desde o ordenador e non se pode instalar. Para instalar Keryx, ábreo desde a web:","This file was opened from the computer and cannot be installed. To install Keryx, open it from the web:","Ce fichier a été ouvert depuis l’ordinateur et ne peut pas être installé. Pour installer Keryx, ouvrez-le depuis le web :"],
 "Tancar":None}
for i,lang in enumerate(['eu','gl','en','fr']):
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v[i],ensure_ascii=False)+',' for k,v in T.items() if v)
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')

# --- manifest, icons and the policy that lets the page load them and its service worker
rep('<meta name="theme-color" content="#0A5509">','<meta name="theme-color" content="#0A5509">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Keryx">')
rep("img-src data:;","img-src data: 'self';")
rep("worker-src blob:;","worker-src blob: 'self'; manifest-src 'self';")

# --- install button, top right
rep('<button id="info-button" class="icon-only flat" aria-haspopup="dialog"></button>','<button id="info-button" class="icon-only flat" aria-haspopup="dialog"></button><button id="install-button" class="install-button" type="button" hidden></button>')
JS=r"""
/* 0.6.4: installable app. The service worker (sw.js) keeps Keryx working offline once opened. The install button sits at the top right and disappears once Keryx runs installed. */
let installPrompt=null;
const isInstalled=()=>matchMedia('(display-mode: standalone)').matches||matchMedia('(display-mode: fullscreen)').matches||matchMedia('(display-mode: minimal-ui)').matches||navigator.standalone===true;
const isAppleMobile=()=>/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
function renderInstall(){const b=$('install-button');if(!b)return;b.hidden=isInstalled();clear(b).append(icon('download'),el('span',{},tr('Instal·lar','Instalar')));b.title=tr('Instal·lar Keryx','Instalar Keryx');b.setAttribute('aria-label',tr('Instal·lar Keryx','Instalar Keryx'));}
async function installApp(){
 if(installPrompt){const p=installPrompt;installPrompt=null;try{await p.prompt();const r=await p.userChoice;if(r?.outcome==='accepted'){$('install-button').hidden=true;}}catch{}return;}
 const local=location.protocol==='file:';
 const body=[el('p',{class:'prose'},tr('Un cop instal·lat, Keryx s’obre com una aplicació, en una finestra pròpia, i funciona sense connexió. Les veus que ja hagis descarregat continuen disponibles.','Una vez instalado, Keryx se abre como una aplicación, en una ventana propia, y funciona sin conexión. Las voces que ya hayas descargado siguen disponibles.'))];
 if(local)body.push(el('p',{class:'prose'},tr('Aquest fitxer s’ha obert des de l’ordinador i no es pot instal·lar. Per instal·lar Keryx, obre’l des de la web:','Este archivo se ha abierto desde el ordenador y no se puede instalar. Para instalar Keryx, ábrelo desde la web:')),el('p',{class:'prose'},el('strong',{},'https://utacub.github.io/keryx/')));
 else if(isAppleMobile())body.push(el('p',{class:'prose'},tr('A l’iPhone o l’iPad, amb Safari: toca el botó Comparteix (el quadrat amb una fletxa cap amunt) i després «Afegeix a la pantalla d’inici».','En el iPhone o el iPad, con Safari: toca el botón Compartir (el cuadrado con una flecha hacia arriba) y después «Añadir a pantalla de inicio».')));
 else body.push(el('p',{class:'prose'},tr('Aquest navegador no ofereix la instal·lació directament. Obre el menú del navegador i tria «Instal·la l’aplicació» o «Afegeix a la pantalla d’inici». Si no hi apareix, obre Keryx amb Chrome, Edge o Safari.','Este navegador no ofrece la instalación directamente. Abre el menú del navegador y elige «Instalar aplicación» o «Añadir a pantalla de inicio». Si no aparece, abre Keryx con Chrome, Edge o Safari.')));
 openDialog(tr('Instal·lar Keryx','Instalar Keryx'),body,[button(tr('Tancar','Cerrar'),closeDialog,'primary')],'scroll-dialog');
}
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;renderInstall();});
window.addEventListener('appinstalled',()=>{installPrompt=null;if($('install-button'))$('install-button').hidden=true;notify(tr('Keryx s’ha instal·lat.','Keryx se ha instalado.'));});
matchMedia('(display-mode: standalone)').addEventListener?.('change',renderInstall);
if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'||location.hostname==='127.0.0.1'))window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{});});
"""
rep("renderAll();refreshVoices();if(matchMedia('(hover:hover) and (pointer:fine)').matches)",
    JS.strip()+"\n$('install-button').onclick=installApp;\nrenderAll();refreshVoices();if(matchMedia('(hover:hover) and (pointer:fine)').matches)")
rep("renderVoice();updateTextUI();renderAccess();}","renderVoice();updateTextUI();renderAccess();renderInstall();}")

CSS="""
/* 0.6.4: install button, top right */
.install-button{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:6px 12px;border-radius:10px;border:2px solid var(--primary);background:var(--primary);color:var(--primaryText);font-weight:700;font-size:14px;white-space:nowrap}
.install-button:focus-visible{outline-color:var(--primaryText)}
@media(max-width:1000px){.install-button span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}.install-button{padding:6px;min-width:40px;justify-content:center}}
@media(max-width:600px){.install-button{min-width:36px;min-height:36px;padding:5px}.install-button .icon{width:18px;height:18px}}
/* Small phones: a narrower logo and language button leave room for it. */
@media(max-width:400px){.header-inner .brand{width:118px;height:30px}.lang-btn{padding:5px 6px;gap:4px}}
@media(max-width:350px){.header-inner .brand{width:96px;height:26px}.lang-btn .icon:last-child{display:none}.header-control{gap:0}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)

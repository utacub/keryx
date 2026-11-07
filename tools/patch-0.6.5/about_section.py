# 0.6.5: the Information window gathers every credit and licence, with the structure of
# «Sobre LECAA Docs» (utacub/lecaa_docs, src/about.ts at c1f870a): the idea, origin and institutions
# with their logos, tools and resources, licences, references and version.
# GPL-3.0-or-later.
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda x: json.dumps(x, ensure_ascii=False)

def data_uri(name):
    with open(os.path.join(HERE, 'logos', name), 'rb') as f:
        return 'data:image/webp;base64,' + base64.b64encode(f.read()).decode()

# [file, alt, caption ca, caption es, url] (captions in Catalan are proper names; kept in every language)
INSTITUTIONS = [
    ('utac-negre.webp', 'UTAC', 'Unitat de Tècniques Augmentatives de Comunicació', 'https://www.utac.cat/'),
    ('ub.webp', 'Universitat de Barcelona', 'Universitat de Barcelona', 'https://web.ub.edu/'),
    ('fbg.webp', 'Fundació Bosch i Gimpera', 'Fundació Bosch i Gimpera', 'https://www.fbg.ub.edu/'),
    ('gencat-educacio.webp', 'Departament d’Educació i Formació Professional', 'UTAC Educació · Departament d’Educació i Formació Professional', 'https://educacio.gencat.cat/'),
    ('gencat-drets-socials.webp', 'Departament de Drets Socials i Inclusió', 'UTAC Sírius · Departament de Drets Socials i Inclusió', 'https://dretssocials.gencat.cat/'),
]

# New Catalan strings and their translations (eu, gl, en, fr). Spanish goes in the code, next to the Catalan.
T = {
 'Keryx s’ha creat des de la Unitat de Tècniques Augmentatives de Comunicació (UTAC), fent servir eines d’intel·ligència artificial.':
  ('Keryx Komunikazio Teknika Augmentatiboen Unitatean (UTAC) sortu da, adimen artifizialeko tresnak erabiliz.',
   'Keryx creouse desde a Unitat de Tècniques Augmentatives de Comunicació (UTAC), empregando ferramentas de intelixencia artificial.',
   'Keryx was created at the Unitat de Tècniques Augmentatives de Comunicació (UTAC), using artificial intelligence tools.',
   'Keryx a été créé au sein de l’Unitat de Tècniques Augmentatives de Comunicació (UTAC), à l’aide d’outils d’intelligence artificielle.'),
 'Identitat gràfica: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas. Els logotips són marques de les institucions titulars i no formen part de la llicència de l’app.':
  ('Identitate grafikoa: Keryxen logotipoa eta UTACen jatorrizko logotipoa, Marc Coronasek emanak. Logotipoak erakunde titularren markak dira eta ez dira aplikazioaren lizentziaren parte.',
   'Identidade gráfica: logotipo de Keryx e logotipo orixinal da UTAC, achegados por Marc Coronas. Os logotipos son marcas das institucións titulares e non forman parte da licenza da app.',
   'Visual identity: Keryx logo and original UTAC logo, provided by Marc Coronas. The logos are trademarks of their institutions and are not covered by the app’s licence.',
   'Identité visuelle : logo de Keryx et logo original de l’UTAC, fournis par Marc Coronas. Les logos sont des marques des institutions titulaires et ne relèvent pas de la licence de l’application.'),
 'Keryx també funciona com un sol fitxer HTML, per enviar-lo per correu o portar-lo en un llapis USB i obrir-lo sense connexió en qualsevol navegador. ':
  ('Keryx fitxategi HTML bakar gisa ere badabil, posta elektronikoz bidaltzeko edo USB memoria batean eramateko eta edozein nabigatzailetan konexiorik gabe irekitzeko. ',
   'Keryx tamén funciona como un só ficheiro HTML, para envialo por correo ou levalo nun lapis USB e abrilo sen conexión en calquera navegador. ',
   'Keryx also works as a single HTML file, to send by email or carry on a USB stick and open offline in any browser. ',
   'Keryx fonctionne aussi comme un seul fichier HTML, à envoyer par courriel ou à emporter sur une clé USB et à ouvrir hors ligne dans n’importe quel navigateur. '),
 'Descarrega l’HTML de Keryx':('Deskargatu Keryxen HTMLa','Descargar o HTML de Keryx','Download the Keryx HTML file','Télécharger le fichier HTML de Keryx'),
 'Keryx és programari lliure, amb la llicència GNU GPL 3.0 o posterior: es pot fer servir, estudiar, modificar i compartir, i les versions modificades s’han de compartir amb la mateixa llicència. El compromís del projecte és que totes les seves funcions siguin gratuïtes i de codi obert. ':
  ('Keryx software librea da, GNU GPL 3.0 edo geroagoko lizentziarekin: erabili, aztertu, aldatu eta partekatu daiteke, eta aldatutako bertsioak lizentzia berarekin partekatu behar dira. Proiektuaren konpromisoa da funtzio guztiak doakoak eta kode irekikoak izatea. ',
   'Keryx é software libre, coa licenza GNU GPL 3.0 ou posterior: pódese usar, estudar, modificar e compartir, e as versións modificadas deben compartirse coa mesma licenza. O compromiso do proxecto é que todas as súas funcións sexan gratuítas e de código aberto. ',
   'Keryx is free software, under the GNU GPL 3.0 or later: it can be used, studied, modified and shared, and modified versions must be shared under the same licence. The project is committed to keeping every feature free of charge and open source. ',
   'Keryx est un logiciel libre, sous licence GNU GPL 3.0 ou ultérieure : on peut l’utiliser, l’étudier, le modifier et le partager, et les versions modifiées doivent être partagées sous la même licence. Le projet s’engage à ce que toutes ses fonctions soient gratuites et open source. '),
 'Les veus descarregables tenen llicències pròpies:':('Ahots deskargagarriek beren lizentziak dituzte:','As voces descargables teñen licenzas propias:','The downloadable voices have their own licences:','Les voix téléchargeables ont leurs propres licences :'),
 'Text complet de les llicències:':('Lizentzien testu osoa:','Texto completo das licenzas:','Full text of the licences:','Texte complet des licences :'),
 'Codi de veus i menú':('Ahotsen eta menuaren kodea','Código de voces e menú','Voice and menu code','Code des voix et du menu'),
 'Motor de veu':('Ahots-motorra','Motor de voz','Speech engine','Moteur vocal'),
 'Tipografia':('Letra-tipoa','Tipografía','Font','Police'),
 'Versió 0.6.5 · 7 de novembre de 2026':('0.6.5 bertsioa · 2026ko azaroaren 7a','Versión 0.6.5 · 7 de novembro de 2026','Version 0.6.5 · 7 November 2026','Version 0.6.5 · 7 novembre 2026'),
}
ES = {
 'Keryx s’ha creat des de la Unitat de Tècniques Augmentatives de Comunicació (UTAC), fent servir eines d’intel·ligència artificial.':'Keryx se ha creado desde la Unitat de Tècniques Augmentatives de Comunicació (UTAC), utilizando herramientas de inteligencia artificial.',
 'Identitat gràfica: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas. Els logotips són marques de les institucions titulars i no formen part de la llicència de l’app.':'Identidad gráfica: logotipo de Keryx y logotipo original de UTAC, aportados por Marc Coronas. Los logotipos son marcas de las instituciones titulares y no forman parte de la licencia de la app.',
 'Keryx també funciona com un sol fitxer HTML, per enviar-lo per correu o portar-lo en un llapis USB i obrir-lo sense connexió en qualsevol navegador. ':'Keryx también funciona como un solo archivo HTML, para enviarlo por correo o llevarlo en un lápiz USB y abrirlo sin conexión en cualquier navegador. ',
 'Descarrega l’HTML de Keryx':'Descargar el HTML de Keryx',
 'Keryx és programari lliure, amb la llicència GNU GPL 3.0 o posterior: es pot fer servir, estudiar, modificar i compartir, i les versions modificades s’han de compartir amb la mateixa llicència. El compromís del projecte és que totes les seves funcions siguin gratuïtes i de codi obert. ':'Keryx es software libre, con la licencia GNU GPL 3.0 o posterior: se puede usar, estudiar, modificar y compartir, y las versiones modificadas deben compartirse con la misma licencia. El compromiso del proyecto es que todas sus funciones sean gratuitas y de código abierto. ',
 'Les veus descarregables tenen llicències pròpies:':'Las voces descargables tienen licencias propias:',
 'Text complet de les llicències:':'Texto completo de las licencias:',
 'Codi de veus i menú':'Código de voces y menú',
 'Motor de veu':'Motor de voz',
 'Tipografia':'Tipografía',
 'Versió 0.6.5 · 7 de novembre de 2026':'Versión 0.6.5 · 7 de noviembre de 2026',
}

def tr(ca):
    return 'tr(%s,%s)' % (J(ca), J(ES[ca]))

def build(s, H, P):
    """Rewrites helpDialog of the 0.6.4 build (after the 0.6.5 text fixes) and removes licencesDialog."""
    a = s.index('function helpDialog(){'); b = s.index('\n', s.index("openDialog(tr('Informació de Keryx'", a))
    old = s[a:b]
    desc_start = old.index("el('p',{class:'prose'},tr('Keryx és un comunicador alfabètic")
    desc = old[desc_start:old.index("button(tr('Manual d’accés amb teclat'")].rstrip(',')
    desc = desc.replace("el('p',{class:'prose'},","el('p',{},",1)
    usage1 = old[old.index("button(tr('Manual d’accés amb teclat'"):old.index(");\ncontent.append(el('h3',{},tr('Veus en línia'")]
    usage2 = old[old.index("el('h3',{},tr('Veus en línia'"):old.index(",el('h3',{},tr('Projecte i crèdits'")]
    refs = old[old.index('const refs='):old.index('const details=')]
    details = old[old.index('const details='):old.index('content.append(details);')]
    name = "el('h3',{},tr(%s,%s)),%s" % (J(H['ca']), J(H['es']), ','.join("el('p',{},tr(%s,%s))" % (J(p['ca']), J(p['es'])) for p in P))
    inst = ','.join("el('figure',{},el('a',{href:%s,target:'_blank',rel:'noopener noreferrer'},el('img',{src:%s,alt:%s})),el('figcaption',{},%s))" % (J(u), J(data_uri(f)), J(alt), J(cap)) for f, alt, cap, u in INSTITUTIONS)
    tools = ("[[tr('Aplicació','Aplicación'),'ChatGPT (0.6.0)','OpenAI','https://chatgpt.com/'],"
             "[tr('Aplicació','Aplicación'),'Claude (0.6.1 i posteriors)'.replace(' i ',tr(' i ',' y ')).replace('posteriors',tr('posteriors','posteriores')),'Anthropic','https://claude.ai/'],"
             "[" + tr('Codi de veus i menú') + ",'LECAA Docs (c1f870a)','UTAC · GPL 3.0','https://github.com/utacub/lecaa_docs/tree/c1f870a65a35573ed66fc597834a7376269b9fae'],"
             "[tr('Veus per descarregar','Voces para descargar'),'Piper ('+KeryxNeural.MODELS.map(m=>m.title.replace(/ \\(.*\\)$/,'')).join(', ')+')','Rhasspy · Open Home Foundation','https://github.com/rhasspy/piper'],"
             "[" + tr('Motor de veu') + ",'ONNX Runtime Web 1.18.0','Microsoft · MIT','https://onnxruntime.ai/'],"
             "[" + tr('Motor de veu') + ",'piper-wasm 1.0.0 · Piper phonemizer · eSpeak NG','Diffusion Studio · MIT · GPL 3.0','https://github.com/diffusionstudio/piper-wasm'],"
             "[" + tr('Tipografia') + ",'DejaVu Sans','DejaVu fonts','https://dejavu-fonts.github.io/']]")
    new = ("function helpDialog(){const content=el('div',{class:'prose about'});\n"
      " const link=(label,url,attrs={})=>el('a',{href:url,target:'_blank',rel:'noopener noreferrer',...attrs},label);\n"
      " const logo=el('div',{class:'about-logo'});document.querySelectorAll('.brand-wrap img.brand').forEach(im=>logo.append(im.cloneNode(true)));\n"
      " content.append(logo,el('h3',{},tr('La idea','La idea'))," + desc + "," + name + "," + usage1 + ");\n"
      " content.append(" + usage2 + ");\n"
      " if(location.protocol!=='file:')content.append(el('h3',{},tr('Versió portàtil','Versión portátil')),el('p',{}," + tr('Keryx també funciona com un sol fitxer HTML, per enviar-lo per correu o portar-lo en un llapis USB i obrir-lo sense connexió en qualsevol navegador. ') + ",el('a',{href:'./UTAC_Keryx_v0.6.5_local.html',download:'UTAC_Keryx_v0.6.5_local.html'}," + tr('Descarrega l’HTML de Keryx') + ")));\n"
      " content.append(el('h3',{},tr('Origen i institucions','Origen e instituciones')),el('p',{}," + tr('Keryx s’ha creat des de la Unitat de Tècniques Augmentatives de Comunicació (UTAC), fent servir eines d’intel·ligència artificial.') + "),"
      "el('p',{},tr('La UTAC és un equip de la Universitat de Barcelona i de la Fundació Bosch i Gimpera. Concreta la seva activitat a partir de dos serveis de la Generalitat de Catalunya: UTAC Educació, del Departament d’Educació i Formació Professional, i UTAC Sírius, del Departament de Drets Socials i Inclusió.','La UTAC es un equipo de la Universitat de Barcelona y de la Fundació Bosch i Gimpera. Concreta su actividad a partir de dos servicios de la Generalitat de Catalunya: UTAC Educació, del Departament d’Educació i Formació Professional, y UTAC Sírius, del Departament de Drets Socials i Inclusió.')),"
      "el('div',{class:'about-institutions'}," + inst + "),el('p',{}," + tr('Identitat gràfica: logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas. Els logotips són marques de les institucions titulars i no formen part de la llicència de l’app.') + "));\n"
      " const TOOLS=" + tools + ";\n"
      " content.append(el('h3',{},tr('Eines i recursos','Herramientas y recursos')),el('ul',{class:'about-tools'},...TOOLS.map(([use,product,owner,url])=>el('li',{},el('span',{class:'use'},use),el('strong',{},product),el('span',{},owner),link(url.replace(/^https?:\\/\\//,'').replace(/\\/$/,''),url)))));\n"
      " const licence=(id,title)=>()=>{openDialog(title,$(id).textContent.split(/\\n\\s*\\n/).map(text=>el('p',{class:'prose'},text)),[button(tr('Tornar','Volver'),helpDialog,'primary')],'scroll-dialog');dialogBack=helpDialog;};\n"
      " content.append(el('h3',{},tr('Llicències','Licencias')),el('p',{}," + tr('Keryx és programari lliure, amb la llicència GNU GPL 3.0 o posterior: es pot fer servir, estudiar, modificar i compartir, i les versions modificades s’han de compartir amb la mateixa llicència. El compromís del projecte és que totes les seves funcions siguin gratuïtes i de codi obert. ') + ",link(tr('Codi font','Código fuente'),'https://github.com/utacub/keryx'),' · ',link('GNU GPL 3.0','https://www.gnu.org/licenses/gpl-3.0.html')),"
      "el('p',{}," + tr('Les veus descarregables tenen llicències pròpies:') + "),el('ul',{class:'about-list'},...KeryxNeural.MODELS.map(m=>el('li',{},m.title+' · '+m.licence+' ',link(tr('Llicència','Licencia'),m.licenceUrl)))),"
      "el('p',{}," + tr('Text complet de les llicències:') + "),el('div',{class:'about-buttons'},button('GNU GPL 3.0',licence('code-license','GNU General Public License v3.0')),button('ONNX Runtime · MIT',licence('third-party-license','ONNX Runtime · MIT'))));\n"
      " " + details + "content.append(details);\n"
      " content.append(el('h3',{},tr('Referències','Referencias')));\n"
      " " + refs + "\n"
      " content.append(el('p',{class:'about-version'},'UTAC Keryx · '," + tr('Versió 0.6.5 · 7 de novembre de 2026') + "));\n"
      " openDialog(tr('Informació de Keryx','Información de Keryx'),[content],[button(tr('Ajustos','Ajustes'),()=>settingsDialog('voice')),button(tr('Tancar','Cerrar'),closeDialog,'primary')],'scroll-dialog');}")
    s = s[:a] + new + s[b:]
    # licencesDialog is now part of the Information window.
    c = s.index('function licencesDialog(){'); d = s.index('\n}\n', c) + 3
    s = s[:c] + s[d:]
    assert 'licencesDialog' not in s
    # Lists of credits keep their links (other lists in dialogs are flattened to paragraphs).
    a1="if(n.tagName==='UL'){"; assert s.count(a1)==1
    s=s.replace(a1,"if(n.tagName==='UL'&&!n.matches('.about-tools,.about-list')){")
    # Dictionaries
    for i, lang in enumerate(['eu', 'gl', 'en', 'fr']):
        ins = ''.join(J(k) + ':' + J(v[i]) + ',' for k, v in T.items())
        key = '"%s":{"' % lang
        assert s.count(key) == 1
        s = s.replace(key, '"%s":{' % lang + ins + '"')
    return s

CSS = """
/* 0.6.5: Information window with every credit and licence, as in «Sobre LECAA Docs». */
.about-logo{height:52px;margin-bottom:6px}.about-logo img.brand{height:52px;width:auto!important;aspect-ratio:2752/742}
.about-list{margin:0 0 10px;padding-left:20px;font-size:14px}.about-list li{margin:4px 0}
.about-institutions{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px 24px;margin:16px 0}
.about-institutions figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center}
.about-institutions a{display:flex;align-items:center;justify-content:center;height:84px;width:100%;padding:6px 10px;border-radius:10px;background:#fff;border:1px solid var(--line)}
.about-institutions img{max-height:100%;max-width:100%;object-fit:contain}
.about-institutions figcaption{font-size:13px;color:var(--muted)}
.about-tools{list-style:none;margin:0;padding:0}
.about-tools li{display:grid;grid-template-columns:11rem 1fr;gap:0 14px;padding:8px 0;border-bottom:1px solid var(--line)}
.about-tools .use{grid-row:span 3;color:var(--muted);font-size:14px}
.about-tools a{font-size:14px;overflow-wrap:anywhere}
.about-buttons{display:flex;flex-wrap:wrap;gap:8px}
.about-version{color:var(--muted);font-size:13px;margin-top:16px}
@media(max-width:560px){.about-tools li{grid-template-columns:1fr}.about-tools .use{grid-row:auto}}
"""

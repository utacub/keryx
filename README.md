# UTAC Keryx 0.6.6

Comunicador alfabètic d’UTAC amb pantalla principal fixa, panell inferior minimitzable i ajustos amb desplaçament vertical. Obriu `UTAC_Keryx_v0.6.6_local.html` amb un navegador. No necessita servidor ni clau d’API. Les descàrregues de veus necessiten Internet la primera vegada.

## Aplicació web i fitxer local

- Aplicació: https://utacub.github.io/keryx/
- Edició descarregable: [`UTAC_Keryx_v0.6.6_local.html`](UTAC_Keryx_v0.6.6_local.html).
- La web i l’HTML descarregable contenen la mateixa aplicació. Les dades de cada navegador i origen són independents; per traslladar frases i ajustos, feu servir Ajustos → Dades → Exportar/Importar còpia.
- Publicació amb GitHub Pages des de la branca `main`, carpeta arrel. `index.html` és autònom; `.nojekyll` evita el processament Jekyll.
- Per publicar una modificació: executeu `python3 build.py`, les proves indicades més avall i incorporeu els fitxers resultants a `main`. La construcció actualitza `index.html`, l’HTML descarregable i la previsualització `dist/index.html`.

## Canvis de la versió 0.6.6

- **Parlar ja no ha de ser el botó més gran.** En editar la disposició dels botons, Parlar ha de continuar sent visible, però ja pot tenir qualsevol mida, com els altres (decisió de Marc, 7 de novembre de 2026).
- **Botons només amb icona.** Els botons del grup principal (Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot, Desfer, Refer i Nou missatge) mostren només la icona. El nom es manté com a nom accessible i com a indicació en passar-hi el ratolí.
- **Desfer i Refer al grup de botons.** Desfer i Refer són ara botons del grup principal, que es poden col·locar, redimensionar i amagar a l’editor de botons com els altres, i ja no surten a sota del camp del missatge. La graella lateral passa de 2 × 5 a 2 × 6. A la posició inferior, en pantalles de menys de 700 px d’amplada i sense disposició desada, els botons es reparteixen en dues files perquè no quedin massa estrets.
- **Pestanya Documents.** Nova pestanya del panell per preparar textos llargs de text pla abans de dir-los. Permet crear, obrir, reanomenar, editar (es desa automàticament), eliminar, importar fitxers `.txt` i exportar-los. Des d’un document es pot parlar tot el text o només la selecció, mostrar-lo a pantalla completa o portar-lo al missatge. Els documents es desen en aquest navegador, separats per perfil (fins a 200 documents de 200.000 caràcters).
- `sw.js` passa a `keryx-0.6.6`.

La 0.6.6 s’obté aplicant `tools/patch-0.6.6/patch066.py` sobre l’HTML de la 0.6.5 (commit `5882800`).

Validació (7 de novembre de 2026), Chromium amb Playwright: amb els botons a baix, a l’esquerra i a la dreta, a 1280×800, 768×1024, 390×844 i 740×360, tots els botons (també Desfer i Refer) són al grup, sense text visible i sense desplaçament de la pàgina. Les sis pestanyes caben en una fila a 320, 390, 740 i 1280 px. A Documents: crear, editar, desar automàticament, portar al missatge, tornar a la llista i conservar-lo després de recarregar funcionen, i no hi ha errors de JavaScript.

## Canvis de la versió 0.6.5

- **Sense finestra de primera vegada.** La finestra «Comencem amb Keryx» ja no s’obre en entrar per primer cop: Keryx comença directament a la pantalla principal, en català, amb accés directe (tacte, ratolí o teclat). La llengua es canvia amb el botó de la capçalera, i l’accés i la veu, a Ajustos (decisió de Marc, 7 de novembre de 2026).
- **Versió al costat del logo.** La versió apareix en petit a la dreta del logo («v. 0.6.5»), alineada per sota amb la línia de base de la paraula Keryx (al 65,2 % de l’alçada del logo, mesurat sobre l’SVG de marca). La caixa del logo s’ajusta ara al dibuix, i als mòbils de 400 px o menys el logo i els espais de la capçalera s’estrenyen una mica perquè tot hi càpiga fins a 320 px.
- **Botons de la capçalera.** «Instal·lar» mostra només la icona, amb la mida dels altres botons d’icona; el text queda com a nom accessible. «Informació» té ara aspecte de botó, com «Ajustos» (decisions de Marc, 7 de novembre de 2026).
- **Crèdits i llicències a la Informació.** Tots els crèdits i llicències són ara a la finestra d’Informació, amb l’estructura de «Sobre LECAA Docs» (`utacub/lecaa_docs`, `src/about.ts`, commit `c1f870a`): logotip, la idea, per què es diu Keryx, l’ajuda d’ús, versió portàtil (a la web), origen i institucions amb els cinc logotips (UTAC, Universitat de Barcelona, Fundació Bosch i Gimpera, Departament d’Educació i Formació Professional, Departament de Drets Socials i Inclusió, presos de LECAA Docs a `tools/patch-0.6.5/logos/`), eines i recursos, llicències (amb el text complet de la GPL i la MIT d’ONNX Runtime i la llicència de cada veu), referències i versió. La finestra separada «Llicències del codi i les veus» desapareix. També es treuen «UTAC · Universitat de Barcelona» del peu i «Prototip local · versió» de la barra de la conversa; la versió es veu al costat del logo. El text és a `tools/patch-0.6.5/about_section.py`.
- **Per què es diu Keryx.** La finestra d’Informació té un apartat breu, en les sis llengües, sobre l’origen del nom: el grec κῆρυξ (kēryx, «herald»), Hermes com a patró dels heralds, el personatge mític Kēryx (Ceryx, Kèrix), fill d’Hermes segons Pausànies (1.38.3), i el lligam amb BJ Hermes i Hermes Mobile: l’app, com l’herald, lliura el missatge per la persona que no el pot dir parlant. Les fonts (Britannica Editors, s. d.; Confederación ASPACE, 2014; Theoi Project, s. d.) són les de la secció 1.1 del document de planificació i s’han afegit a les referències. El text és a `tools/patch-0.6.5/name_section.py`.
- **Revisió del català.** S’ha revisat tot el text en català que es veu a Keryx (botons, avisos, ajustos, ajuda, informació i frases). Correccions:
  - la tecla de majúscules s’anomena «Maj», no «Majús»;
  - la llista de pendents ja no inclou la instal·lació PWA, que ja està feta;
  - s’han completat frases a què faltava un complement o un article («Fes més petit un altre botó o amaga’l», «la veu del navegador», «quan torni a obrir Keryx», «els sis idiomes», «una còpia de Keryx»);
  - «la seva cantonada» passa a «arrossega’n la cantonada», i la lectura de frases es descriu com «en escriure un punt, un interrogant o una exclamació, o en prémer Intro»;
  - als crèdits, «logotip de Keryx i logotip original d’UTAC, aportats per Marc Coronas» i «GPL-3.0 o posterior».

  Com que el text català és també la clau de les traduccions, cada canvi s’aplica igualment als diccionaris basc, gallec, anglès i francès. El quadre «Aplicació instal·lada» que mostra Windows en instal·lar Keryx amb Edge (amb el botó «No ho permetes») és del sistema i no es pot canviar des de l’aplicació.
- `sw.js` passa a `keryx-0.6.5`.

La 0.6.5 s’obté aplicant `tools/patch-0.6.5/patch065.py` sobre l’HTML de la 0.6.4 (commit `9cfeff4`).

Validació (7 de novembre de 2026), Chromium amb Playwright i un navegador sense dades: a 1280×800 i 390×844 no s’obre cap finestra ni en la primera visita ni en recarregar, i no hi ha errors de JavaScript. La capçalera no es desborda a 320, 340, 360, 390, 768 i 1280 px d’amplada, ni a 740×360, i tots els botons queden dins la pantalla.

## Canvis de la versió 0.6.4

- **Aplicació instal·lable (PWA).** La web té ara un manifest (`manifest.webmanifest`), les icones del kit de marca (`icons/`: 192 i 512 px, versions maskable i icona d’Apple de 180 px) i un service worker (`sw.js`). Un cop oberta, Keryx funciona sense connexió: la pàgina es demana primer a la xarxa, de manera que una versió nova s’aplica en tornar a obrir amb connexió, i sense connexió es fa servir la còpia desada. El service worker no intervé en les descàrregues de veus ni en altres llocs.
- **Botó «Instal·lar» a dalt a la dreta.** Als navegadors que ho permeten (Chrome, Edge, Samsung Internet…), obre el diàleg d’instal·lació del navegador. A l’iPhone i l’iPad explica com fer-ho amb Safari (Comparteix → Afegeix a la pantalla d’inici), perquè Safari no permet que una web obri aquest diàleg. Als altres navegadors indica on és l’opció al menú. Si l’HTML s’ha obert des de l’ordinador, explica que cal obrir-lo des de la web. El botó desapareix quan Keryx funciona instal·lat. En pantalles de 1000 px o menys només mostra la icona.
- La política de seguretat de contingut admet ara el manifest, les icones i el service worker del mateix origen (`manifest-src 'self'`, `img-src 'self'`, `worker-src 'self'`).
- En publicar una versió nova cal canviar `VERSION` a `sw.js`, perquè els dispositius instal·lats descartin la còpia anterior.

La 0.6.4 s’obté aplicant `tools/patch-0.6.4/patch064.py` sobre l’HTML de la 0.6.3 (commit `e338cc4`).

Validació (7 de novembre de 2026), Chromium amb Playwright servint la carpeta per HTTP local: el service worker s’activa; Chromium no troba errors al manifest ni cap motiu que impedeixi la instal·lació; en recarregar sense connexió l’aplicació s’obre igualment; la capçalera hi cap sense desbordar-se a 320, 360 i 390 px d’amplada; les proves de pantalla fixa de la 0.6.2 continuen passant. No s’ha provat la instal·lació real en Android, iOS ni escriptori.

## Canvis de la versió 0.6.3

- **Arrossegar a l’editor dels botons principals.** Un botó es mou arrossegant-lo dins la graella, i canvia de mida arrossegant la cantonada inferior dreta del botó seleccionat. Si es deixa anar sobre un botó de la mateixa mida, s’intercanvien. Mentre s’arrossega, la graella mostra on quedarà; si la posició no és vàlida (solapament, fora de la graella o un botó tan gran com Parlar), el botó es marca amb un contorn discontinu i en deixar-lo anar torna on era, amb el motiu escrit a sota.
- **Sense botons de control.** Els botons Esquerra, Dreta, Amunt, Avall, Més ample… de la 0.6.2 s’han tret: l’editor està pensat per a pantalla tàctil i ratolí, i qui fa servir un altre accés no necessita editar la disposició (decisió de Marc, 7 de novembre de 2026). Tocar un botó i després una casella buida encara el porta allà, que és l’alternativa d’un sol toc per moure; canviar la mida només es pot fer arrossegant (W3C, 2023, criteri 2.5.7).

La 0.6.3 s’obté aplicant `tools/patch-0.6.3/patch063.py` sobre l’HTML de la 0.6.2 (commit `8e2b93d`):

```
python3 tools/patch-0.6.3/patch063.py UTAC_Keryx_v0.6.2_local.html UTAC_Keryx_v0.6.3_local.html
```

Validació (7 de novembre de 2026), Chromium amb Playwright a 1280 × 800 i 390 × 844: arrossegar Aturar sobre Mostrar els intercanvia; arrossegar la cantonada canvia la mida; una mida que solaparia un altre botó es rebutja amb el motiu; sense errors de JavaScript. No s’ha provat en dispositius tàctils reals.

## Canvis de la versió 0.6.2

- **Botons principals.** El grup Parlar, Aturar, Mostrar i Nou missatge incorpora «Esborrar paraula», que abans era un botó petit sota el missatge i se n’ha tret, i un botó nou, «Esborrar-ho tot» (paperera). «Esborrar-ho tot» buida el missatge; Desfer el recupera.
- **Posició dels botons principals.** Nova opció a Ajustos → Pantalla: els botons poden anar sota el missatge (com fins ara), en una columna a l’esquerra o en una columna a la dreta. En columna, Aturar i Mostrar, i Esborrar paraula i Esborrar-ho tot, comparteixen fila a mitja amplada; en columnes estretes, aquests quatre només mostren la icona, i el nom continua disponible per als lectors de pantalla. Sota el missatge, en mòbils en vertical, els botons ocupen dues files. En columna, el missatge guanya alçada.
- **Edició dels botons principals** (Ajustos → Pantalla). Una graella de 2 × 5 per a la columna lateral i una de 12 × 2 per a sota el missatge. Cada persona pot seleccionar un botó i moure’l, fer-lo més ample, estret, alt o baix, portar-lo a una casella buida, i triar quins botons es mostren. Els controls són botons, no arrossegament, perquè l’editor també es pugui fer servir amb teclat, escombratge o permanència. Moure un botó cap a un altre de la mateixa mida els intercanvia. Parlar sempre és visible i l’editor no deixa que cap altre botó l’iguali o el superi en superfície. Sense una disposició desada, s’usa la disposició per defecte, que s’adapta a la pantalla; si la personalitzada coincideix amb la inicial, no es desa. Les disposicions es desen al perfil i es validen en importar una còpia.
- **Parlar sempre és el botó més gran**, en totes les posicions i mides. En finestres baixes en horitzontal amb el panell obert, Parlar ocupa tota la primera fila (abans, una quarta part).
- **El marc de focus segueix el tema.** El contorn del camp actiu (per exemple, el missatge mentre s’escriu) i el ressaltat d’escombratge i permanència prenen el color principal del tema, en lloc d’un blau fix. Sobre els botons plens del color principal, el contorn pren el color del text del botó perquè es continuï veient. El contrast del color principal amb el fons és d’almenys 4,74:1 en els 33 temes, per sobre del mínim de 3:1 per a components de la interfície (W3C, 2023, criteri 1.4.11).
- **La finestra d’Informació es desplaça** en lloc de dividir-se en pàgines, com els ajustos. També el manual d’accés amb teclat i les llicències que s’hi obren.
- Textos nous en els sis idiomes; les traduccions a euskera, gallec, anglès i francès no han estat revisades per parlants nadius.

La 0.6.2 s’obté aplicant `tools/patch-0.6.2/patch062.py` sobre l’HTML de la 0.6.1 (commit `c85ac75`):

```
python3 tools/patch-0.6.2/patch062.py UTAC_Keryx_v0.6.1_local.html UTAC_Keryx_v0.6.2_local.html
```

### Validació de la 0.6.2 (7 de novembre de 2026)

Chromium amb Playwright a 1280 × 800, 640 × 400, 768 × 1024, 390 × 844, 360 × 640 i 740 × 360, amb les tres posicions dels botons: el document no es desplaça, cap botó principal no queda tallat, Parlar té més superfície que cada un dels altres cinc i no hi ha errors de JavaScript. Esborrar paraula i Esborrar-ho tot mantenen el cursor al missatge, i Desfer recupera el text esborrat. A l’editor s’ha comprovat l’intercanvi de botons, el bloqueig de solapaments i de botons que no hi caben, la regla de Parlar i que la disposició es manté després de recarregar; amb disposicions personalitzades, cap botó no queda tallat a 1280 × 800, 390 × 844, 740 × 360 i 360 × 640. L’opció es desa i es recupera en tornar a carregar. S’ha comprovat el marc de focus amb els temes Clar, Fosc, Rosa i Alt contrast, i que la finestra d’Informació té una sola pàgina amb desplaçament. Límits: no s’ha provat en dispositius reals ni amb lectors de pantalla.

W3C. (2023). *Web Content Accessibility Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

## Canvis de la versió 0.6.1

- **Pantalla fixa també amb el text ampliat.** En finestres baixes en horitzontal (mòbil de costat, o text al 200 % en un portàtil), el missatge queda a l’esquerra i el panell a la dreta. En finestres de menys de 520 px d’alçada, els botons del peu passen a la fila superior i cap botó no queda tallat.
- **Missatge llarg.** El quadre del missatge no creix: la lletra es redueix fins a 20 px perquè el text hi càpiga sencer. Si encara no hi cap, apareixen els botons «Línia amunt» i «Línia avall».
- **Més frases per pàgina en pantalles petites.** Dues columnes a partir de 260 px d’amplada i targetes més baixes; en mòbils, els botons Silenci i Mode privat pugen a la fila superior. A 360 × 640 hi caben 4 frases per pàgina (abans, 1); a 390 × 844, 10. Les respostes ràpides també es paginen quan no hi caben.
- **Panell inferior.** La barra tancada és clara, com l’oberta, i té la mateixa alçada. El botó d’amagar i mostrar té sempre la mateixa mida i és a l’extrem dret, de color verd fosc amb el text o la icona en blanc («Amagar panell» / «Mostrar panell» en pantalles amples; només la icona en pantalles de 1000 px d’amplada o menys).
- **Teclat físic.** El panell comença amagat quan hi ha un teclat físic. Cap API web no informa de si n’hi ha un, i per això s’usen dos indicis: un ratolí o un trackpad com a punter principal, o pulsacions reals al missatge sense un teclat de pantalla que ocupi part de la finestra. Si la persona torna a obrir o tancar el panell, l’app respecta aquesta tria durant la sessió. Amb escombratge o permanència, el panell no s’amaga.
- Textos nous en els sis idiomes; les traduccions a euskera, gallec, anglès i francès no han estat revisades per parlants nadius.

### Com s’ha fet la 0.6.1

Aquest repositori encara no conté les fonts de construcció (`build.py`, `src/`, proves) que descriuen les seccions següents. La 0.6.1 s’ha obtingut aplicant `tools/patch-0.6.1/patch061.py` sobre l’HTML construït de la 0.6.0, i el resultat és reproduïble:

```
python3 tools/patch-0.6.1/patch061.py UTAC_Keryx_v0.6.0_local.html UTAC_Keryx_v0.6.1_local.html
```

Quan les fonts s’afegeixin al repositori, aquests canvis s’hi han de portar.

### Validació de la 0.6.1 (7 de novembre de 2026)

Chromium amb Playwright, obrint el fitxer local, a 1280 × 800, 640 × 400 (equivalent a 1280 × 800 amb text al 200 %), 768 × 1024, 390 × 844, 360 × 640 i 740 × 360, amb un missatge de 274 caràcters i les vistes Respostes, Frases i Teclat: el document no es desplaça, cap panell de conversa no té desplaçament i no hi ha errors de JavaScript. S’ha comprovat que el panell s’amaga en escriure amb tecles reals en un dispositiu tàctil emulat, que el teclat de pantalla no l’amaga i que, després de tornar-lo a obrir, no s’amaga de nou. Límits: no s’ha provat en dispositius reals ni amb teclats Bluetooth, ni amb lectors de pantalla; amb text al 200 %, algunes tecles del teclat de pantalla fan una mica menys de 24 px d’amplada; el missatge que no hi cap pot mostrar una línia tallada a la part superior.

## Canvis de la versió 0.6.0

- El panell inferior es recull en una franja de 40 px. El missatge ocupa l’espai alliberat; la franja permet tornar al mateix apartat. Es pot accionar amb ratolí, tacte, teclat i els modes d’accés de l’aplicació.
- Camp de missatge buit, sense text de suggeriment. Els esborranys desats es conserven.
- Normalització de majúscules idèntica a `forSpeech` de LECAA Docs abans d’enviar paraules o missatges a qualsevol motor de veu. El text visible i desat es conserva. Els noms de les lletres es tracten de manera literal.
- Tots els ajustos de cada apartat són en una única pàgina amb desplaçament vertical. La capçalera, les pestanyes i el peu es mantenen visibles. Tab i l’escombratge porten el control enfocat a la zona visible; Re Pàg i Av Pàg desplacen el contingut.
- Ajustos → Escriptura → Llegir mentre escric: tres caselles independents per llegir cada lletra, cada paraula en prémer espai i cada frase en fer punt, interrogació, exclamació o Intro. Es poden activar totes o cap; inicialment estan desactivades. Es desen per perfil i s’inclouen en les còpies de seguretat.
- Les lectures d’escriptura segueixen una cua sense superposar-se. Aturar i Esc les cancel·len; Parlar té prioritat. Funciona amb el teclat físic i el de pantalla. Enganxar, desfer i inserir una frase desada no activen l’eco d’escriptura.
- Etiquetes noves en els sis idiomes de l’aplicació. Es conserven els 33 temes i el catàleg de veus.

## Canvis de la versió 0.5.0

- 33 temes: els tres originals (clar, fosc i alt contrast) més 15 paletes clares i 15 de fosques.
- Ajustos → Pantalla → Tema: desplegable amb desplaçament intern i 33 captures reals de la mateixa pantalla de l’aplicació. Cap dependència de xarxa per a les miniatures.
- Una sola parada de Tab; fletxes, Inici, Fi, Re Pàg, Av Pàg i cerca per primeres lletres; Intro/Espai confirma, Esc/Tab cancel·la. L’opció activa i la seleccionada es distingeixen. L’escombratge porta la casella activa a la part visible de la llista.
- Persistència per perfil, importació/exportació de totes les paletes i compatibilitat amb els tres identificadors originals. El manual de teclat incorpora el selector en els sis idiomes.
- Contrast mínim calculat de 4,64:1 en les parelles de text comprovades; no equival a una certificació WCAG ni a una prova amb lectors de pantalla.

## Funcions de la versió 0.4.0 conservades

- Selector com el de LECAA Docs: globus, codi curt, menú amb el nom de cada llengua i marca de selecció. Navegació amb fletxes, Inici, Fi, Intro, Espai, Tab i Esc.
- Sis idiomes, en aquest ordre: Català, Castellano, Euskara, Galego, English i Français. No s’afegeixen idiomes a partir de les veus del navegador.
- Ajustos → Veu i llengües → Idiomes del menú: selecció per perfil. Sempre en queda un d’actiu. Desactivar l’idioma actual selecciona el primer dels que continuen activats.
- Canvi de menús i de veu sense perdre el missatge. Veu desada per idioma. Les frases personals no es tradueixen automàticament; el banc inicial continua contenint 90 exemples en català i castellà.
- Mateix catàleg Piper que LECAA Docs: Ona; Davefx i les dues veus Sharvard; Maider i Antton; Davefx i Tugão com a alternatives explícites per al gallec. Anglès i francès utilitzen les veus del sistema o del navegador.
- Descàrrega amb progrés i cancel·lació. Publicació atòmica del model i la configuració a IndexedDB. Síntesi en un worker, sense enviar el missatge a cap servidor. Les descàrregues no s’inclouen als JSON de perfils.
- Les veus castellanes del navegador es limiten a `es` i `es-ES`. Les alternatives gallegues mai no es trien automàticament.

## Construcció

L’HTML resultant inclou els recursos visuals, fonts, dades, codi i motor JavaScript. El model i els binaris WASM es descarreguen només quan s’instal·la una veu.

1. Python 3 amb `fonttools`; Node.js per a les proves i la regeneració opcional del worker.
2. `python3 build.py` genera `index.html`, l’HTML local i `dist/index.html`.
3. `node test-core.cjs`, `node test-languages.cjs`, `node test-themes.cjs` i `node test-writing.cjs` executen les comprovacions.
4. `npm ci --ignore-scripts` instal·la les dependències fixades si cal modificar el worker o les traduccions.
5. `node build-i18n.cjs` regenera els diccionaris a partir dels fitxers de traducció, inclòs `translations-v06.json`.
6. Worker: `node_modules/.bin/esbuild src/neural/voice.worker.ts --bundle --platform=browser --format=iife --target=es2020 --external:fs --external:path --outfile=src/neural/worker.bundle.js --legal-comments=inline`.
7. Catàleg: `node_modules/.bin/esbuild src/neural/catalog.ts --bundle --format=iife --global-name=KeryxVoiceCatalog --outfile=src/neural/catalog.js`.

Les referències `fs` i `path` del glue Emscripten corresponen a la branca Node, que no s’executa al worker del navegador.

## Validació de la versió 0.6.0

Resultats i límits a `QA_writing_results.md`. `src/writing.js` conté les funcions de text i la cua; `src/writing-ui.js`, la integració amb els dos teclats i els ajustos. `make-writing-qa.py` crea, després de construir, una prova separada amb registre de les peticions de veu i dues variants: motor simulat i Piper real. Les pàgines de prova no s’inclouen en l’HTML distribuït.

## Validació de temes del 7 de novembre de 2026

Resultats i límits a `QA_themes_results.md`. Les captures de `assets/theme-previews` corresponen a la mateixa pantalla de 1024 × 640, reduïda a 288 × 180. La previsualització serveix per comparar colors; no representa el contingut personal ni les preferències de mida de cada perfil. `build.py` exigeix les 33 captures; `--without-previews` només serveix per preparar captures noves, no per distribuir l’aplicació.

## Validació anterior del 7 de novembre de 2026

- Proves de dades, importació, compatibilitat de còpies, teclat, cancel·lació i selecció de veus: correctes.
- Les set veus reals han generat mostres d’àudio no silencioses des d’IndexedDB, amb totes les crides de xarxa bloquejades per la prova. Resultats a `QA_neural_results.txt`.
- Cancel·lació d’una descàrrega d’Antton sense donar per instal·lat cap model parcial; la descàrrega posterior s’ha completat.
- Aturar durant la preparació impedeix que la veu comenci després.
- Menú amb sis idiomes; reducció a català i castellà; persistència després de recarregar; protecció de l’últim idioma; conservació del text i de la veu escollida per idioma: comprovats a la interfície.
- Pantalla principal 1363 × 936 i panells 1024 × 600, 820 × 1180 i 390 × 844: dimensions del document iguals al viewport i cap control visible fora de pantalla en les vistes comprovades.

Les proves de navegador s’han fet amb Chromium en una previsualització HTTP. L’entorn de prova no permet obrir `file://`; no s’ha fet una prova directa del fitxer des del disc ni una validació en tots els sistemes operatius. S’ha mantingut la càrrega de blobs i WASM utilitzada per l’edició HTML única de LECAA Docs. Les traduccions noves a euskera, gallec, anglès i francès no han estat revisades per parlants nadius. No s’ha fet una avaluació perceptiva o clínica de les veus.

## Crèdits i llicències

Codi d’aquesta versió: GPL-3.0-or-later. El catàleg, la fonemització i l’estructura del worker deriven de LECAA Docs, UTAC, commit `c1f870a65a35573ed66fc597834a7376269b9fae`. Adaptació a Keryx: emmagatzematge transaccional, cancel·lació, selecció de parlant Sharvard, selecció d’idiomes per perfil i integració amb l’editor. Les identitats gràfiques UTAC i Keryx es conserven amb la seva atribució.

- LECAA Docs: https://github.com/utacub/lecaa_docs/tree/c1f870a65a35573ed66fc597834a7376269b9fae
- Normalització de majúscules i noms de les lletres, consultats el 7 de novembre de 2026: https://github.com/utacub/lecaa_docs/blob/main/src/speech/text.ts (blob `129e5adaafb818cc2e888a419ec267db8b73e6c8`) i https://github.com/utacub/lecaa_docs/blob/main/src/letters.ts (blob `a7323ef5652ef3959f241ade709ad2d89efa75e9`). Es conserva l’atribució GPL a `src/writing.js`; la cua i la integració són pròpies de Keryx.
- ONNX Runtime Web 1.18.0, Microsoft, MIT: `src/neural/LICENSE-ONNX.txt`.
- Glue de @diffusionstudio/vits-web 1.0.3 i @diffusionstudio/piper-wasm 1.0.0: MIT, segons les declaracions dels paquets i el codi original. https://github.com/diffusionstudio/vits-web i https://github.com/diffusionstudio/piper-wasm
- espeak-ng / fonemitzador: GPL-3.0. Llicència GPL completa a `src/neural/LICENSE-LECAA-Docs.txt` i dins de l’HTML.
- Ona: UPC Festcat, CC BY-SA 3.0 ES. Davefx: CC0. Sharvard: CC BY 3.0. Maider i Antton: CC BY 4.0. Tugão: CC0. El catàleg conté els enllaços originals de cada model i la interfície els mostra abans de descarregar.
- DejaVu Sans: llicència inclosa als recursos i a l’HTML.

Els perfils, les converses de prova i les veus descarregades durant la validació no formen part del fitxer distribuït.

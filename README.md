# UTAC Keryx 0.6.1

Comunicador alfabètic d’UTAC amb pantalla principal fixa, panell inferior minimitzable i ajustos amb desplaçament vertical. Obriu `UTAC_Keryx_v0.6.1_local.html` amb un navegador. No necessita servidor ni clau d’API. Les descàrregues de veus necessiten Internet la primera vegada.

## Aplicació web i fitxer local

- Aplicació: https://utacub.github.io/keryx/
- Edició descarregable: [`UTAC_Keryx_v0.6.1_local.html`](UTAC_Keryx_v0.6.1_local.html).
- La web i l’HTML descarregable contenen la mateixa aplicació. Les dades de cada navegador i origen són independents; per traslladar frases i ajustos, feu servir Ajustos → Dades → Exportar/Importar còpia.
- Publicació amb GitHub Pages des de la branca `main`, carpeta arrel. `index.html` és autònom; `.nojekyll` evita el processament Jekyll.
- Per publicar una modificació: executeu `python3 build.py`, les proves indicades més avall i incorporeu els fitxers resultants a `main`. La construcció actualitza `index.html`, l’HTML descarregable i la previsualització `dist/index.html`.

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

# UTAC Keryx 0.6.0

Comunicador alfabètic d’UTAC amb pantalla principal fixa, panell inferior minimitzable i ajustos amb desplaçament vertical. Obriu `UTAC_Keryx_v0.6.0_local.html` amb un navegador. No necessita servidor ni clau d’API. Les descàrregues de veus necessiten Internet la primera vegada.

## Aplicació web i fitxer local

- Aplicació: https://utacub.github.io/keryx/
- Edició descarregable: [`UTAC_Keryx_v0.6.0_local.html`](UTAC_Keryx_v0.6.0_local.html).
- La web i l’HTML descarregable contenen la mateixa aplicació. Les dades de cada navegador i origen són independents; per traslladar frases i ajustos, feu servir Ajustos → Dades → Exportar/Importar còpia.
- Publicació amb GitHub Pages des de la branca `main`, carpeta arrel. `index.html` és autònom; `.nojekyll` evita el processament Jekyll.
- Per publicar una modificació: executeu `python3 build.py`, les proves indicades més avall i incorporeu els fitxers resultants a `main`. La construcció actualitza `index.html`, l’HTML descarregable i la previsualització `dist/index.html`.

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

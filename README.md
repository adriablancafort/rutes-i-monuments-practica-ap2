# Pràctica GCED-AP2 2024 · Rutes i monuments



Llegeix les entrades, pregunta què fer i crida les funcions adequades.

## Llibreries
Per executar el projecte calen les següent llibreries::

- typing
- dataclasses
- bs4
- requests
- re
- lxml
- gpxpy
- staticmap
- scikit-learn
- scipy
- numpy
- networkx
- simplekml
- haversine
- math

## Instalació i execució

Per instalar aquest projecte cal seguir els següents passos en ordre:
1: Descomprimir el zip
2: Instalar totes les llibreries especificades en requirements.txt
3: Executar el main.py -> python3 main.py
4: Intereccionar amb la consola seguint les instruccions donades pel programa

## Objectiu del projecte

Aquest projecte té com a objectiu ajudar els senderistes a trobar els camins més curts des del punt del mapa on estan fins el monoment important de la zona més proper.

## Obtenció i neteja de les dades    

Les dades dels monuments s'obtindran a través de [Catalunya Medieval](https://www.catalunyamedieval.es/). El codi localitzat a monuments.py scrapeja una a una les pàgines d'aquesta web, estreu les localitzacions i informació rellevant respecte el monument i la guarda a un fitxer txt anomenat "monuments.dat". Si aquest fitxer està creat en la carpeta de camí relatiu "../" a monuments.py, la funció no torna a escrapejar els monuments, sinó que els llegeix del fitxer. Això evita pèrdues de temps.

Per aconseguir les dades sobre les rutes que els senderistes poden seguir escrapejem una pàgine web de senderisme:[OpenStreetMap](https://www.openstreetmap.org/). La funció "download_segments" localitzada a segments.py fa això. De les dades extrau el temps, i coordenades.

Finalment, ens hem adonar que les dades proporcionades tenen bastants errors. Afortunadament aquests errors són només errors del GPS no fucionant o de bugs en el sistema. Això vol dir que tots els errors venen de "steps" que són físicament impossibles (la persona s'ha mogut massa ràpid i no s'ha mogut). Per això, com a mètode de filtrat de dades, eliminem un segment del conjunt de dades si: Hi ha més de 15 segons entre els dos costats del segment, hi ha més de 500m entre els dos extrems. El temps entre dos segments és molt petit (no s'ha mogut). Això funciona ja que el les dades donades són extretes cada "X" segons, o sigui en intervals de freqüència constant. Això fa que qualsevol cosa que no sigui previsible vol dir que el GPS ha funcionat malament.


## Idea general sobre la implementació

La idea de l'algorísme és la segúent: Un cop obtingues les dades creem un graph que modelitza totes les rutes que es poden extraure. Amb el graph creat surgeix el problema de que és massa gran i la majoria d'arestes són molt petites. Per arreglar això fem un algorísme de clustering per ajuntar totes els vèrtexs a l'esapai en els vèrtex més significatius. Un cop tenim aquests vèrtexs del clúster creem un graph representatiu de l'anterior usant els vèrtexs del clúster. Aquest serà el graph que usarem per obtenir el camí final usant un Djikstra. L'excursionista pot començar en un punt que no és del graph, llavors les direccions indicades pel programa serà com arribar al punt més proper del monument desitjat que està al graph començant des del node del graph més proper al punt de principi.


## Esquelet del projecte

### mòdul `segments.py`

### mòdul `graphmaker.py`

### mòdul `viewer.py`

### mòdul `monuments.py`

### mòdul `routes.py`

### mòdul `main.py`


## Fonts d'informació


- [Lliçons de fitxers en Python](https://lliçons.jutge.org/python/fitxers-i-formats.html)

- [Tutorial de NetworkX](https://networkx.github.io/documentation/stable/tutorial.html)

- [Tutorial de Requests](https://realpython.com/python-requests/)

- [Documentació de BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

- [Documentació de simplekml](https://simplekml.readthedocs.io/en/latest/)

- [Documentació de haversine](https://pypi.org/project/haversine/)

- [Documentació de gpxpy](https://github.com/tkrajina/gpxpy)

- [Google Maps](https://github.com/adriablancafort/rutes-i-monuments-practica-ap2.git)
## Indicacions


## Autors

- Eloi Pagès 
- Adrià Blancafort

Algorísmia i programació 2
# calcul-parlamentare
Calculator pentru numărul de mandate obținute de candidați în alegerile parlamentare, conform legii 208/2015

> python tally.py [mandate] [voturi]

##### Mandate
Fișier .csv care conține numărul de mandate pe circumscripție, fiecare rând fiind sub forma
</br>
[Circumscripție], [număr mandate] </br>
Vezi mandate_cdep.csv pentru exemplu

##### Voturi
Fișier .csv care conțione numărul de voturi, fiecare coloană fiind sub forma
</br>
[Partid] </br>
[Voturi circumscripție 1] </br>
[Voturi circumscripție 2] </br>
... </br>
[Voturi circumscripție n] </br>
</br>
sau
</br>
[Candidat Independent] </br>
-1 </br>
... </br>
-1 </br>
[Voturi în circumscripția în care candidează] </br>
-1 </br>
... </br>
-1 </br>
Vezi cdep2016.csv pentru exemplu

##### Legea 208/2015 privind alegerea Senatului și Camerei Deputaților
http://www.roaep.ro/legislatie/wp-content/uploads/2015/12/Lege-nr.-208-2015-actulizare-22-11-2015.pdf

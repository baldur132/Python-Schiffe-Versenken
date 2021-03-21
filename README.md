# Python-Schiffe-Versenken
***Gruppe 1*** <br>
Schiffe Verseken in Python mit einem Command Line Interface

## Features
 - 10x10 Felder Spielbrett
 - Interaktion durch CLI
 - Singerplayer mit Computer Gegener
 - 2 Spieler Multiplayer
 - Automatisches Speichern in einer Datei
## Spielregeln: 
### Vorbereitung
 1. Die Schiffe dürfen nicht aneinander stoßen.
 2. Die Schiffe dürfen nicht über Eck gebaut sein oder Ausbuchtungen besitzen.
 3. Die Schiffe dürfen auch am Rand liegen.
 4. Die Schiffe dürfen nicht diagonal aufgestellt werden.
 5. Jeder verfügt über insgesamt zehn Schiffe (in Klammern die Größe):
     - ein Schlachtschiff (5 Kästchen)
     - zwei Kreuzer (je 4 Kästchen)
     - drei Zerstörer (je 3 Kästchen)
     - vier U-Boote (je 2 Kästchen)

### Spielverlauf
 - Der *Schießende* gibt eine Koordinate an, an der er feuert
 - Der *Beschossense* sieht auf seinem Brett und antwortet *Wasser*, *Treffer* oder *versenkt*
 - Ein Schiff gilt als *versenkt*, wenn alle Felder des Schiffes getroffen wurden
 - Der *Schießende* notiert dies in seinem zweiten Brett
 - Der *Beschossene* markiert die Treffer, um zu sehen, wann ein Schiff *versenkt* ist
 - Weiterer Fortgang: Die Rollen von dem *Schießenden* und *Beschossenen* wechseln sich bis bei einem alle Schiffe *versenkt* sind
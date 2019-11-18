# Software für Gefragt - Gejagt: Junghacker\*innen Edition

* n0emis -> backend, python
* Niklas -> frontend, vanillajs (?)

Gerne auch weitere Leute einbringen, besonders die, die Websites hübsch machen können mit fancy Animationen!

IPC via Eel-Library

Contributions: Pullrequest!

## Generelle Datenmodelle

Import und Export von Daten: JSON-serialisiert

Backend ist die single source of truth, das Frontend der slave.

Vom Backend werden die Daten aus einem Order eingelesen, sie liegen im dokumentierten JSON-Format vor. Ein Export soll ggfs. ebenfalls erfolgen, dafür wird aber eine neue Datei mit Zeitstempel angelegt, aus der widerrum gelesen und damit der State recovered werden kann.

### Team und Spieler

Spieler und ihre Properties sind Objekte eines Teams

```js
{
	"players": [
		{
			"name": "Vorname?Nickname",
			"level": 5,	// value from 1-10
			"played": false,
			"points": 0,
			"won": false,	// Jagdrunde gewonnen?
			"rounds": []
		}	
	],
	"name": "Teamname"
}
```

Properties wie Punktzahl des gesamten Teams müss errechnet werden, basierend auf "won" == true und points.

### Fragen

Fragen sind für das tool readonly. Bestenfalls sollte es die bereits gespielten Fragen (zumindest ihre IDs) mit den jeweiligen Runden assoziiert abspeichern, damit dieselbe Frage nicht mehrfach auftaucht. Bereits vor einem Spiel sollen für einen Spieler die besten Fragen basierend auf dem level und per Zufall ausgewählt werden. Die Antwortmöglichkeiten müssen in jedem Fall geshuffled werden. 

Es werden nur 3 Antwortmöglichkeiten gespielt, wenn das level der Spielenden mindestens 5 unter dem level der Frage liegt.

```js
[
	{
		"text": "Wie lautet die Frage?",
		"correctAnswer": "So!",
		"wrongAnswers": ["So nicht!", "So auch nicht!", "So schonmal gar nicht! ;)"],
		"level": "5",	// value from 1-10
		"category": "Kategorie"
	}
]
```

### Runden

Die Runden spezifizieren die einzelnen Spielrunden, von denen die Spieler teil waren. Ihre IDs werden den arrays der Spieler hinzugefügt und die Spieler den Runden hier - cross-referencing macht einiges leichter :)

Die Generation findet, wie bereits oben angemerkt, komplett vor der tatsächlichen Runde statt, aber nicht so, als dass durch die Spielleitung Einfluss genommen werden kann.

```js
[
	{
		"level": 5,	// most skilled player (available) team
		"players": [],
		"questions": [],
		"type": 1, 	// 1=Schnellrate, 2=Jagd, 3=Finale
		"won": false,
		"chaser": "Jägername", 	// null bei 1
		"value": null	// null bei 1, player[points] oder suggested bei 2, Teampunktzahl bei 3,
		"suggestedValues": [5, 20], // nur bei 2, das niedrigere und das höhere Angebot des Jägers
	}
]
```

## Funktionalitäten, wenn nicht bereits beschrieben

* Viewer-Fenster
	* sichtbar für das Publikum, die Spielenden und die Moderation
	* Schnellraterunde
		* Frage, aktuelle Punktzahl des Spielenden
			* +1 bei korrekter Antwort
	* Jagdrunde
		* Frage + Antwortmöglichkeiten
		* Gewinnleiter
			* Zu Beginn mit Auswahl, ob die durch den Jäger abgegebenen Angebote angenommen werden oder ob mit Punktzahl aus Schnellraterunde gespielt wird
			* Der Jäger legt seine Angebote fest, sie müssen durch den Admin eingegeben werden
			* Bei höherem Angebot verliert der Spielende 1 Feld Vorsprung
			* Bei niedrigerem Angebot erhält der Spielende ein weiteres Feld Vorsprung
			* Bei Ausschlagung der Angebote gibt es 2 Felder Vorsprung
			* Jäger und Spieler werden gleichzeitig angezeigt, Jäger in einer stark abgegrenzten Farbe.
			* Von oben nach unten
		* Eingeloggte Antwort des Spielers wird farblich hervorgehoben
		* Danach wird die korrekte Antwort in grün angezeigt
		* Zum Schluss wird die Antwort des Jägers eingerahmt
		* Nach Antwort von einer Partei = 5 Sekunden Restzeit für die andere
			* Akkustisch hervorheben und als Progressbar anzeigen
	* Finalrunde
		* Voneinander abgegrenzte Stufen, wachsen mit jeder richtigen Antwort
		* Spieler starten mit Punkten Vorsprung entsprechend der Anzahl derer Spieler, die die Jagdrunde gewonnen haben
		* Durch dieselbe abgegrenzte Farbe wird der Stand des Jagenden angezeigt
		* Es wird nacheinander gespielt; erst Spieler, dann Jäger
		* Richtige Antwort +1
* Admin-Fenster
	* Sieht die aktuelle Frage + alle zugehörigen Informationen
	* Entscheidet ob richtig oder falsch, am besten per Tastatur
	* gibt für Jagdrunde Angebote schnell ein, nachdem sie geäußert wurden
	* muss hauptsächlich funktional sein und effizient nutzbar
	* Nächste Frage
	* Finalrunde
		* Uhr anhalten
* Buzzer
	* Jagdrunde
		* 4x Antwortmöglichkeit einloggen für Spieler und auch Jäger
		* via Tastatur, idealerweise pro Gerät dieselben Tasten, damit nicht für die andere Partei eingeloggt werden kann
	* Finalrunde
		* Nur Kandidaten erhalten Buzzer
		* 1 pro Person
		* buzzen, bevor Antwort mündlich gegeben wird
		* Ausgabe des Spielernamens per TTS?
* Extra
	* Ausgabe der Frage und Aktionen in einem extra Fenster für Einbindung in den Livestream/der Aufzeichnung? Overlay des Kamerabildes? Chromakey? Kann das VOC sowas?

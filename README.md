# gefragt-gejagt-studio

Die Software für "Gefragt - Gejagt: Junghacker\*innen Edition" für den Einsatz auf dem 36. Chaos Communication Congress! Mithelfen unter https://nwng.eu/36c3-gg oder in diesem Repository!

"Gefragt - Gejagt" wird in Deutschland für die ARD von itv produziert. Dieses Projekt hat keine Verbindungen zu den gennanten Organisationen und wird nur für ein nicht-kommerzielles Community-Event verwendet.

## Beitragen

Die genaue, geplante Funktionsweise der Software ist im [RFC][RFC.md] dokumentiert - der RFC wird ständig erweitert, sobald Entscheidungen getroffen wurden, die noch nicht darin dokumentiert sind. Alle Beiträge sind willkommen!

## Setup

Um ein VirtualEnv mit allen Abhängigkeiten zu erstellen, führe folgendes aus:

```
python -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Server starten

Um den Server zu starten, benutze `python -m gefragt_gejagt`. Hierzu musst du dich allerding im VirtualEnv befinden: `source .venv/bin/activate` Wenn du Informationen zu den verfügbaren Optionen brauchst, verwende den optionalen Parameter `-h`.

## Aufbau
Zur Verknüpfung zwischen dem Python-Backend und dem Frontend nutzen wir die Bibliothek Eel. Mehr Infos dazu unter
https://github.com/samuelhwilliams/Eel/

## License
This project is licensed with the [European Union Public Licence (EUPL) v1.2](https://joinup.ec.europa.eu/news/understanding-eupl-v12)

The new version 1.2 of the European Union Public Licence (EUPL) is published in the 23 EU languages in the EU Official Journal: [Commission Implementing Decision (EU) 2017/863 of 18 May 2017 updating the open source software licence EUPL to further facilitate the sharing and reuse of software developed by public administrations](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2017.128.01.0059.01.ENG&toc=OJ:L:2017:128:FULL) ([OJ 19/05/2017 L128 p. 59–64](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2017.128.01.0059.01.ENG&toc=OJ:L:2017:128:FULL)).

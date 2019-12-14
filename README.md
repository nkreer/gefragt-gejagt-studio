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
Zur verknüpfung zwischen dem Python-Backend und dem Frontend nutzen wir die Bibliothek Eel. Mehr infos dazu unter
https://github.com/samuelhwilliams/Eel/

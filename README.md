# Vokabeltrainer – Community-Katalog

Die Vokabeln des Vokabeltrainers, gepflegt von der Community. Der Trainer lädt diesen Katalog aus dem Branch `main`;
Änderungen kommen per Pull Request nach `develop` und von dort gesammelt per Pull Request nach `main`.

## Aufbau

```
languages.yaml            Sprachen: Basissprachen (Übersetzungen) und lernbare Zielsprachen
topics.yaml               Themen mit Icon und Namen je Basissprache
words/<sprache>/<thema>.yaml
                          Vokabeln einer Zielsprache, eine Datei je Thema (z. B. words/en/food.yaml)
schema/                   JSON-Schemas der drei Dateiarten
scripts/validate.py       Prüft den Katalog – lokal und in der CI bei jedem Pull Request
```

Eine Vokabel sieht so aus:

```yaml
- id: "apple"                   # stabile Kennung, eindeutig je Sprache – nie ändern
  lemma: "apple"                # die Vokabel
  pos: noun                     # Wortart
  level: A1                     # Niveau nach GER: A1 … C2
  ipa: "/ˈæp.əl/"               # Lautschrift, optional
  example: "I eat an apple every day."
  translations:                 # je Basissprache; die erste ist die Hauptübersetzung
    de: ["der Apfel", "Apfel"]
  example_translations:
    de: "Ich esse jeden Tag einen Apfel."
```

Mitmachen: siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Umfang

**Englisch (`words/en/`)** deckt den Grundwortschatz von A1 bis B2 ab: rund 3.700 Vokabeln
(A1 ≈ 900, A2 ≈ 1.100, B1 ≈ 880, B2 ≈ 810). Die aktuellen Zahlen gibt `scripts/validate.py` aus.

- **Niveaus** folgen dem Gemeinsamen Europäischen Referenzrahmen (GER) und richten sich danach, wie früh ein Wort
  üblicherweise gelernt wird.
- **Übersetzungen, Beispielsätze und Lautschrift** (britisches Englisch) sind eigene Inhalte des Katalogs, nicht aus
  einem Wörterbuch übernommen.
- **Wortarten:** Gibt es ein Wort in mehreren Wortarten, gibt es nur dann getrennte Einträge, wenn sich die
  deutsche Bedeutung unterscheidet (`light-noun` „das Licht“, `light-adjective` „hell, leicht“). Varianten mit
  gleicher Übersetzung sind zusammengefasst, z. B. die Farbe „black“ nur als Adjektiv.
- **Themen:** Jede Vokabel steht in genau einem Thema aus `topics.yaml`. Wörter ohne konkreten Sachbereich
  (z. B. „aspect“, „amount“) liegen unter *Allgemeine Begriffe*, Funktionswörter wie Artikel, Pronomen und
  Präpositionen unter *Funktionswörter*.

Wortschatz über B2 hinaus (C1/C2) ist willkommen; das Niveau bitte nach GER angeben.

## Lizenz

- **Vokabeldaten** (`words/`, `languages.yaml`, `topics.yaml`):
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de), siehe [LICENSE-DATA](LICENSE-DATA).
  Weiterverwendung ist erlaubt, auch kommerziell, mit Namensnennung („Vokabeltrainer – Community-Katalog“ mit Link
  auf dieses Repository) und unter derselben Lizenz für veränderte Daten.
- **Code und Werkzeuge** (`scripts/`, `schema/`, `.github/`, Dokumentation): MIT, siehe [LICENSE](LICENSE).

## Lokal prüfen

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/validate.py
```

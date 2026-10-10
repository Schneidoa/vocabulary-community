# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Worum es geht

Reiner Datenkatalog (YAML) für einen Vokabeltrainer – kein App-Code. Der Trainer importiert den Stand von `main`.
Sprache des Repos (Doku, Kommentare, Commit-Messages, Validator-Ausgaben) ist Deutsch.

## Befehle

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/validate.py                      # Schema, doppelte IDs/Lemmas, Sprach- und Themenverweise; gibt Zahlen je Niveau aus
.venv/bin/python scripts/validate.py --base origin/develop # zusätzlich: Warnung bei entfernten/umbenannten IDs ggü. dem Ref
```

Es gibt keine Tests außer dem Validator. Die CI (`.github/workflows/validate.yml`) ruft ihn bei Pull Requests mit
`--base origin/<Ziel-Branch>` auf.

## Aufbau und Zusammenhänge

- `languages.yaml`: Sprachen mit `base` (Übersetzungssprache, derzeit nur `de`) und `learnable` (Zielsprache: `en`, `fr`).
- `topics.yaml`: Themen; der `slug` ist zugleich der Dateiname unter `words/<sprache>/<slug>.yaml`. Themen-Namen nur
  für Basissprachen.
- `words/<sprache>/<thema>.yaml`: Liste von Vokabeln. Der Ordnername muss ein `code` aus `languages.yaml` sein,
  der Dateiname ein `slug` aus `topics.yaml`.
- `schema/*.schema.json`: JSON-Schemas (Draft 2020-12) für die drei Dateiarten; `scripts/validate.py` wendet sie an
  und prüft darüber hinaus Querverweise: `id` eindeutig je Sprache (über alle Themen-Dateien), `(lemma, pos)` eindeutig
  je Sprache, Schlüssel in `translations`/`example_translations` müssen Basissprachen sein.

## Regeln für Vokabeldaten (Details in CONTRIBUTING.md)

- **`id` nie ändern, löschen oder wiederverwenden** – Lernfortschritt der Nutzer hängt daran. Tippfehler nur in
  `lemma` korrigieren. Format `^[a-z0-9]+(-[a-z0-9]+)*$`; bei gleichem Wort in mehreren Wortarten mit Suffix
  (`light-noun`, `light-adjective`) – getrennte Einträge nur, wenn sich die deutsche Bedeutung unterscheidet.
- Einträge je Datei **alphabetisch nach `id`** sortiert (wird vom Validator nicht geprüft, aktuell aber überall
  eingehalten). Jede Vokabel steht in genau einem Thema.
- Alle Textwerte in `"…"` (YAML-Fallen wie `no`/`on`); nur `pos` und `level` ohne Anführungszeichen.
- `translations.de` ist eine Liste, die erste ist die Hauptübersetzung; deutsche Nomen mit Artikel (`"der Apfel"`).
- Französisch: Nomen im `lemma` mit bestimmtem Artikel (`"la pomme"`), bei Elision mit Geschlecht (`"l'arbre (m.)"`,
  `"les vacances (f. pl.)"`); `id` ohne Artikel und ohne Akzente (`oeil`); Adjektive in männlicher Form.
- Lautschrift: Englisch britisch, Französisch Standardfranzösisch. Beispielsätze kurz, alltäglich, mit der Vokabel
  in genau dieser Form.
- Inhalte (Übersetzungen, Beispiele, IPA) sind eigene Inhalte – nichts aus Wörterbüchern übernehmen und keine
  externen Wortlisten als Quelle in Repo, Commits oder PRs nennen.
- Bei größeren Ergänzungen die Zahlen im Abschnitt „Umfang“ der README an die Ausgabe des Validators anpassen.

## Branches

Pull Requests gehen gegen `develop`; `main` ist geschützt und wird nur per PR von `develop` aktualisiert.
Lizenz: Daten CC BY-NC-SA 4.0 (`LICENSE-DATA`), Code/Schemas/Doku MIT (`LICENSE`).

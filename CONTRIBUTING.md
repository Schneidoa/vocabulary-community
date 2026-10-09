# Mitmachen

Danke, dass du den Katalog verbesserst! Jede Änderung kommt als Pull Request gegen `develop`. Die CI prüft sie
automatisch; nach Review und Merge sammelt sich die Änderung in `develop`.

`main` ist der veröffentlichte Stand, den der Trainer importiert. Er ist geschützt und wird nur per Pull Request
von `develop` nach `main` aktualisiert.

## Lizenz deiner Beiträge

Mit deinem Pull Request

1. stellst du deine Beiträge unter die Lizenzen des Katalogs: Vokabeldaten unter CC BY-NC-SA 4.0, Code unter MIT
   (siehe [README](README.md#lizenz));
2. räumst du dem Maintainer dieses Repositorys (Daniel Schneider) zusätzlich ein einfaches, unbefristetes,
   unwiderrufliches und nicht auf nichtkommerzielle Zwecke beschränktes Recht ein, deine Beiträge zu nutzen, zu
   bearbeiten und weiterzugeben – insbesondere im Vokabeltrainer selbst, auch wenn dieser kostenpflichtig oder
   werbefinanziert angeboten wird. Dieses Recht ist übertragbar, etwa an einen künftigen Betreiber des Trainers;
3. bestätigst du, dass du die Rechte an deinen Beiträgen hast. Übernimm deshalb keine Wortlisten, Übersetzungen
   oder Beispielsätze aus Wörterbüchern oder anderen urheberrechtlich geschützten Quellen.

## Vokabeln hinzufügen

1. Passende Datei unter `words/<sprache>/` wählen, z. B. `words/en/travel.yaml`. Gibt es kein passendes Thema,
   zuerst eins in `topics.yaml` anlegen.
2. Eintrag ergänzen, alphabetisch nach `id` einsortiert (das vermeidet Konflikte zwischen Pull Requests).
3. `python scripts/validate.py` ausführen oder auf die CI warten.

## Regeln

### Die `id` ist heilig

Der Lernfortschritt aller Nutzer hängt an der `id`. Deshalb:

- Eine `id` wird beim Anlegen vergeben und danach **nie geändert oder wiederverwendet**.
- Form: Kleinbuchstaben, Ziffern und Bindestriche, abgeleitet von der Vokabel: `apple`, `good-morning`.
- Gibt es dieselbe Vokabel mit mehreren Wortarten, hängt die Wortart an: `light-noun`, `light-adjective`.
- Tippfehler korrigierst du in `lemma`, nicht in der `id`.
- Löschen nur, wenn ein Eintrag wirklich falsch ist – die CI warnt bei entfernten IDs.

### Text immer in Anführungszeichen

YAML liest manche Wörter ohne Anführungszeichen nicht als Text: `no` wird zu `false`, `on` zu `true`, `1` zu
einer Zahl. Darum steht jeder Text in `"…"`. Nur `pos` und `level` brauchen keine.

### Übersetzungen

- Je Basissprache eine Liste. Die **erste** ist die Hauptübersetzung, die der Trainer anzeigt; alle weiteren
  gelten beim Abfragen ebenfalls als richtig.
- Nomen mit Artikel: `"der Apfel"`. Beim Abfragen ist der Artikel optional.
- **Französische Nomen** stehen auch im `lemma` mit bestimmtem Artikel: `"la pomme"`, `"les vacances (f. pl.)"`.
  Bei elidiertem Artikel steht das Geschlecht dahinter: `"l'arbre (m.)"`, `"l'eau (f.)"`. Die `id` ist das Wort
  ohne Artikel und ohne Akzente: `pomme`, `arbre`, `oeil`. Adjektive stehen in der männlichen Form (`"petit"`).
- Eine neue Basissprache (z. B. Französisch für französischsprachige Lernende) braucht einen Eintrag in
  `languages.yaml` mit `base: true` und Übersetzungen unter `translations.fr`. Im Trainer sind dafür zusätzlich die
  Oberflächentexte nötig.

### Wortarten und Niveaus

| `pos` | | `pos` | |
|---|---|---|---|
| `noun` | Nomen | `preposition` | Präposition |
| `verb` | Verb | `conjunction` | Konjunktion |
| `adjective` | Adjektiv | `numeral` | Zahlwort |
| `adverb` | Adverb | `phrase` | Redewendung |
| `pronoun` | Pronomen | `interjection` | Ausruf |
| `determiner` | Begleiter | | |

`level` folgt dem Gemeinsamen Europäischen Referenzrahmen: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`.

### Beispielsätze

Kurz, alltäglich und mit der Vokabel genau in dieser Form. Der Trainer liest sie vor und blendet die Übersetzung
ein.

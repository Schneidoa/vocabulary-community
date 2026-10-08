#!/usr/bin/env python3
"""
Prüft den Vokabel-Katalog: Schema, eindeutige IDs, bekannte Sprachen und Themen.

    python scripts/validate.py                    # alles prüfen
    python scripts/validate.py --base origin/main # zusätzlich: IDs, die gegenüber main fehlen

Läuft lokal und in GitHub Actions; dort erscheinen Fehler als Anmerkungen direkt im Pull Request.
"""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"


class Report:
    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def error(self, file, message):
        self.errors += 1
        self._emit("error", file, message)

    def warning(self, file, message):
        self.warnings += 1
        self._emit("warning", file, message)

    @staticmethod
    def _emit(level, file, message):
        rel = os.path.relpath(file, ROOT)
        if IN_ACTIONS:
            print(f"::{level} file={rel}::{message}")
        else:
            print(f"{'FEHLER' if level == 'error' else 'Warnung'}: {rel}: {message}")


def load_yaml(path, report):
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        report.error(path, f"kein gültiges YAML: {e}")
        return None


def check_schema(path, data, schema_name, report):
    schema = json.loads((ROOT / "schema" / schema_name).read_text(encoding="utf-8"))
    valid = True
    for err in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        valid = False
        where = describe(data, list(err.path))
        hint = ""
        if err.validator == "type" and err.validator_value == "string" and isinstance(err.instance, (bool, int, float)):
            # YAML liest z. B. no, yes, on, off oder 1 ohne Anführungszeichen nicht als Text
            hint = " – Text bitte in Anführungszeichen setzen"
        report.error(path, f"{where}: {err.message}{hint}")
    return valid


def describe(data, path):
    """Pfad wie [3].translations.de lesbar machen, mit der id des Eintrags."""
    if path and isinstance(path[0], int) and isinstance(data, list) and path[0] < len(data):
        entry = data[path[0]]
        label = entry.get("id") or entry.get("slug") or entry.get("code") if isinstance(entry, dict) else None
        rest = ".".join(str(p) for p in path[1:])
        return f"Eintrag {path[0] + 1}" + (f" ({label})" if label else "") + (f", {rest}" if rest else "")
    return ".".join(str(p) for p in path) or "Datei"


def word_files(root):
    return sorted((root / "words").glob("*/*.yaml"))


def ids_at(ref):
    """IDs je Sprache im Stand von ref (z. B. origin/main), gelesen per git show."""
    listing = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref, "words"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
    result = defaultdict(set)
    for name in listing:
        if not name.endswith(".yaml"):
            continue
        content = subprocess.run(["git", "show", f"{ref}:{name}"], cwd=ROOT, capture_output=True, text=True,
                                 check=True).stdout
        language = Path(name).parent.name
        for entry in yaml.safe_load(content) or []:
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                result[language].add(entry["id"])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="Git-Ref zum Vergleich, z. B. origin/main: warnt vor entfernten IDs")
    args = parser.parse_args()
    report = Report()

    languages = load_yaml(ROOT / "languages.yaml", report) or []
    topics = load_yaml(ROOT / "topics.yaml", report) or []
    languages_ok = check_schema(ROOT / "languages.yaml", languages, "languages.schema.json", report)
    topics_ok = check_schema(ROOT / "topics.yaml", topics, "topics.schema.json", report)
    if not (languages_ok and topics_ok):
        return finish(report)

    codes = {l["code"] for l in languages}
    base_codes = {l["code"] for l in languages if l["base"]}
    for name, items, key in (("Sprache", languages, "code"), ("Thema", topics, "slug")):
        for value, count in Counter(i[key] for i in items).items():
            if count > 1:
                report.error(ROOT / ("languages.yaml" if key == "code" else "topics.yaml"), f"{name} {value} doppelt")
    topic_slugs = {t["slug"] for t in topics}
    for topic in topics:
        for code in topic["names"]:
            if code not in base_codes:
                report.error(ROOT / "topics.yaml", f"Thema {topic['slug']}: {code} ist keine Basissprache")

    seen_ids = defaultdict(dict)
    seen_lemmas = defaultdict(dict)
    stats = defaultdict(Counter)
    coverage = defaultdict(Counter)
    for path in word_files(ROOT):
        language, topic = path.parent.name, path.stem
        if language not in codes:
            report.error(path, f"Sprache {language} fehlt in languages.yaml")
        if topic not in topic_slugs:
            report.error(path, f"Thema {topic} fehlt in topics.yaml")
        words = load_yaml(path, report)
        if words is None or not check_schema(path, words, "words.schema.json", report):
            continue
        for word in words:
            wid = word["id"]
            if wid in seen_ids[language]:
                report.error(path, f"id {wid} gibt es schon in {seen_ids[language][wid]}")
            seen_ids[language][wid] = path.name
            key = (word["lemma"], word["pos"])
            if key in seen_lemmas[language]:
                report.error(path, f"{word['lemma']} ({word['pos']}) gibt es schon als id {seen_lemmas[language][key]}")
            seen_lemmas[language][key] = wid
            for field in ("translations", "example_translations"):
                for code in word.get(field, {}):
                    if code not in base_codes:
                        report.error(path, f"{wid}: {field}.{code} – {code} ist keine Basissprache")
            stats[language][word["level"]] += 1
            for code in word["translations"]:
                coverage[language][code] += 1

    if args.base:
        try:
            before = ids_at(args.base)
        except subprocess.CalledProcessError as e:
            report.error(ROOT, f"Vergleich mit {args.base} nicht möglich: {e.stderr.strip()}")
            before = {}
        for language, ids in before.items():
            removed = sorted(ids - set(seen_ids.get(language, {})))
            if removed:
                report.warning(ROOT / "words" / language,
                               f"entfernte oder umbenannte IDs: {', '.join(removed)} – der Lernfortschritt dazu geht "
                               f"verloren. IDs nie umbenennen; Tippfehler nur in lemma korrigieren.")

    for language in sorted(stats):
        levels = ", ".join(f"{lv} {n}" for lv, n in sorted(stats[language].items()))
        total = sum(stats[language].values())
        covered = ", ".join(f"{code} {n * 100 // total} %" for code, n in sorted(coverage[language].items()))
        print(f"{language}: {total} Vokabeln ({levels}) · übersetzt: {covered}")
    return finish(report)


def finish(report):
    print(f"{report.errors} Fehler, {report.warnings} Warnungen")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())

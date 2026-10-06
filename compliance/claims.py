"""Reproduce every number the site states about the NR-4 proposal, and validate the parse.

Run: python compliance/claims.py  -> prints JSON and writes compliance/claims.json
Inputs: product/data/cnae.json (built by product/build_data.py from compliance/sources/).
"""
import hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")
items = json.load(open(os.path.join(HERE, "..", "product", "data", "cnae.json"), encoding="utf-8"))["items"]


def sha(p):
    return hashlib.sha256(open(os.path.join(SRC, p), "rb").read()).hexdigest()


# Parse validation for the consultation text: line numbers must be contiguous and each subclass unique.
s = open(os.path.join(SRC, "consulta_anexoI_nr04_texto_participativo_2026-10-06.txt"), encoding="utf-8").read()
seg = s[s.find("Subclasse CNAE Descri"):]
rows = re.findall(r"(\d{1,4}) (\d{5,7}) (.+?) ?([1-4]) (\d+)(?= \d{1,4} \d{5,7} | \d{1,4} [A-ZÁ])", seg)
lines = [int(r[0]) for r in rows]
subs = [r[1].zfill(7) for r in rows]
gaps = [(a, b) for a, b in zip(lines, lines[1:]) if b != a + 1]

half = {}
for r in rows:
    half.setdefault(int(r[0]) <= 1335, {})[r[1]] = r[3]
out_copies_differ = sum(1 for k, v in half.get(True, {}).items() if half.get(False, {}).get(k) != v)
with_p = [i for i in items if i["gr_proposed"] is not None]
up = [i for i in with_p if i["gr_proposed"] > i["gr_current"]]
down = [i for i in with_p if i["gr_proposed"] < i["gr_current"]]
same = [i for i in with_p if i["gr_proposed"] == i["gr_current"]]
lose = [i for i in with_p if i["gr_current"] <= 2 and i["gr_proposed"] >= 3]
gain = [i for i in with_p if i["gr_current"] >= 3 and i["gr_proposed"] <= 2]
out = {
    "consulted": "2026-10-06",
    "sources_sha256": {f: sha(f) for f in ["portaria_2318.txt", "consulta_anexoI_nr04_texto_participativo_2026-10-06.txt",
                                           "ibge_cnae_subclasses_2026-10-06.json", "portaria_mtp_2318_2022_nova_nr04.pdf",
                                           "aviso_consulta_nr04_2026-06-01.pdf", "nr01_atualizada_2025.pdf"]},
    "parse_validation": {"rows": len(rows), "first_line": lines[0], "last_line": lines[-1], "line_gaps": gaps,
                         "duplicate_subclasses": len(subs) - len(set(subs)),
                         "note": "The texto participativo lists the table twice (Anexo I and again in its Apêndice); both copies are compared below."},
    "copies_differ": out_copies_differ,
    "corrections": json.load(open(os.path.join(HERE, "..", "product", "data", "cnae.json"), encoding="utf-8"))["meta"].get("corrections"),
    "n_subclasses": len(items), "n_with_proposed": len(with_p),
    "missing_proposed": [i["code"] for i in items if i["gr_proposed"] is None],
    "up": len(up), "down": len(down), "same": len(same),
    "cross_le2_to_ge3": len(lose), "cross_ge3_to_le2": len(gain),
    "method": ("Current grade: Anexo I of Portaria MTP 2.318/2022, defined per CNAE class; each subclass inherits its class grade. "
               "Proposed grade: per subclass from the consultation's texto participativo. 'up/down/same' compares the two for the "
               "1,331 subclasses with a proposed grade. 'cross_le2_to_ge3' counts subclasses whose grade would move from 1-2 to 3-4, the "
               "only grades for which NR-1 items 1.8.4/1.8.6 allow ME/EPP to be dispensed of PGR/PCMSO (other conditions also apply)."),
}
json.dump(out, open(os.path.join(HERE, "claims.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))

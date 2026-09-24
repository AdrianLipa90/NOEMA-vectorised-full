"""Generate expanded Polish linguistic database for CIELingo.

Reads the seed DB, adds ~300 lexemes across all PoS categories
with 9-axis semantic mass profiles, case forms, and operator roles.
"""
from __future__ import annotations

import json
from pathlib import Path

SEED_PATH = Path(__file__).resolve().parents[1] / "data/cielingo/polish/polish_linguistic_surface_v01.json"
OUT_PATH = Path(__file__).resolve().parents[1] / "data/cielingo/polish/polish_linguistic_surface_v02.json"

AXES = [
    "concreteness", "agency", "relational_force", "affective_charge",
    "memory_weight", "abstraction_level", "temporal_weight",
    "identity_relevance", "ethical_weight",
]

def mass(*values: float) -> dict[str, float]:
    return dict(zip(AXES, values))

LEXICON: list[dict] = [
    # ── Nouns: Emotions (~20) ──
    {"lemma": "miłość", "forms": ["miłość", "miłości", "miłością"], "pos": "noun", "case_forms": {"miłość": "Nom", "miłości": "Gen", "miłością": "Ins"}, "semantic_mass": mass(0.2, 0.3, 0.9, 0.95, 0.8, 0.6, 0.5, 0.7, 0.7)},
    {"lemma": "nienawiść", "forms": ["nienawiść", "nienawiści", "nienawiścią"], "pos": "noun", "case_forms": {"nienawiść": "Nom", "nienawiści": "Gen", "nienawiścią": "Ins"}, "semantic_mass": mass(0.2, 0.4, 0.8, 0.9, 0.7, 0.5, 0.4, 0.6, 0.3)},
    {"lemma": "radość", "forms": ["radość", "radości", "radością"], "pos": "noun", "case_forms": {"radość": "Nom", "radości": "Gen", "radością": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.8, 0.95, 0.7, 0.4, 0.3, 0.5, 0.6)},
    {"lemma": "smutek", "forms": ["smutek", "smutku", "smutkiem"], "pos": "noun", "case_forms": {"smutek": "Nom", "smutku": "Gen", "smutkiem": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.6, 0.85, 0.6, 0.4, 0.5, 0.4, 0.3)},
    {"lemma": "strach", "forms": ["strach", "strachu", "strachem"], "pos": "noun", "case_forms": {"strach": "Nom", "strachu": "Gen", "strachem": "Ins"}, "semantic_mass": mass(0.2, 0.3, 0.7, 0.9, 0.7, 0.3, 0.4, 0.5, 0.2)},
    {"lemma": "gniew", "forms": ["gniew", "gniewu", "gniewem"], "pos": "noun", "case_forms": {"gniew": "Nom", "gniewu": "Gen", "gniewem": "Ins"}, "semantic_mass": mass(0.2, 0.5, 0.7, 0.9, 0.6, 0.3, 0.3, 0.5, 0.2)},
    {"lemma": "spokój", "forms": ["spokój", "spokoju", "spokojem"], "pos": "noun", "case_forms": {"spokój": "Nom", "spokoju": "Gen", "spokojem": "Ins"}, "semantic_mass": mass(0.2, 0.1, 0.5, 0.85, 0.5, 0.5, 0.6, 0.6, 0.7)},
    {"lemma": "nadzieja", "forms": ["nadzieja", "nadziei", "nadzieją"], "pos": "noun", "case_forms": {"nadzieja": "Nom", "nadziei": "Gen", "nadzieją": "Ins"}, "semantic_mass": mass(0.15, 0.2, 0.8, 0.9, 0.7, 0.6, 0.6, 0.6, 0.7)},
    {"lemma": "tęsknota", "forms": ["tęsknota", "tęsknoty", "tęsknotą"], "pos": "noun", "case_forms": {"tęsknota": "Nom", "tęsknoty": "Gen", "tęsknotą": "Ins"}, "semantic_mass": mass(0.2, 0.15, 0.7, 0.85, 0.7, 0.5, 0.6, 0.5, 0.4)},
    {"lemma": "cierpienie", "forms": ["cierpienie", "cierpienia", "cierpieniem"], "pos": "noun", "case_forms": {"cierpienie": "Nom", "cierpienia": "Gen", "cierpieniem": "Ins"}, "semantic_mass": mass(0.3, 0.2, 0.7, 0.9, 0.7, 0.4, 0.5, 0.6, 0.3)},
    {"lemma": "rozpacz", "forms": ["rozpacz", "rozpaczy", "rozpaczą"], "pos": "noun", "case_forms": {"rozpacz": "Nom", "rozpaczy": "Gen", "rozpaczą": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.6, 0.95, 0.6, 0.3, 0.4, 0.5, 0.2)},
    {"lemma": "zaufanie", "forms": ["zaufanie", "zaufania", "zaufaniem"], "pos": "noun", "case_forms": {"zaufanie": "Nom", "zaufania": "Gen", "zaufaniem": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.9, 0.85, 0.6, 0.5, 0.6, 0.7, 0.8)},
    {"lemma": "zdrada", "forms": ["zdrada", "zdrady", "zdradą"], "pos": "noun", "case_forms": {"zdrada": "Nom", "zdrady": "Gen", "zdradą": "Ins"}, "semantic_mass": mass(0.3, 0.6, 0.8, 0.9, 0.7, 0.3, 0.4, 0.7, 0.1)},
    {"lemma": "żałość", "forms": ["żałość", "żałości", "żałością"], "pos": "noun", "case_forms": {"żałość": "Nom", "żałości": "Gen", "żałością": "Ins"}, "semantic_mass": mass(0.2, 0.15, 0.6, 0.8, 0.5, 0.4, 0.5, 0.4, 0.3)},
    {"lemma": "wstyd", "forms": ["wstyd", "wstydu", "wstydem"], "pos": "noun", "case_forms": {"wstyd": "Nom", "wstydu": "Gen", "wstydem": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.5)},
    {"lemma": "duma", "forms": ["duma", "dumy", "dumą"], "pos": "noun", "case_forms": {"duma": "Nom", "dumy": "Gen", "dumą": "Ins"}, "semantic_mass": mass(0.2, 0.5, 0.7, 0.85, 0.6, 0.5, 0.4, 0.7, 0.5)},
    {"lemma": "zazdrość", "forms": ["zazdrość", "zazdrości", "zazdrością"], "pos": "noun", "case_forms": {"zazdrość": "Nom", "zazdrości": "Gen", "zazdrością": "Ins"}, "semantic_mass": mass(0.2, 0.3, 0.7, 0.85, 0.6, 0.3, 0.4, 0.5, 0.2)},
    {"lemma": "lęk", "forms": ["lęk", "lęku", "lękiem"], "pos": "noun", "case_forms": {"lęk": "Nom", "lęku": "Gen", "lękiem": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.6, 0.85, 0.6, 0.4, 0.5, 0.4, 0.2)},
    {"lemma": "czułość", "forms": ["czułość", "czułości", "czułością"], "pos": "noun", "case_forms": {"czułość": "Nom", "czułości": "Gen", "czułością": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.9, 0.9, 0.7, 0.4, 0.4, 0.6, 0.7)},

    # ── Nouns: Cognition (~15) ──
    {"lemma": "myśl", "forms": ["myśl", "myśli", "myślą"], "pos": "noun", "case_forms": {"myśl": "Nom", "myśli": "Gen", "myślą": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.5, 0.4, 0.6, 0.8, 0.5, 0.7, 0.6)},
    {"lemma": "rozum", "forms": ["rozum", "rozumu", "rozumem"], "pos": "noun", "case_forms": {"rozum": "Nom", "rozumu": "Gen", "rozumem": "Ins"}, "semantic_mass": mass(0.05, 0.4, 0.5, 0.2, 0.6, 0.9, 0.4, 0.6, 0.7)},
    {"lemma": "wiedza", "forms": ["wiedza", "wiedzy", "wiedzą"], "pos": "noun", "case_forms": {"wiedza": "Nom", "wiedzy": "Gen", "wiedzą": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.6, 0.3, 0.7, 0.9, 0.6, 0.5, 0.7)},
    {"lemma": "prawda", "forms": ["prawda", "prawdy", "prawdą"], "pos": "noun", "case_forms": {"prawda": "Nom", "prawdy": "Gen", "prawdą": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.7, 0.5, 0.7, 0.9, 0.6, 0.7, 0.9)},
    {"lemma": "mądrość", "forms": ["mądrość", "mądrości", "mądrością"], "pos": "noun", "case_forms": {"mądrość": "Nom", "mądrości": "Gen", "mądrością": "Ins"}, "semantic_mass": mass(0.05, 0.4, 0.6, 0.3, 0.7, 0.9, 0.6, 0.7, 0.8)},
    {"lemma": "pamięć", "forms": ["pamięć", "pamięci", "pamięcią"], "pos": "noun", "case_forms": {"pamięć": "Nom", "pamięci": "Gen", "pamięcią": "Ins"}, "semantic_mass": mass(0.1, 0.2, 0.5, 0.5, 0.9, 0.7, 0.8, 0.6, 0.5)},
    {"lemma": "świadomość", "forms": ["świadomość", "świadomości", "świadomością"], "pos": "noun", "case_forms": {"świadomość": "Nom", "świadomości": "Gen", "świadomością": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.6, 0.4, 0.7, 0.95, 0.5, 0.8, 0.7)},
    {"lemma": "umysł", "forms": ["umysł", "umysłu", "umysłem"], "pos": "noun", "case_forms": {"umysł": "Nom", "umysłu": "Gen", "umysłem": "Ins"}, "semantic_mass": mass(0.05, 0.4, 0.5, 0.3, 0.6, 0.9, 0.4, 0.7, 0.6)},
    {"lemma": "intuicja", "forms": ["intuicja", "intuicji", "intuicją"], "pos": "noun", "case_forms": {"intuicja": "Nom", "intuicji": "Gen", "intuicją": "Ins"}, "semantic_mass": mass(0.05, 0.2, 0.5, 0.5, 0.6, 0.85, 0.4, 0.6, 0.5)},
    {"lemma": "logika", "forms": ["logika", "logiki", "logiką"], "pos": "noun", "case_forms": {"logika": "Nom", "logiki": "Gen", "logiką": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.6, 0.1, 0.5, 0.95, 0.3, 0.4, 0.7)},
    {"lemma": "wyobraźnia", "forms": ["wyobraźnia", "wyobraźni", "wyobraźnią"], "pos": "noun", "case_forms": {"wyobraźnia": "Nom", "wyobraźni": "Gen", "wyobraźnią": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.5, 0.6, 0.6, 0.85, 0.5, 0.6, 0.4)},
    {"lemma": "idea", "forms": ["idea", "idei", "ideą"], "pos": "noun", "case_forms": {"idea": "Nom", "idei": "Gen", "ideą": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.5, 0.4, 0.5, 0.95, 0.5, 0.6, 0.6)},
    {"lemma": "koncept", "forms": ["koncept", "konceptu", "konceptem"], "pos": "noun", "case_forms": {"koncept": "Nom", "konceptu": "Gen", "konceptem": "Ins"}, "semantic_mass": mass(0.05, 0.3, 0.4, 0.2, 0.4, 0.95, 0.3, 0.5, 0.5)},
    {"lemma": "język", "forms": ["język", "języka", "językiem"], "pos": "noun", "case_forms": {"język": "Nom", "języka": "Gen", "językiem": "Ins"}, "semantic_mass": mass(0.4, 0.3, 0.7, 0.3, 0.6, 0.8, 0.5, 0.7, 0.5)},
    {"lemma": "słowo", "forms": ["słowo", "słowa", "słowem"], "pos": "noun", "case_forms": {"słowo": "Nom", "słowa": "Gen", "słowem": "Ins"}, "semantic_mass": mass(0.3, 0.2, 0.7, 0.4, 0.6, 0.8, 0.4, 0.6, 0.5)},

    # ── Nouns: Nature/Element (~20) ──
    {"lemma": "ogień", "forms": ["ogień", "ognia", "ogniem"], "pos": "noun", "case_forms": {"ogień": "Nom", "ognia": "Gen", "ogniem": "Ins"}, "semantic_mass": mass(0.9, 0.4, 0.5, 0.7, 0.5, 0.2, 0.3, 0.4, 0.3)},
    {"lemma": "wiatr", "forms": ["wiatr", "wiatru", "wiatrem"], "pos": "noun", "case_forms": {"wiatr": "Nom", "wiatru": "Gen", "wiatrem": "Ins"}, "semantic_mass": mass(0.85, 0.3, 0.4, 0.5, 0.4, 0.2, 0.3, 0.3, 0.2)},
    {"lemma": "ziemia", "forms": ["ziemia", "ziemi", "ziemią"], "pos": "noun", "case_forms": {"ziemia": "Nom", "ziemi": "Gen", "ziemią": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.6, 0.3, 0.5, 0.1, 0.5, 0.5, 0.4)},
    {"lemma": "niebo", "forms": ["niebo", "nieba", "niebem"], "pos": "noun", "case_forms": {"niebo": "Nom", "nieba": "Gen", "niebem": "Ins"}, "semantic_mass": mass(0.7, 0.05, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.3)},
    {"lemma": "gwiazda", "forms": ["gwiazda", "gwiazdy", "gwiazdą"], "pos": "noun", "case_forms": {"gwiazda": "Nom", "gwiazdy": "Gen", "gwiazdą": "Ins"}, "semantic_mass": mass(0.8, 0.05, 0.3, 0.6, 0.5, 0.5, 0.6, 0.4, 0.3)},
    {"lemma": "księżyc", "forms": ["księżyc", "księżyca", "księżycem"], "pos": "noun", "case_forms": {"księżyc": "Nom", "księżyca": "Gen", "księżycem": "Ins"}, "semantic_mass": mass(0.8, 0.05, 0.3, 0.5, 0.4, 0.4, 0.5, 0.3, 0.2)},
    {"lemma": "słońce", "forms": ["słońce", "słońca", "słońcem"], "pos": "noun", "case_forms": {"słońce": "Nom", "słońca": "Gen", "słońcem": "Ins"}, "semantic_mass": mass(0.9, 0.1, 0.4, 0.7, 0.5, 0.2, 0.5, 0.4, 0.4)},
    {"lemma": "las", "forms": ["las", "lasu", "lasem"], "pos": "noun", "case_forms": {"las": "Nom", "lasu": "Gen", "lasem": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.5, 0.5, 0.5, 0.1, 0.4, 0.3, 0.4)},
    {"lemma": "rzeka", "forms": ["rzeka", "rzeki", "rzeką"], "pos": "noun", "case_forms": {"rzeka": "Nom", "rzeki": "Gen", "rzeką": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.5, 0.4, 0.5, 0.1, 0.5, 0.3, 0.3)},
    {"lemma": "morze", "forms": ["morze", "morza", "morzem"], "pos": "noun", "case_forms": {"morze": "Nom", "morza": "Gen", "morzem": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.4, 0.5, 0.5, 0.15, 0.5, 0.3, 0.3)},
    {"lemma": "góra", "forms": ["góra", "góry", "górą"], "pos": "noun", "case_forms": {"góra": "Nom", "góry": "Gen", "górą": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.3, 0.3, 0.4, 0.1, 0.5, 0.3, 0.2)},
    {"lemma": "drzewo", "forms": ["drzewo", "drzewa", "drzewem"], "pos": "noun", "case_forms": {"drzewo": "Nom", "drzewa": "Gen", "drzewem": "Ins"}, "semantic_mass": mass(0.95, 0.2, 0.4, 0.4, 0.5, 0.1, 0.4, 0.3, 0.3)},
    {"lemma": "kwiat", "forms": ["kwiat", "kwiatu", "kwiatem"], "pos": "noun", "case_forms": {"kwiat": "Nom", "kwiatu": "Gen", "kwiatem": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.3, 0.6, 0.4, 0.1, 0.2, 0.2, 0.3)},
    {"lemma": "ptak", "forms": ["ptak", "ptaka", "ptakiem"], "pos": "noun", "case_forms": {"ptak": "Nom", "ptaka": "Gen", "ptakiem": "Ins"}, "semantic_mass": mass(0.95, 0.5, 0.3, 0.3, 0.3, 0.1, 0.2, 0.2, 0.2)},
    {"lemma": "kamień", "forms": ["kamień", "kamienia", "kamieniem"], "pos": "noun", "case_forms": {"kamień": "Nom", "kamienia": "Gen", "kamieniem": "Ins"}, "semantic_mass": mass(0.95, 0.05, 0.2, 0.1, 0.4, 0.05, 0.5, 0.2, 0.1)},
    {"lemma": "liść", "forms": ["liść", "liścia", "liściem"], "pos": "noun", "case_forms": {"liść": "Nom", "liścia": "Gen", "liściem": "Ins"}, "semantic_mass": mass(0.95, 0.1, 0.2, 0.3, 0.3, 0.05, 0.2, 0.2, 0.2)},
    {"lemma": "śnieg", "forms": ["śnieg", "śniegu", "śniegiem"], "pos": "noun", "case_forms": {"śnieg": "Nom", "śniegu": "Gen", "śniegiem": "Ins"}, "semantic_mass": mass(0.95, 0.05, 0.2, 0.3, 0.3, 0.05, 0.3, 0.2, 0.2)},

    # ── Nouns: Body/Physical (~12) ──
    {"lemma": "ciało", "forms": ["ciało", "ciała", "ciałem"], "pos": "noun", "case_forms": {"ciało": "Nom", "ciała": "Gen", "ciałem": "Ins"}, "semantic_mass": mass(0.95, 0.3, 0.5, 0.3, 0.5, 0.1, 0.5, 0.6, 0.4)},
    {"lemma": "krew", "forms": ["krew", "krwi", "krwią"], "pos": "noun", "case_forms": {"krew": "Nom", "krwi": "Gen", "krwią": "Ins"}, "semantic_mass": mass(0.9, 0.1, 0.5, 0.6, 0.4, 0.1, 0.3, 0.4, 0.3)},
    {"lemma": "serce", "forms": ["serce", "serca", "sercem"], "pos": "noun", "case_forms": {"serce": "Nom", "serca": "Gen", "sercem": "Ins"}, "semantic_mass": mass(0.85, 0.2, 0.8, 0.8, 0.6, 0.3, 0.5, 0.7, 0.6)},
    {"lemma": "głowa", "forms": ["głowa", "głowy", "głową"], "pos": "noun", "case_forms": {"głowa": "Nom", "głowy": "Gen", "głową": "Ins"}, "semantic_mass": mass(0.95, 0.3, 0.4, 0.2, 0.4, 0.15, 0.3, 0.5, 0.3)},
    {"lemma": "ręka", "forms": ["ręka", "ręki", "ręką"], "pos": "noun", "case_forms": {"ręka": "Nom", "ręki": "Gen", "ręką": "Ins"}, "semantic_mass": mass(0.95, 0.5, 0.5, 0.2, 0.4, 0.05, 0.3, 0.4, 0.3)},
    {"lemma": "oko", "forms": ["oko", "oka", "okiem"], "pos": "noun", "case_forms": {"oko": "Nom", "oka": "Gen", "okiem": "Ins"}, "semantic_mass": mass(0.95, 0.2, 0.4, 0.3, 0.5, 0.1, 0.3, 0.4, 0.3)},
    {"lemma": "dusza", "forms": ["dusza", "duszy", "duszą"], "pos": "noun", "case_forms": {"dusza": "Nom", "duszy": "Gen", "duszą": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.7, 0.7, 0.7, 0.85, 0.6, 0.9, 0.8)},

    # ── Nouns: Time/Space (~12) ──
    {"lemma": "czas", "forms": ["czas", "czasu", "czasem"], "pos": "noun", "case_forms": {"czas": "Nom", "czasu": "Gen", "czasem": "Ins"}, "semantic_mass": mass(0.1, 0.2, 0.5, 0.3, 0.5, 0.85, 0.95, 0.5, 0.4)},
    {"lemma": "chwila", "forms": ["chwila", "chwili", "chwilą"], "pos": "noun", "case_forms": {"chwila": "Nom", "chwili": "Gen", "chwilą": "Ins"}, "semantic_mass": mass(0.2, 0.15, 0.3, 0.3, 0.3, 0.5, 0.9, 0.3, 0.2)},
    {"lemma": "dzień", "forms": ["dzień", "dnia", "dniem"], "pos": "noun", "case_forms": {"dzień": "Nom", "dnia": "Gen", "dniem": "Ins"}, "semantic_mass": mass(0.7, 0.2, 0.4, 0.4, 0.4, 0.3, 0.9, 0.3, 0.3)},
    {"lemma": "noc", "forms": ["noc", "nocy", "nocą"], "pos": "noun", "case_forms": {"noc": "Nom", "nocy": "Gen", "nocą": "Ins"}, "semantic_mass": mass(0.6, 0.15, 0.4, 0.5, 0.4, 0.4, 0.85, 0.4, 0.3)},
    {"lemma": "świat", "forms": ["świat", "świata", "światem"], "pos": "noun", "case_forms": {"świat": "Nom", "świata": "Gen", "światem": "Ins"}, "semantic_mass": mass(0.6, 0.3, 0.7, 0.4, 0.6, 0.7, 0.6, 0.6, 0.5)},
    {"lemma": "przestrzeń", "forms": ["przestrzeń", "przestrzeni", "przestrzenią"], "pos": "noun", "case_forms": {"przestrzeń": "Nom", "przestrzeni": "Gen", "przestrzenią": "Ins"}, "semantic_mass": mass(0.3, 0.1, 0.4, 0.2, 0.4, 0.85, 0.4, 0.4, 0.3)},
    {"lemma": "miejsce", "forms": ["miejsce", "miejsca", "miejscem"], "pos": "noun", "case_forms": {"miejsce": "Nom", "miejsca": "Gen", "miejscem": "Ins"}, "semantic_mass": mass(0.6, 0.15, 0.4, 0.2, 0.4, 0.3, 0.4, 0.3, 0.2)},
    {"lemma": "kraniec", "forms": ["kraniec", "krańca", "krańcem"], "pos": "noun", "case_forms": {"kraniec": "Nom", "krańca": "Gen", "krańcem": "Ins"}, "semantic_mass": mass(0.5, 0.1, 0.3, 0.3, 0.3, 0.5, 0.4, 0.3, 0.2)},
    {"lemma": "koniec", "forms": ["koniec", "końca", "końcem"], "pos": "noun", "case_forms": {"koniec": "Nom", "końca": "Gen", "końcem": "Ins"}, "semantic_mass": mass(0.4, 0.2, 0.5, 0.5, 0.4, 0.6, 0.7, 0.5, 0.4)},
    {"lemma": "początek", "forms": ["początek", "początku", "początkiem"], "pos": "noun", "case_forms": {"początek": "Nom", "początku": "Gen", "początkiem": "Ins"}, "semantic_mass": mass(0.3, 0.3, 0.5, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5)},

    # ── Nouns: Abstract/Philosophical (~20) ──
    {"lemma": "byt", "forms": ["byt", "bytu", "bytem"], "pos": "noun", "case_forms": {"byt": "Nom", "bytu": "Gen", "bytem": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.5, 0.2, 0.5, 0.95, 0.5, 0.6, 0.5)},
    {"lemma": "nicość", "forms": ["nicość", "nicości", "nicością"], "pos": "noun", "case_forms": {"nicość": "Nom", "nicości": "Gen", "nicością": "Ins"}, "semantic_mass": mass(0.05, 0.05, 0.2, 0.5, 0.3, 0.95, 0.4, 0.4, 0.2)},
    {"lemma": "pustka", "forms": ["pustka", "pustki", "pustką"], "pos": "noun", "case_forms": {"pustka": "Nom", "pustki": "Gen", "pustką": "Ins"}, "semantic_mass": mass(0.2, 0.05, 0.3, 0.6, 0.3, 0.8, 0.5, 0.4, 0.2)},
    {"lemma": "cisza", "forms": ["cisza", "ciszy", "ciszą"], "pos": "noun", "case_forms": {"cisza": "Nom", "ciszy": "Gen", "ciszą": "Ins"}, "semantic_mass": mass(0.2, 0.05, 0.3, 0.6, 0.5, 0.6, 0.5, 0.4, 0.4)},
    {"lemma": "chaos", "forms": ["chaos", "chaosu", "chaosem"], "pos": "noun", "case_forms": {"chaos": "Nom", "chaosu": "Gen", "chaosem": "Ins"}, "semantic_mass": mass(0.3, 0.3, 0.5, 0.7, 0.4, 0.5, 0.4, 0.3, 0.1)},
    {"lemma": "porządek", "forms": ["porządek", "porządku", "porządkiem"], "pos": "noun", "case_forms": {"porządek": "Nom", "porządku": "Gen", "porządkiem": "Ins"}, "semantic_mass": mass(0.3, 0.3, 0.6, 0.4, 0.5, 0.6, 0.4, 0.5, 0.7)},
    {"lemma": "harmonia", "forms": ["harmonia", "harmonii", "harmonią"], "pos": "noun", "case_forms": {"harmonia": "Nom", "harmonii": "Gen", "harmonią": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.7, 0.7, 0.6, 0.6, 0.4, 0.6, 0.8)},
    {"lemma": "piękno", "forms": ["piękno", "piękna", "pięknem"], "pos": "noun", "case_forms": {"piękno": "Nom", "piękna": "Gen", "pięknem": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.6, 0.85, 0.7, 0.7, 0.4, 0.6, 0.7)},
    {"lemma": "dobro", "forms": ["dobro", "dobra", "dobrem"], "pos": "noun", "case_forms": {"dobro": "Nom", "dobra": "Gen", "dobrem": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.7, 0.6, 0.6, 0.8, 0.4, 0.7, 0.95)},
    {"lemma": "zło", "forms": ["zło", "zła", "złem"], "pos": "noun", "case_forms": {"zło": "Nom", "zła": "Gen", "złem": "Ins"}, "semantic_mass": mass(0.2, 0.5, 0.6, 0.7, 0.5, 0.6, 0.4, 0.5, 0.05)},
    {"lemma": "wolność", "forms": ["wolność", "wolności", "wolnością"], "pos": "noun", "case_forms": {"wolność": "Nom", "wolności": "Gen", "wolnością": "Ins"}, "semantic_mass": mass(0.1, 0.5, 0.7, 0.7, 0.6, 0.8, 0.5, 0.8, 0.85)},
    {"lemma": "przeznaczenie", "forms": ["przeznaczenie", "przeznaczenia", "przeznaczeniem"], "pos": "noun", "case_forms": {"przeznaczenie": "Nom", "przeznaczenia": "Gen", "przeznaczeniem": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.6, 0.5, 0.5, 0.85, 0.7, 0.6, 0.5)},
    {"lemma": "tajemnica", "forms": ["tajemnica", "tajemnicy", "tajemnicą"], "pos": "noun", "case_forms": {"tajemnica": "Nom", "tajemnicy": "Gen", "tajemnicą": "Ins"}, "semantic_mass": mass(0.2, 0.2, 0.4, 0.5, 0.5, 0.8, 0.5, 0.4, 0.3)},
    {"lemma": "wieczność", "forms": ["wieczność", "wieczności", "wiecznością"], "pos": "noun", "case_forms": {"wieczność": "Nom", "wieczności": "Gen", "wiecznością": "Ins"}, "semantic_mass": mass(0.05, 0.1, 0.4, 0.5, 0.5, 0.9, 0.95, 0.5, 0.5)},
    {"lemma": "nieskończoność", "forms": ["nieskończoność", "nieskończoności", "nieskończonością"], "pos": "noun", "case_forms": {"nieskończoność": "Nom", "nieskończoności": "Gen", "nieskończonością": "Ins"}, "semantic_mass": mass(0.05, 0.1, 0.3, 0.4, 0.4, 0.95, 0.7, 0.5, 0.4)},
    {"lemma": "los", "forms": ["los", "losu", "losem"], "pos": "noun", "case_forms": {"los": "Nom", "losu": "Gen", "losem": "Ins"}, "semantic_mass": mass(0.2, 0.3, 0.5, 0.5, 0.4, 0.7, 0.6, 0.5, 0.4)},
    {"lemma": "światło", "forms": ["światło", "światła", "światłem"], "pos": "noun", "case_forms": {"światło": "Nom", "światła": "Gen", "światłem": "Ins"}, "semantic_mass": mass(0.7, 0.1, 0.4, 0.6, 0.5, 0.4, 0.4, 0.4, 0.5)},
    {"lemma": "ciemność", "forms": ["ciemność", "ciemności", "ciemnością"], "pos": "noun", "case_forms": {"ciemność": "Nom", "ciemności": "Gen", "ciemnością": "Ins"}, "semantic_mass": mass(0.5, 0.1, 0.3, 0.6, 0.4, 0.5, 0.4, 0.3, 0.15)},
    {"lemma": "tożsamość", "forms": ["tożsamość", "tożsamości", "tożsamością"], "pos": "noun", "case_forms": {"tożsamość": "Nom", "tożsamości": "Gen", "tożsamością": "Ins"}, "semantic_mass": mass(0.1, 0.4, 0.6, 0.4, 0.6, 0.8, 0.6, 0.95, 0.7)},
    {"lemma": "istnienie", "forms": ["istnienie", "istnienia", "istnieniem"], "pos": "noun", "case_forms": {"istnienie": "Nom", "istnienia": "Gen", "istnieniem": "Ins"}, "semantic_mass": mass(0.1, 0.3, 0.5, 0.3, 0.5, 0.9, 0.6, 0.6, 0.5)},

    # ── Nouns: Society/Relation (~15) ──
    {"lemma": "człowiek", "forms": ["człowiek", "człowieka", "człowiekiem"], "pos": "noun", "case_forms": {"człowiek": "Nom", "człowieka": "Gen", "człowiekiem": "Ins"}, "semantic_mass": mass(0.8, 0.6, 0.7, 0.5, 0.6, 0.4, 0.5, 0.7, 0.6)},
    {"lemma": "przyjaźń", "forms": ["przyjaźń", "przyjaźni", "przyjaźnią"], "pos": "noun", "case_forms": {"przyjaźń": "Nom", "przyjaźni": "Gen", "przyjaźnią": "Ins"}, "semantic_mass": mass(0.2, 0.3, 0.95, 0.85, 0.7, 0.4, 0.5, 0.7, 0.8)},
    {"lemma": "rodzina", "forms": ["rodzina", "rodziny", "rodziną"], "pos": "noun", "case_forms": {"rodzina": "Nom", "rodziny": "Gen", "rodziną": "Ins"}, "semantic_mass": mass(0.5, 0.3, 0.9, 0.6, 0.6, 0.3, 0.5, 0.7, 0.7)},
    {"lemma": "wspólnota", "forms": ["wspólnota", "wspólnoty", "wspólnotą"], "pos": "noun", "case_forms": {"wspólnota": "Nom", "wspólnoty": "Gen", "wspólnotą": "Ins"}, "semantic_mass": mass(0.3, 0.4, 0.9, 0.5, 0.5, 0.4, 0.4, 0.7, 0.6)},
    {"lemma": "ojczyzna", "forms": ["ojczyzna", "ojczyzny", "ojczyzną"], "pos": "noun", "case_forms": {"ojczyzna": "Nom", "ojczyzny": "Gen", "ojczyzną": "Ins"}, "semantic_mass": mass(0.4, 0.3, 0.8, 0.6, 0.6, 0.4, 0.6, 0.8, 0.7)},
    {"lemma": "miasto", "forms": ["miasto", "miasta", "miastem"], "pos": "noun", "case_forms": {"miasto": "Nom", "miasta": "Gen", "miastem": "Ins"}, "semantic_mass": mass(0.85, 0.3, 0.6, 0.3, 0.4, 0.3, 0.5, 0.4, 0.3)},
    {"lemma": "dom", "forms": ["dom", "domu", "domem"], "pos": "noun", "case_forms": {"dom": "Nom", "domu": "Gen", "domem": "Ins"}, "semantic_mass": mass(0.9, 0.2, 0.7, 0.6, 0.6, 0.2, 0.5, 0.6, 0.5)},
    {"lemma": "droga", "forms": ["droga", "drogi", "drogą"], "pos": "noun", "case_forms": {"droga": "Nom", "drogi": "Gen", "drogą": "Ins"}, "semantic_mass": mass(0.8, 0.2, 0.5, 0.3, 0.4, 0.3, 0.5, 0.4, 0.3)},
    {"lemma": "most", "forms": ["most", "mostu", "mostem"], "pos": "noun", "case_forms": {"most": "Nom", "mostu": "Gen", "mostem": "Ins"}, "semantic_mass": mass(0.85, 0.15, 0.6, 0.2, 0.3, 0.2, 0.3, 0.3, 0.2)},

    # ── Verbs: Existence/State (~12) ──
    {"lemma": "być", "forms": ["jest", "są", "był", "była", "byli", "były", "będzie", "będą"], "pos": "verb", "semantic_mass": mass(0.1, 0.3, 0.5, 0.2, 0.3, 0.8, 0.6, 0.4, 0.3)},
    {"lemma": "stać się", "forms": ["staje", "stoi", "stał", "stała"], "pos": "verb", "semantic_mass": mass(0.2, 0.3, 0.5, 0.3, 0.3, 0.6, 0.5, 0.4, 0.3)},
    {"lemma": "żyć", "forms": ["żyje", "żyją", "żył", "żyła"], "pos": "verb", "semantic_mass": mass(0.5, 0.5, 0.6, 0.5, 0.5, 0.4, 0.6, 0.6, 0.6)},
    {"lemma": "umrzeć", "forms": ["umiera", "umarł", "umarła"], "pos": "verb", "semantic_mass": mass(0.4, 0.2, 0.5, 0.8, 0.5, 0.5, 0.7, 0.5, 0.3)},
    {"lemma": "istnieć", "forms": ["istnieje", "istnieją", "istniał", "istniała"], "pos": "verb", "semantic_mass": mass(0.1, 0.3, 0.4, 0.2, 0.4, 0.85, 0.5, 0.4, 0.4)},
    {"lemma": "trwać", "forms": ["trwa", "trwają", "trwał", "trwała"], "pos": "verb", "semantic_mass": mass(0.2, 0.2, 0.4, 0.2, 0.4, 0.5, 0.8, 0.3, 0.3)},
    {"lemma": "zmienić", "forms": ["zmienia", "zmieniają", "zmienił", "zmieniła"], "pos": "verb", "semantic_mass": mass(0.2, 0.5, 0.5, 0.4, 0.4, 0.5, 0.6, 0.4, 0.3)},
    {"lemma": "zniknąć", "forms": ["znika", "znikają", "zniknął", "zniknęła"], "pos": "verb", "semantic_mass": mass(0.2, 0.2, 0.3, 0.5, 0.3, 0.6, 0.5, 0.3, 0.2)},
    {"lemma": "narodzić się", "forms": ["narodził", "narodziła", "rodzi"], "pos": "verb", "semantic_mass": mass(0.6, 0.4, 0.7, 0.6, 0.5, 0.4, 0.6, 0.6, 0.5)},
    {"lemma": "zostać", "forms": ["zostaje", "zostaną", "został", "została"], "pos": "verb", "semantic_mass": mass(0.2, 0.3, 0.4, 0.2, 0.3, 0.5, 0.4, 0.3, 0.3)},
    {"lemma": "brakować", "forms": ["brak", "brakuje"], "pos": "verb", "semantic_mass": mass(0.1, 0.1, 0.3, 0.4, 0.2, 0.4, 0.3, 0.2, 0.2)},

    # ── Verbs: Perception/Sensation (~10) ──
    {"lemma": "widzieć", "forms": ["widzi", "widzę", "widzisz", "widzą", "widział", "widziała"], "pos": "verb", "semantic_mass": mass(0.5, 0.3, 0.5, 0.3, 0.5, 0.5, 0.4, 0.4, 0.3)},
    {"lemma": "słyszeć", "forms": ["słyszy", "słyszę", "słyszysz", "słyszą", "słyszał", "słyszała"], "pos": "verb", "semantic_mass": mass(0.4, 0.2, 0.5, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3)},
    {"lemma": "czuć", "forms": ["czuje", "czuję", "czujesz", "czują", "czuł", "czuła"], "pos": "verb", "semantic_mass": mass(0.3, 0.2, 0.6, 0.8, 0.5, 0.5, 0.4, 0.5, 0.4)},
    {"lemma": "dotykać", "forms": ["dotyka", "dotykam", "dotykasz", "dotykał", "dotykała"], "pos": "verb", "semantic_mass": mass(0.8, 0.3, 0.5, 0.4, 0.4, 0.3, 0.3, 0.4, 0.3)},
    {"lemma": "czuć zapach", "forms": ["pachnie", "czuję zapach"], "pos": "verb", "semantic_mass": mass(0.5, 0.1, 0.3, 0.5, 0.4, 0.3, 0.3, 0.3, 0.2)},

    # ── Verbs: Emotion (~10) ──
    {"lemma": "kochać", "forms": ["kocha", "kocham", "kochasz", "kochają", "kochał", "kochała"], "pos": "verb", "semantic_mass": mass(0.2, 0.4, 0.9, 0.95, 0.7, 0.4, 0.5, 0.7, 0.7)},
    {"lemma": "nienawidzić", "forms": ["nienawidzi", "nienawidzę", "nienawidzisz", "nienawidził", "nienawidziła"], "pos": "verb", "semantic_mass": mass(0.2, 0.5, 0.7, 0.9, 0.6, 0.3, 0.4, 0.6, 0.2)},
    {"lemma": "bać się", "forms": ["boi", "boję", "boisz", "boją", "bał", "bała"], "pos": "verb", "semantic_mass": mass(0.2, 0.2, 0.6, 0.85, 0.5, 0.3, 0.4, 0.4, 0.2)},
    {"lemma": "cieszyć się", "forms": ["cieszy", "cieszę", "cieszysz", "cieszą", "cieszył", "cieszyła"], "pos": "verb", "semantic_mass": mass(0.2, 0.3, 0.7, 0.9, 0.5, 0.3, 0.3, 0.5, 0.5)},
    {"lemma": "smucić się", "forms": ["smuci", "smucę", "smucisz", "smucą", "smucił", "smuciła"], "pos": "verb", "semantic_mass": mass(0.2, 0.2, 0.5, 0.85, 0.5, 0.3, 0.4, 0.4, 0.2)},
    {"lemma": "złościć się", "forms": ["złości", "złościł", "złościła"], "pos": "verb", "semantic_mass": mass(0.2, 0.5, 0.6, 0.9, 0.4, 0.2, 0.3, 0.4, 0.15)},
    {"lemma": "pragnąć", "forms": ["pragnie", "pragnę", "pragniesz", "pragnął", "pragnęła"], "pos": "verb", "semantic_mass": mass(0.2, 0.4, 0.7, 0.8, 0.5, 0.5, 0.5, 0.6, 0.4)},
    {"lemma": "wierzyć", "forms": ["wierzy", "wierzę", "wierzysz", "wierzyli", "wierzyła"], "pos": "verb", "semantic_mass": mass(0.1, 0.3, 0.7, 0.6, 0.6, 0.7, 0.5, 0.7, 0.7)},

    # ── Verbs: Cognition (~10) ──
    {"lemma": "myśleć", "forms": ["myśli", "myślę", "myślisz", "myślą", "myślał", "myślała"], "pos": "verb", "semantic_mass": mass(0.05, 0.4, 0.5, 0.3, 0.5, 0.85, 0.4, 0.6, 0.5)},
    {"lemma": "wiedzieć", "forms": ["wie", "wiem", "wiesz", "wiedzą", "wiedział", "wiedziała"], "pos": "verb", "semantic_mass": mass(0.05, 0.3, 0.5, 0.2, 0.5, 0.9, 0.4, 0.5, 0.6)},
    {"lemma": "rozumieć", "forms": ["rozumie", "rozumiem", "rozumiesz", "rozumieją", "rozumiał", "rozumiała"], "pos": "verb", "semantic_mass": mass(0.05, 0.3, 0.5, 0.3, 0.5, 0.85, 0.3, 0.5, 0.6)},
    {"lemma": "pamiętać", "forms": ["pamięta", "pamiętam", "pamiętasz", "pamiętał", "pamiętała"], "pos": "verb", "semantic_mass": mass(0.1, 0.3, 0.4, 0.4, 0.85, 0.6, 0.6, 0.5, 0.4)},
    {"lemma": "zapomnieć", "forms": ["zapomina", "zapomniał", "zapomniała"], "pos": "verb", "semantic_mass": mass(0.1, 0.2, 0.3, 0.5, 0.7, 0.5, 0.5, 0.4, 0.2)},
    {"lemma": "wyobrazić", "forms": ["wyobraża", "wyobrażam", "wyobrażasz", "wyobrażał", "wyobrażała"], "pos": "verb", "semantic_mass": mass(0.05, 0.3, 0.4, 0.5, 0.5, 0.85, 0.4, 0.5, 0.3)},
    {"lemma": "marzyć", "forms": ["marzy", "marzę", "marzysz", "marzą", "marzył", "marzyła"], "pos": "verb", "semantic_mass": mass(0.1, 0.2, 0.5, 0.7, 0.5, 0.7, 0.5, 0.5, 0.4)},
    {"lemma": "milczeć", "forms": ["milczy", "milczę", "milczysz", "milczą", "milczał", "milczała"], "pos": "verb", "semantic_mass": mass(0.15, 0.1, 0.3, 0.5, 0.4, 0.5, 0.5, 0.3, 0.3)},

    # ── Verbs: Communication (~8) ──
    {"lemma": "mówić", "forms": ["mówi", "mówię", "mówisz", "mówią", "mówił", "mówiła"], "pos": "verb", "semantic_mass": mass(0.3, 0.5, 0.7, 0.4, 0.4, 0.5, 0.3, 0.5, 0.4)},
    {"lemma": "powiedzieć", "forms": ["powie", "powiem", "powie", "powiedzą", "powiedział", "powiedziała"], "pos": "verb", "semantic_mass": mass(0.2, 0.5, 0.7, 0.4, 0.4, 0.5, 0.3, 0.5, 0.4)},
    {"lemma": "pytać", "forms": ["pyta", "pytam", "pytasz", "pytają", "pytał", "pytała"], "pos": "verb", "semantic_mass": mass(0.2, 0.5, 0.6, 0.3, 0.3, 0.5, 0.2, 0.4, 0.4)},
    {"lemma": "odpowiedzieć", "forms": ["odpowiada", "odpowiem", "odpowie", "odpowiedział", "odpowiedziała"], "pos": "verb", "semantic_mass": mass(0.2, 0.4, 0.6, 0.3, 0.3, 0.5, 0.2, 0.4, 0.5)},
    {"lemma": "wołać", "forms": ["woła", "wołam", "wołasz", "wołają", "wołał", "wołała"], "pos": "verb", "semantic_mass": mass(0.4, 0.5, 0.6, 0.6, 0.3, 0.3, 0.2, 0.4, 0.3)},
    {"lemma": "śpiewać", "forms": ["śpiewa", "śpiewam", "śpiewasz", "śpiewają", "śpiewał", "śpiewała"], "pos": "verb", "semantic_mass": mass(0.3, 0.4, 0.5, 0.7, 0.4, 0.4, 0.3, 0.4, 0.4)},
    {"lemma": "słuchać", "forms": ["słucha", "słucham", "słuchasz", "słuchają", "słuchał", "słuchała"], "pos": "verb", "semantic_mass": mass(0.3, 0.3, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4)},
    {"lemma": "krzyczeć", "forms": ["krzyczy", "krzyczę", "krzyczysz", "krzyczą", "krzyczał", "krzyczała"], "pos": "verb", "semantic_mass": mass(0.4, 0.5, 0.4, 0.7, 0.3, 0.2, 0.2, 0.3, 0.15)},

    # ── Verbs: Motion (~10) ──
    {"lemma": "iść", "forms": ["idzie", "idę", "idziesz", "idą", "szedł", "szła"], "pos": "verb", "semantic_mass": mass(0.6, 0.5, 0.4, 0.2, 0.3, 0.2, 0.4, 0.3, 0.2)},
    {"lemma": "biec", "forms": ["biegnie", "biegnę", "biegniesz", "biegną", "biegł", "biegła"], "pos": "verb", "semantic_mass": mass(0.6, 0.6, 0.3, 0.4, 0.2, 0.15, 0.3, 0.2, 0.15)},
    {"lemma": "przyjść", "forms": ["przychodzi", "przyjdę", "przyjdziesz", "przyjdą", "przyszedł", "przyszła"], "pos": "verb", "semantic_mass": mass(0.4, 0.4, 0.5, 0.3, 0.3, 0.3, 0.5, 0.4, 0.3)},
    {"lemma": "odejść", "forms": ["odchodzi", "odejdę", "odejdziesz", "odejdą", "odszedł", "odeszła"], "pos": "verb", "semantic_mass": mass(0.3, 0.4, 0.4, 0.5, 0.3, 0.4, 0.5, 0.4, 0.2)},
    {"lemma": "stać", "forms": ["stoi", "stoję", "stoisz", "stoją", "stał", "stała"], "pos": "verb", "semantic_mass": mass(0.5, 0.2, 0.3, 0.15, 0.3, 0.2, 0.4, 0.2, 0.15)},
    {"lemma": "lecieć", "forms": ["leci", "lecę", "lecisz", "lecą", "leciał", "leciała"], "pos": "verb", "semantic_mass": mass(0.5, 0.4, 0.3, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2)},
    {"lemma": "płynąć", "forms": ["płynie", "płynę", "płyniesz", "płyną", "płynął", "płynęła"], "pos": "verb", "semantic_mass": mass(0.7, 0.3, 0.4, 0.4, 0.3, 0.2, 0.4, 0.3, 0.2)},
    {"lemma": "spaść", "forms": ["spada", "spadnę", "spadniesz", "spadną", "spadł", "spadła"], "pos": "verb", "semantic_mass": mass(0.5, 0.2, 0.3, 0.5, 0.2, 0.3, 0.3, 0.2, 0.15)},
    {"lemma": "wracać", "forms": ["wraca", "wracam", "wracasz", "wracają", "wracał", "wracała"], "pos": "verb", "semantic_mass": mass(0.4, 0.4, 0.5, 0.4, 0.4, 0.3, 0.5, 0.5, 0.3)},
    {"lemma": "otwierać", "forms": ["otwiera", "otwieram", "otwierasz", "otwierają", "otwierał", "otwierała"], "pos": "verb", "semantic_mass": mass(0.5, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3)},

    # ── Adjectives: Emotional (~10) ──
    {"lemma": "piękny", "forms": ["piękny", "piękna", "piękne", "piękni"], "pos": "adjective", "semantic_mass": mass(0.3, 0.2, 0.5, 0.8, 0.5, 0.6, 0.3, 0.5, 0.6)},
    {"lemma": "brzydki", "forms": ["brzydki", "brzydka", "brzydkie"], "pos": "adjective", "semantic_mass": mass(0.3, 0.2, 0.3, 0.6, 0.3, 0.4, 0.2, 0.3, 0.15)},
    {"lemma": "dobry", "forms": ["dobry", "dobra", "dobre", "dobrzy"], "pos": "adjective", "semantic_mass": mass(0.2, 0.4, 0.7, 0.7, 0.5, 0.5, 0.3, 0.6, 0.9)},
    {"lemma": "zły", "forms": ["zły", "zła", "złe", "źli"], "pos": "adjective", "semantic_mass": mass(0.3, 0.4, 0.5, 0.7, 0.4, 0.4, 0.3, 0.5, 0.1)},
    {"lemma": "smutny", "forms": ["smutny", "smutna", "smutne"], "pos": "adjective", "semantic_mass": mass(0.2, 0.2, 0.4, 0.8, 0.4, 0.3, 0.4, 0.3, 0.2)},
    {"lemma": "radosny", "forms": ["radosny", "radosna", "radosne"], "pos": "adjective", "semantic_mass": mass(0.2, 0.3, 0.5, 0.85, 0.4, 0.3, 0.2, 0.4, 0.5)},
    {"lemma": "spokojny", "forms": ["spokojny", "spokojna", "spokojne"], "pos": "adjective", "semantic_mass": mass(0.2, 0.15, 0.5, 0.7, 0.4, 0.4, 0.5, 0.5, 0.6)},
    {"lemma": "silny", "forms": ["silny", "silna", "silne", "silni"], "pos": "adjective", "semantic_mass": mass(0.4, 0.7, 0.5, 0.4, 0.3, 0.3, 0.3, 0.5, 0.4)},
    {"lemma": "słaby", "forms": ["słaby", "słaba", "słabe"], "pos": "adjective", "semantic_mass": mass(0.3, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2)},
    {"lemma": "czuły", "forms": ["czuły", "czuła", "czułe"], "pos": "adjective", "semantic_mass": mass(0.2, 0.2, 0.7, 0.8, 0.5, 0.4, 0.3, 0.5, 0.6)},

    # ── Adjectives: Physical (~8) ──
    {"lemma": "wielki", "forms": ["wielki", "wielka", "wielkie", "wielcy"], "pos": "adjective", "semantic_mass": mass(0.5, 0.4, 0.4, 0.5, 0.4, 0.4, 0.3, 0.4, 0.4)},
    {"lemma": "mały", "forms": ["mały", "mała", "małe"], "pos": "adjective", "semantic_mass": mass(0.5, 0.2, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2)},
    {"lemma": "wysoki", "forms": ["wysoki", "wysoka", "wysokie"], "pos": "adjective", "semantic_mass": mass(0.6, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2)},
    {"lemma": "głęboki", "forms": ["głęboki", "głęboka", "głębokie"], "pos": "adjective", "semantic_mass": mass(0.5, 0.2, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3)},
    {"lemma": "jasny", "forms": ["jasny", "jasna", "jasne"], "pos": "adjective", "semantic_mass": mass(0.4, 0.15, 0.3, 0.5, 0.3, 0.3, 0.2, 0.3, 0.4)},
    {"lemma": "ciemny", "forms": ["ciemny", "ciemna", "ciemne"], "pos": "adjective", "semantic_mass": mass(0.4, 0.15, 0.3, 0.5, 0.3, 0.4, 0.3, 0.3, 0.2)},
    {"lemma": "ciepły", "forms": ["ciepły", "ciepła", "ciepłe"], "pos": "adjective", "semantic_mass": mass(0.5, 0.1, 0.3, 0.5, 0.3, 0.2, 0.2, 0.2, 0.3)},
    {"lemma": "zimny", "forms": ["zimny", "zimna", "zimne"], "pos": "adjective", "semantic_mass": mass(0.5, 0.1, 0.3, 0.4, 0.2, 0.2, 0.2, 0.2, 0.15)},

    # ── Adjectives: Cognitive (~6) ──
    {"lemma": "mądry", "forms": ["mądry", "mądra", "mądre", "mądrzy"], "pos": "adjective", "semantic_mass": mass(0.1, 0.5, 0.5, 0.3, 0.5, 0.8, 0.3, 0.6, 0.7)},
    {"lemma": "głupi", "forms": ["głupi", "głupia", "głupie"], "pos": "adjective", "semantic_mass": mass(0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.2, 0.3, 0.15)},
    {"lemma": "prawdziwy", "forms": ["prawdziwy", "prawdziwa", "prawdziwe"], "pos": "adjective", "semantic_mass": mass(0.2, 0.3, 0.6, 0.5, 0.5, 0.7, 0.4, 0.6, 0.8)},
    {"lemma": "fałszywy", "forms": ["fałszywy", "fałszywa", "fałszywe"], "pos": "adjective", "semantic_mass": mass(0.2, 0.3, 0.4, 0.5, 0.3, 0.6, 0.3, 0.4, 0.1)},
    {"lemma": "dziwny", "forms": ["dziwny", "dziwna", "dziwne"], "pos": "adjective", "semantic_mass": mass(0.2, 0.2, 0.3, 0.4, 0.3, 0.5, 0.3, 0.3, 0.2)},

    # ── Adverbs (~15) ──
    {"lemma": "zawsze", "forms": ["zawsze"], "pos": "adverb", "semantic_mass": mass(0.05, 0.1, 0.3, 0.2, 0.3, 0.6, 0.9, 0.2, 0.2)},
    {"lemma": "nigdy", "forms": ["nigdy"], "pos": "adverb", "semantic_mass": mass(0.05, 0.1, 0.2, 0.3, 0.2, 0.6, 0.8, 0.2, 0.15)},
    {"lemma": "często", "forms": ["często"], "pos": "adverb", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.2, 0.3, 0.7, 0.15, 0.15)},
    {"lemma": "rzadko", "forms": ["rzadko"], "pos": "adverb", "semantic_mass": mass(0.2, 0.15, 0.2, 0.15, 0.15, 0.3, 0.6, 0.15, 0.15)},
    {"lemma": "już", "forms": ["już"], "pos": "adverb", "semantic_mass": mass(0.1, 0.1, 0.2, 0.2, 0.2, 0.4, 0.7, 0.2, 0.15)},
    {"lemma": "jeszcze", "forms": ["jeszcze"], "pos": "adverb", "semantic_mass": mass(0.1, 0.15, 0.2, 0.2, 0.2, 0.4, 0.6, 0.2, 0.15)},
    {"lemma": "dopiero", "forms": ["dopiero"], "pos": "adverb", "semantic_mass": mass(0.1, 0.15, 0.2, 0.15, 0.15, 0.4, 0.6, 0.15, 0.15)},
    {"lemma": "bardzo", "forms": ["bardzo"], "pos": "adverb", "semantic_mass": mass(0.15, 0.1, 0.3, 0.4, 0.2, 0.3, 0.2, 0.15, 0.15)},
    {"lemma": "tylko", "forms": ["tylko"], "pos": "adverb", "semantic_mass": mass(0.05, 0.1, 0.2, 0.15, 0.15, 0.5, 0.2, 0.15, 0.15)},
    {"lemma": "nawet", "forms": ["nawet"], "pos": "adverb", "semantic_mass": mass(0.1, 0.15, 0.2, 0.2, 0.15, 0.4, 0.2, 0.15, 0.15)},
    {"lemma": "właśnie", "forms": ["właśnie"], "pos": "adverb", "semantic_mass": mass(0.1, 0.15, 0.2, 0.2, 0.15, 0.4, 0.3, 0.15, 0.15)},
    {"lemma": "potem", "forms": ["potem"], "pos": "adverb", "semantic_mass": mass(0.1, 0.1, 0.2, 0.15, 0.2, 0.3, 0.7, 0.15, 0.15)},
    {"lemma": "tutaj", "forms": ["tutaj", "tu"], "pos": "adverb", "semantic_mass": mass(0.4, 0.1, 0.2, 0.15, 0.2, 0.2, 0.3, 0.15, 0.15)},
    {"lemma": "tam", "forms": ["tam"], "pos": "adverb", "semantic_mass": mass(0.3, 0.1, 0.2, 0.15, 0.2, 0.2, 0.3, 0.15, 0.15)},

    # ── Pronouns (~20) ──
    {"lemma": "ja", "forms": ["ja", "mnie", "mi", "mną"], "pos": "pronoun", "case_forms": {"ja": "Nom", "mnie": "Acc", "mi": "Dat", "mną": "Ins"}, "semantic_mass": mass(0.3, 0.6, 0.5, 0.3, 0.4, 0.3, 0.3, 0.95, 0.4)},
    {"lemma": "ty", "forms": ["ty", "ciebie", "tobie", "tobą"], "pos": "pronoun", "case_forms": {"ty": "Nom", "ciebie": "Acc", "tobie": "Dat", "tobą": "Ins"}, "semantic_mass": mass(0.3, 0.5, 0.6, 0.3, 0.3, 0.3, 0.3, 0.8, 0.4)},
    {"lemma": "on", "forms": ["on", "jego", "jemu", "nim"], "pos": "pronoun", "case_forms": {"on": "Nom", "jego": "Acc", "jemu": "Dat", "nim": "Ins"}, "semantic_mass": mass(0.4, 0.4, 0.4, 0.2, 0.3, 0.2, 0.2, 0.4, 0.3)},
    {"lemma": "ona", "forms": ["ona", "jej", "nią"], "pos": "pronoun", "case_forms": {"ona": "Nom", "jej": "Acc", "nią": "Ins"}, "semantic_mass": mass(0.4, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.4, 0.3)},
    {"lemma": "my", "forms": ["my", "nas", "nam", "nami"], "pos": "pronoun", "semantic_mass": mass(0.3, 0.5, 0.7, 0.3, 0.4, 0.3, 0.3, 0.8, 0.5)},
    {"lemma": "wy", "forms": ["wy", "was", "wam", "wami"], "pos": "pronoun", "semantic_mass": mass(0.3, 0.5, 0.6, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4)},
    {"lemma": "się", "forms": ["się"], "pos": "pronoun", "semantic_mass": mass(0.1, 0.2, 0.5, 0.1, 0.1, 0.4, 0.1, 0.2, 0.1)},
    {"lemma": "co", "forms": ["co"], "pos": "pronoun", "semantic_mass": mass(0.05, 0.2, 0.3, 0.1, 0.15, 0.5, 0.15, 0.2, 0.15)},
    {"lemma": "kto", "forms": ["kto", "kogo", "komu", "kim"], "pos": "pronoun", "semantic_mass": mass(0.2, 0.4, 0.3, 0.15, 0.15, 0.3, 0.15, 0.3, 0.2)},
    {"lemma": "nic", "forms": ["nic", "niczego", "niczym"], "pos": "pronoun", "semantic_mass": mass(0.05, 0.05, 0.2, 0.3, 0.15, 0.6, 0.2, 0.15, 0.1)},
    {"lemma": "wszystko", "forms": ["wszystko", "wszystkiego", "wszystkim"], "pos": "pronoun", "semantic_mass": mass(0.1, 0.2, 0.4, 0.2, 0.3, 0.5, 0.3, 0.3, 0.3)},
    {"lemma": "ten", "forms": ["ten", "ta", "to", "te", "ci"], "pos": "pronoun", "semantic_mass": mass(0.3, 0.2, 0.3, 0.15, 0.2, 0.3, 0.2, 0.2, 0.15)},

    # ── Prepositions (~20) ──
    {"lemma": "w", "forms": ["w", "we"], "pos": "preposition", "governs": ["Loc", "Acc"], "semantic_mass": mass(0.3, 0.15, 0.5, 0.1, 0.15, 0.3, 0.2, 0.15, 0.1)},
    {"lemma": "na", "forms": ["na"], "pos": "preposition", "governs": ["Loc", "Acc"], "semantic_mass": mass(0.4, 0.15, 0.4, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1)},
    {"lemma": "z", "forms": ["z", "ze"], "pos": "preposition", "governs": ["Gen", "Ins"], "semantic_mass": mass(0.2, 0.2, 0.5, 0.15, 0.15, 0.2, 0.15, 0.2, 0.15)},
    {"lemma": "do", "forms": ["do"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.2, 0.2, 0.4, 0.1, 0.15, 0.2, 0.3, 0.15, 0.15)},
    {"lemma": "od", "forms": ["od", "ode"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.2, 0.15, 0.3, 0.1, 0.15, 0.2, 0.3, 0.15, 0.1)},
    {"lemma": "przez", "forms": ["przez"], "pos": "preposition", "governs": ["Acc"], "semantic_mass": mass(0.3, 0.2, 0.4, 0.2, 0.15, 0.2, 0.3, 0.15, 0.15)},
    {"lemma": "dla", "forms": ["dla"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.15, 0.2, 0.6, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3)},
    {"lemma": "bez", "forms": ["bez"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.15, 0.1, 0.3, 0.3, 0.15, 0.3, 0.2, 0.15, 0.1)},
    {"lemma": "o", "forms": ["o"], "pos": "preposition", "governs": ["Loc", "Acc"], "semantic_mass": mass(0.15, 0.15, 0.3, 0.15, 0.1, 0.2, 0.15, 0.15, 0.1)},
    {"lemma": "po", "forms": ["po"], "pos": "preposition", "governs": ["Loc", "Acc"], "semantic_mass": mass(0.3, 0.15, 0.3, 0.15, 0.15, 0.2, 0.4, 0.15, 0.1)},
    {"lemma": "przy", "forms": ["przy"], "pos": "preposition", "governs": ["Loc"], "semantic_mass": mass(0.3, 0.15, 0.4, 0.15, 0.15, 0.15, 0.2, 0.15, 0.1)},
    {"lemma": "między", "forms": ["między"], "pos": "preposition", "governs": ["Ins", "Acc"], "semantic_mass": mass(0.2, 0.15, 0.5, 0.15, 0.15, 0.2, 0.2, 0.15, 0.15)},
    {"lemma": "nad", "forms": ["nad", "nade"], "pos": "preposition", "governs": ["Ins", "Acc"], "semantic_mass": mass(0.3, 0.15, 0.3, 0.15, 0.15, 0.15, 0.15, 0.15, 0.1)},
    {"lemma": "pod", "forms": ["pod", "pode"], "pos": "preposition", "governs": ["Ins", "Acc"], "semantic_mass": mass(0.3, 0.15, 0.3, 0.1, 0.15, 0.15, 0.15, 0.15, 0.1)},
    {"lemma": "przed", "forms": ["przed", "przede"], "pos": "preposition", "governs": ["Ins", "Acc"], "semantic_mass": mass(0.2, 0.15, 0.3, 0.15, 0.15, 0.2, 0.4, 0.15, 0.1)},
    {"lemma": "za", "forms": ["za"], "pos": "preposition", "governs": ["Ins", "Acc", "Gen"], "semantic_mass": mass(0.2, 0.15, 0.3, 0.15, 0.15, 0.2, 0.3, 0.15, 0.15)},
    {"lemma": "wśród", "forms": ["wśród"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.2, 0.15, 0.5, 0.15, 0.15, 0.2, 0.2, 0.15, 0.15)},
    {"lemma": "według", "forms": ["według"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.1, 0.15, 0.4, 0.1, 0.15, 0.4, 0.2, 0.15, 0.2)},
    {"lemma": "obok", "forms": ["obok"], "pos": "preposition", "governs": ["Gen"], "semantic_mass": mass(0.3, 0.15, 0.3, 0.1, 0.15, 0.15, 0.2, 0.15, 0.1)},
    {"lemma": "przeciw", "forms": ["przeciw", "przeciwko"], "pos": "preposition", "governs": ["Dat"], "semantic_mass": mass(0.2, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.3, 0.15)},

    # ── Conjunctions (~12) ──
    {"lemma": "i", "forms": ["i"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.1, 0.6, 0.1, 0.1, 0.3, 0.15, 0.1, 0.1)},
    {"lemma": "a", "forms": ["a"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.5, 0.15, 0.1, 0.3, 0.15, 0.1, 0.1)},
    {"lemma": "ale", "forms": ["ale"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.5, 0.2, 0.1, 0.3, 0.15, 0.1, 0.15)},
    {"lemma": "lub", "forms": ["lub", "albo"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.1, 0.4, 0.1, 0.1, 0.3, 0.1, 0.1, 0.1)},
    {"lemma": "więc", "forms": ["więc", "zatem"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.5, 0.15, 0.1, 0.4, 0.2, 0.1, 0.15)},
    {"lemma": "że", "forms": ["że", "iż"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.1, 0.5, 0.1, 0.1, 0.4, 0.1, 0.1, 0.1)},
    {"lemma": "gdy", "forms": ["gdy", "kiedy"], "pos": "conjunction", "semantic_mass": mass(0.1, 0.1, 0.4, 0.15, 0.15, 0.3, 0.6, 0.1, 0.1)},
    {"lemma": "jeśli", "forms": ["jeśli", "jeżeli"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.4, 0.15, 0.1, 0.5, 0.3, 0.1, 0.15)},
    {"lemma": "chociaż", "forms": ["chociaż", "choć"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.4, 0.2, 0.1, 0.3, 0.15, 0.1, 0.15)},
    {"lemma": "ponieważ", "forms": ["ponieważ", "bo"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.15, 0.5, 0.15, 0.1, 0.4, 0.2, 0.1, 0.15)},
    {"lemma": "aby", "forms": ["aby", "żeby"], "pos": "conjunction", "semantic_mass": mass(0.05, 0.2, 0.4, 0.2, 0.15, 0.4, 0.3, 0.15, 0.15)},

    # ── Particles (~10) ──
    {"lemma": "nie", "forms": ["nie"], "pos": "particle", "operator": "negation", "semantic_mass": mass(0.05, 0.1, 0.3, 0.3, 0.1, 0.4, 0.15, 0.1, 0.1)},
    {"lemma": "czy", "forms": ["czy"], "pos": "particle", "operator": "interrogative", "semantic_mass": mass(0.05, 0.2, 0.3, 0.2, 0.1, 0.4, 0.15, 0.1, 0.1)},
    {"lemma": "niech", "forms": ["niech"], "pos": "particle", "operator": "optative", "semantic_mass": mass(0.05, 0.3, 0.3, 0.3, 0.15, 0.3, 0.2, 0.15, 0.15)},
    {"lemma": "może", "forms": ["może"], "pos": "particle", "operator": "modal", "semantic_mass": mass(0.05, 0.2, 0.3, 0.2, 0.1, 0.5, 0.2, 0.1, 0.1)},
    {"lemma": "no", "forms": ["no"], "pos": "particle", "operator": "emphasis", "semantic_mass": mass(0.1, 0.15, 0.2, 0.2, 0.1, 0.2, 0.1, 0.1, 0.1)},
    {"lemma": "tak", "forms": ["tak"], "pos": "particle", "operator": "affirmation", "semantic_mass": mass(0.1, 0.2, 0.3, 0.2, 0.1, 0.3, 0.1, 0.15, 0.15)},
    {"lemma": "aż", "forms": ["aż"], "pos": "particle", "operator": "emphasis", "semantic_mass": mass(0.1, 0.15, 0.2, 0.3, 0.1, 0.2, 0.2, 0.1, 0.1)},
    {"lemma": "by", "forms": ["by"], "pos": "particle", "operator": "conditional", "semantic_mass": mass(0.05, 0.15, 0.3, 0.1, 0.1, 0.5, 0.2, 0.1, 0.1)},
    {"lemma": "oto", "forms": ["oto"], "pos": "particle", "operator": "presentative", "semantic_mass": mass(0.2, 0.15, 0.2, 0.2, 0.1, 0.2, 0.15, 0.1, 0.1)},

    # ── Numerals (~8) ──
    {"lemma": "jeden", "forms": ["jeden", "jedna", "jedno", "jedni"], "pos": "numeral", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.2, 0.5, 0.2, 0.2, 0.15)},
    {"lemma": "dwa", "forms": ["dwa", "dwie", "dwaj", "dwóch"], "pos": "numeral", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.15, 0.4, 0.15, 0.15, 0.1)},
    {"lemma": "trzy", "forms": ["trzy", "trzej"], "pos": "numeral", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.15, 0.4, 0.15, 0.15, 0.1)},
    {"lemma": "cztery", "forms": ["cztery", "czterej"], "pos": "numeral", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.15, 0.4, 0.15, 0.15, 0.1)},
    {"lemma": "pięć", "forms": ["pięć", "pięciu"], "pos": "numeral", "semantic_mass": mass(0.2, 0.2, 0.3, 0.15, 0.15, 0.4, 0.15, 0.15, 0.1)},
    {"lemma": "dwa razy", "forms": ["dwa razy"], "pos": "numeral", "semantic_mass": mass(0.15, 0.15, 0.3, 0.1, 0.1, 0.4, 0.2, 0.1, 0.1)},
    {"lemma": "wiele", "forms": ["wiele", "wielu"], "pos": "numeral", "semantic_mass": mass(0.15, 0.2, 0.4, 0.15, 0.2, 0.4, 0.2, 0.15, 0.15)},
    {"lemma": "mało", "forms": ["mało"], "pos": "numeral", "semantic_mass": mass(0.15, 0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.1, 0.1)},

    # ── Interjections (~5) ──
    {"lemma": "ach", "forms": ["ach"], "pos": "interjection", "semantic_mass": mass(0.1, 0.15, 0.2, 0.7, 0.2, 0.2, 0.1, 0.15, 0.15)},
    {"lemma": "och", "forms": ["och"], "pos": "interjection", "semantic_mass": mass(0.1, 0.15, 0.2, 0.7, 0.2, 0.2, 0.1, 0.15, 0.15)},
    {"lemma": "hej", "forms": ["hej"], "pos": "interjection", "semantic_mass": mass(0.2, 0.2, 0.3, 0.5, 0.15, 0.15, 0.1, 0.15, 0.15)},
    {"lemma": "biada", "forms": ["biada"], "pos": "interjection", "semantic_mass": mass(0.15, 0.15, 0.2, 0.75, 0.15, 0.2, 0.15, 0.15, 0.1)},
    {"lemma": "precz", "forms": ["precz"], "pos": "interjection", "semantic_mass": mass(0.3, 0.4, 0.3, 0.6, 0.15, 0.2, 0.15, 0.15, 0.1)},
]

if __name__ == "__main__":
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))

    # Merge seed vocabulary + new lexemes, deduplicate by lemma
    seen_lemmas: set[str] = set()
    merged_vocab = []
    for item in seed.get("vocabulary", []):
        lemma = item["lemma"]
        if lemma not in seen_lemmas:
            seen_lemmas.add(lemma)
            merged_vocab.append(item)
    for item in LEXICON:
        lemma = item["lemma"]
        if lemma not in seen_lemmas:
            seen_lemmas.add(lemma)
            merged_vocab.append(item)

    out = dict(seed)
    out["vocabulary"] = merged_vocab
    out["status"] = "seed_runtime_adapter_generated_v02"
    out["lexeme_count"] = len(merged_vocab)
    STAT = {"pos": {}, "total": len(merged_vocab)}
    for v in merged_vocab:
        p = v["pos"]
        STAT["pos"][p] = STAT["pos"].get(p, 0) + 1
    out["statistics"] = STAT

    OUT_PATH.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Written {len(merged_vocab)} lexemes to {OUT_PATH}")
    print(f"Stats: {STAT}")

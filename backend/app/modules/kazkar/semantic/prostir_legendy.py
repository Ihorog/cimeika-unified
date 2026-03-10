"""
Prostir Legendy — semantic node definitions for the Kazkar legend space.
10 nodes mirroring the cit/zdibnosti/kazkar semantic graph.
"""
from typing import Dict, List, Optional

# Each node: id, nazva, opys, hlybyna, zv_yazani_vuzly, rezonansni_sensy, arkhetyp
NODES: List[Dict] = [
    {
        "id": "prysutnist",
        "nazva": "Присутність",
        "opys": "Стан повного усвідомленого буття тут і зараз",
        "hlybyna": 0,
        "zv_yazani_vuzly": ["tysha", "dostatnist", "moment"],
        "rezonansni_sensy": ["усвідомленість", "тут", "зараз"],
        "arkhetyp": "Центр",
    },
    {
        "id": "tysha",
        "nazva": "Тиша",
        "opys": "Простір між думками, де народжується ясність",
        "hlybyna": 1,
        "zv_yazani_vuzly": ["prysutnist", "spokiy"],
        "rezonansni_sensy": ["спокій", "ясність", "простір"],
        "arkhetyp": "Порожнеча",
    },
    {
        "id": "dostatnist",
        "nazva": "Достатність",
        "opys": "Відчуття повноти без потреби у більшому",
        "hlybyna": 1,
        "zv_yazani_vuzly": ["prysutnist", "balans"],
        "rezonansni_sensy": ["повнота", "достатньо", "баланс"],
        "arkhetyp": "Достаток",
    },
    {
        "id": "moment",
        "nazva": "Момент",
        "opys": "Неподільна одиниця живого досвіду",
        "hlybyna": 1,
        "zv_yazani_vuzly": ["prysutnist", "chas"],
        "rezonansni_sensy": ["мить", "досвід", "живе"],
        "arkhetyp": "Іскра",
    },
    {
        "id": "spokiy",
        "nazva": "Спокій",
        "opys": "Стійкість посеред змін",
        "hlybyna": 2,
        "zv_yazani_vuzly": ["tysha", "pryynyattya"],
        "rezonansni_sensy": ["стійкість", "рівновага", "спокій"],
        "arkhetyp": "Якір",
    },
    {
        "id": "pryynyattya",
        "nazva": "Прийняття",
        "opys": "Відкритість до того, що є",
        "hlybyna": 2,
        "zv_yazani_vuzly": ["spokiy", "mudrist"],
        "rezonansni_sensy": ["відкритість", "прийняття", "є"],
        "arkhetyp": "Відкритість",
    },
    {
        "id": "chas",
        "nazva": "Час",
        "opys": "Ріка змін, що несе досвід",
        "hlybyna": 2,
        "zv_yazani_vuzly": ["moment", "tsykl"],
        "rezonansni_sensy": ["зміна", "плин", "досвід"],
        "arkhetyp": "Ріка",
    },
    {
        "id": "balans",
        "nazva": "Баланс",
        "opys": "Гармонія між протилежностями",
        "hlybyna": 2,
        "zv_yazani_vuzly": ["dostatnist", "mudrist"],
        "rezonansni_sensy": ["гармонія", "рівновага", "між"],
        "arkhetyp": "Терези",
    },
    {
        "id": "mudrist",
        "nazva": "Мудрість",
        "opys": "Знання, що виросло з досвіду",
        "hlybyna": 3,
        "zv_yazani_vuzly": ["pryynyattya", "balans"],
        "rezonansni_sensy": ["знання", "досвід", "глибина"],
        "arkhetyp": "Мудрець",
    },
    {
        "id": "tsykl",
        "nazva": "Цикл",
        "opys": "Повернення на новому рівні усвідомлення",
        "hlybyna": 3,
        "zv_yazani_vuzly": ["chas", "prysutnist"],
        "rezonansni_sensy": ["повернення", "спіраль", "ріст"],
        "arkhetyp": "Спіраль",
    },
]

_NODE_MAP: Dict[str, Dict] = {n["id"]: n for n in NODES}


def get_node(node_id: str) -> Optional[Dict]:
    return _NODE_MAP.get(node_id)


def get_all_nodes() -> List[Dict]:
    return NODES

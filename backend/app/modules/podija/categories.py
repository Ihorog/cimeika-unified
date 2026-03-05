"""
PoDiya category and subcategory definitions.

Seven main categories for organising ПоДія events, each with
topic-specific subcategories as described in the Cimeika ecosystem spec.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel


class SubcategorySchema(BaseModel):
    slug: str
    name: str


class CategorySchema(BaseModel):
    slug: str
    name: str
    subcategories: List[SubcategorySchema]


PODIYA_CATEGORIES: Dict[str, Dict] = {
    "weather": {
        "name": "Погода",
        "slug": "weather",
        "subcategories": [
            {"slug": "forecast_day",     "name": "Прогноз на день"},
            {"slug": "forecast_week",    "name": "Тижневий прогноз"},
            {"slug": "meteorological",   "name": "Метеорологічні явища"},
            {"slug": "historical",       "name": "Історичні дані погоди"},
            {"slug": "health_impact",    "name": "Вплив погоди на здоров'я"},
            {"slug": "climate_change",   "name": "Кліматичні зміни"},
            {"slug": "regional",         "name": "Прогноз для різних регіонів"},
        ],
    },
    "horoscopes": {
        "name": "Гороскопи",
        "slug": "horoscopes",
        "subcategories": [
            {"slug": "daily",            "name": "Щоденний гороскоп"},
            {"slug": "weekly",           "name": "Тижневий гороскоп"},
            {"slug": "monthly",          "name": "Місячний гороскоп"},
            {"slug": "astro_profiles",   "name": "Астрологічні профілі"},
            {"slug": "compatibility",    "name": "Сумісність знаків"},
            {"slug": "transits",         "name": "Астрологічні транзити"},
            {"slug": "personal",         "name": "Персональний гороскоп"},
        ],
    },
    "events": {
        "name": "Події",
        "slug": "events",
        "subcategories": [
            {"slug": "local",            "name": "Місцеві події"},
            {"slug": "cultural",         "name": "Культурні заходи"},
            {"slug": "sports",           "name": "Спортивні події"},
            {"slug": "festivals",        "name": "Фестивалі та ярмарки"},
            {"slug": "concerts",         "name": "Виставки та концерти"},
            {"slug": "educational",      "name": "Освітні події"},
            {"slug": "travel",           "name": "Подорожі та туризм"},
        ],
    },
    "games": {
        "name": "Ігри",
        "slug": "games",
        "subcategories": [
            {"slug": "logic",            "name": "Логічні ігри"},
            {"slug": "strategy",         "name": "Стратегічні ігри"},
            {"slug": "casual",           "name": "Казуальні ігри"},
            {"slug": "educational",      "name": "Освітні ігри"},
            {"slug": "sports_sim",       "name": "Спортивні симулятори"},
            {"slug": "mobile",           "name": "Мобільні ігри"},
            {"slug": "kids",             "name": "Розвиваючі ігри для дітей"},
        ],
    },
    "holidays": {
        "name": "Організація свят",
        "slug": "holidays",
        "subcategories": [
            {"slug": "family",           "name": "Сімейні свята"},
            {"slug": "corporate",        "name": "Корпоративні заходи"},
            {"slug": "kids_parties",     "name": "Дитячі свята"},
            {"slug": "weddings",         "name": "Весілля та ювілеї"},
            {"slug": "themed",           "name": "Тематичні вечірки"},
            {"slug": "gift_ideas",       "name": "Подарункові ідеї"},
            {"slug": "decor",            "name": "Святковий декор"},
        ],
    },
    "leisure": {
        "name": "Дозвілля",
        "slug": "leisure",
        "subcategories": [
            {"slug": "cinema",           "name": "Кіно та серіали"},
            {"slug": "literature",       "name": "Література та книги"},
            {"slug": "theater_music",    "name": "Театр та музика"},
            {"slug": "outdoor",          "name": "Відпочинок на природі"},
            {"slug": "hobbies",          "name": "Хобі та захоплення"},
            {"slug": "video_games",      "name": "Відеоігри"},
            {"slug": "art",              "name": "Мистецтво та виставки"},
        ],
    },
    "quests": {
        "name": "Квести",
        "slug": "quests",
        "subcategories": [
            {"slug": "city",             "name": "Міські квести"},
            {"slug": "online",           "name": "Онлайн-квести"},
            {"slug": "interactive",      "name": "Інтерактивні історії"},
            {"slug": "kids",             "name": "Квести для дітей"},
            {"slug": "themed",           "name": "Тематичні квести"},
            {"slug": "extreme",          "name": "Екстремальні квести"},
            {"slug": "educational",      "name": "Освітні квести"},
        ],
    },
}


def get_all_categories() -> List[CategorySchema]:
    """Return list of all categories with their subcategories."""
    return [CategorySchema(**v) for v in PODIYA_CATEGORIES.values()]


def get_category(slug: str) -> Optional[CategorySchema]:
    """Return a single category by slug, or None if not found."""
    data = PODIYA_CATEGORIES.get(slug)
    return CategorySchema(**data) if data else None


VALID_CATEGORY_SLUGS: List[str] = list(PODIYA_CATEGORIES.keys())

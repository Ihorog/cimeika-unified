#!/usr/bin/env python3
"""
Експорт легенд Ci з cimeika-unified в Markdown формат для ciwiki

Цей скрипт експортує всі легенди Ci з бази даних Kazkar
у формат Markdown, готовий для копіювання в ciwiki репозиторій.
"""

import sys
import re
import traceback
from datetime import datetime
from pathlib import Path

# Додаємо шлях до backend модулів
backend_path = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(backend_path))

from config.database import SessionLocal
from modules.kazkar.service import KazkarService


def sanitize_filename(title: str) -> str:
    """Конвертує назву легенди в безпечне ім'я файлу
    
    Підтримує кириличні символи (українська, російська).
    """
    # Замінюємо пробіли на дефіси
    safe_title = title.replace(' ', '-')
    # Видаляємо спеціальні символи, але зберігаємо кирилицю, латиницю, цифри і дефіси
    safe_title = re.sub(r'[^\w\-]', '', safe_title, flags=re.UNICODE)
    # Видаляємо подвійні дефіси
    safe_title = re.sub(r'-+', '-', safe_title)
    # Видаляємо дефіси на початку/кінці
    safe_title = safe_title.strip('-')
    return safe_title


def legend_to_markdown(legend, index: int) -> str:
    """Конвертує легенду в Markdown формат"""
    
    # Заголовок
    md = f"# {legend.title}\n\n"
    
    # Метадані
    md += "## 📋 Метадані\n\n"
    md += f"- **ID**: {legend.id}\n"
    md += f"- **Тип**: {legend.story_type}\n"
    
    if legend.participants:
        md += f"- **Учасники**: {', '.join(legend.participants)}\n"
    
    if legend.location:
        md += f"- **Локація**: {legend.location}\n"
    
    if legend.tags:
        md += f"- **Теги**: {', '.join([f'`{tag}`' for tag in legend.tags])}\n"
    
    md += f"- **Дата створення**: {legend.time.strftime('%d.%m.%Y')}\n"
    md += f"- **Canon Bundle**: {legend.canon_bundle_id}\n"
    md += "\n---\n\n"
    
    # Основний текст
    md += "## 📖 Текст легенди\n\n"
    md += legend.content
    md += "\n\n---\n\n"
    
    # Футер
    md += "## 🔗 Посилання\n\n"
    md += f"- **Джерело**: [cimeika-unified/kazkar](https://github.com/Ihorog/cimeika-unified)\n"
    md += f"- **Інтерактивний перегляд**: [/kazkar/legends](https://cimeika.app/kazkar/legends)\n"
    md += f"- **API**: `GET /api/v1/kazkar/stories/{legend.id}`\n"
    md += "\n---\n\n"
    md += f"_Експортовано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}_\n"
    
    return md


def create_index_md(legends) -> str:
    """Створює індексний файл README.md для розділу Легенда Сі"""
    
    md = "# Легенда Сі\n\n"
    md += "> Бібліотека легенд системи Cimeika\n\n"
    md += "---\n\n"
    
    md += "## 🎯 Про Легенду Сі\n\n"
    md += "**Легенда Сі** — це збірка текстових матеріалів, які описують:\n"
    md += "- Походження та філософію системи Cimeika\n"
    md += "- Історію створення модулів\n"
    md += "- Міфологію та символізм системи\n"
    md += "- Ключові принципи та цінності\n\n"
    
    md += "---\n\n"
    
    md += "## 📚 Легенди\n\n"
    md += f"**Всього легенд**: {len(legends)}\n\n"
    
    for i, legend in enumerate(legends, 1):
        filename = sanitize_filename(legend.title)
        md += f"### {i}. [{legend.title}](./{str(i).zfill(2)}-{filename}.md)\n\n"
        
        # Короткий опис (перші 200 символів)
        preview = legend.content[:200].replace("\n", " ")
        if len(legend.content) > 200:
            preview += "..."
        md += f"{preview}\n\n"
        
        # Теги
        if legend.tags:
            md += f"**Теги**: {', '.join([f'`{tag}`' for tag in legend.tags])}\n\n"
    
    md += "---\n\n"
    
    md += "## 🔗 Інтерактивний інтерфейс\n\n"
    md += "Ці файли є статичною копією для документаційних цілей.\n\n"
    md += "**Для повноцінної роботи з легендами використовуйте інтерактивний інтерфейс**:\n\n"
    md += "🌐 [Легенди Ci в Cimeika](https://cimeika.app/kazkar/legends)\n\n"
    md += "**Можливості інтерактивного інтерфейсу**:\n"
    md += "- 🔍 Пошук легенд\n"
    md += "- 🏷️ Фільтрація за тегами\n"
    md += "- 📖 Зручний перегляд з метаданими\n"
    md += "- ✏️ Створення нових легенд\n"
    md += "- 🔄 Завжди актуальний контент\n\n"
    
    md += "---\n\n"
    
    md += "## 📊 Технічна інформація\n\n"
    md += "- **Модуль**: Kazkar (хранитель пам'яті та легенд)\n"
    md += "- **База даних**: PostgreSQL\n"
    md += "- **API**: FastAPI REST\n"
    md += "- **Frontend**: React + TypeScript\n"
    md += "- **Canon Bundle**: CIMEIKA_CANON_TZ_v1\n\n"
    
    md += "---\n\n"
    
    md += "## 📞 Документація\n\n"
    md += "Детальну інформацію дивіться:\n"
    md += "- [CI_LEGENDS_UNIFIED_RESOURCE.md](https://github.com/Ihorog/cimeika-unified/blob/main/docs/CI_LEGENDS_UNIFIED_RESOURCE.md)\n"
    md += "- [CI_LEGENDS_PLACEMENT.md](https://github.com/Ihorog/cimeika-unified/blob/main/docs/CI_LEGENDS_PLACEMENT.md)\n"
    md += "- [Документація Kazkar](https://github.com/Ihorog/cimeika-unified/blob/main/docs/modules/kazkar.md)\n\n"
    
    md += "---\n\n"
    md += f"_Експортовано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}_\n"
    
    return md


def main():
    """Головна функція експорту"""
    
    print("=" * 60)
    print("ЕКСПОРТ ЛЕГЕНД CI В MARKDOWN ДЛЯ CIWIKI")
    print("=" * 60)
    print()
    
    # Створюємо директорію для експорту
    export_dir = Path(__file__).parent.parent.parent / "tmp" / "ciwiki_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Директорія експорту: {export_dir}")
    print()
    
    # Підключаємося до БД
    db = SessionLocal()
    service = KazkarService()
    
    try:
        # Отримуємо всі легенди
        print("🔍 Завантаження легенд з бази даних...")
        legends = service.get_legends(db, skip=0, limit=100)
        
        if not legends:
            print("⚠️  Легенди не знайдені в базі даних.")
            print("💡 Спробуйте спочатку виконати: python backend/scripts/seed_ci_legends.py")
            return
        
        print(f"✅ Знайдено {len(legends)} легенд(и)\n")
        
        # Експортуємо кожну легенду
        print("📝 Експорт легенд в Markdown...\n")
        
        for i, legend in enumerate(legends, 1):
            # Генеруємо ім'я файлу
            safe_title = sanitize_filename(legend.title)
            filename = f"{str(i).zfill(2)}-{safe_title}.md"
            filepath = export_dir / filename
            
            # Конвертуємо в Markdown
            md_content = legend_to_markdown(legend, i)
            
            # Записуємо файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"  ✅ {i}. {legend.title}")
            print(f"     → {filename}")
        
        # Створюємо індексний файл
        print("\n📚 Створення індексного файлу README.md...")
        index_md = create_index_md(legends)
        index_path = export_dir / "README.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_md)
        
        print(f"  ✅ README.md створено")
        
        # Підсумок
        print("\n" + "=" * 60)
        print("✅ ЕКСПОРТ ЗАВЕРШЕНО УСПІШНО")
        print("=" * 60)
        print()
        print(f"📂 Експортовано {len(legends)} легенд(и) + README.md")
        print(f"📁 Локація: {export_dir}")
        print()
        print("📋 Наступні кроки:")
        print("  1. Перейдіть в ciwiki репозиторій")
        print("  2. Створіть папку 'Легенда-Сі' (якщо не існує)")
        print(f"  3. Скопіюйте файли з {export_dir}")
        print("  4. Commit та push в ciwiki")
        print()
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()

import json, os
def process_raw_text(ai_json_response):
    try:
        data = json.loads(ai_json_response)
        file_path = 'calendar.json'
        events = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                events = json.load(f)
        events.append(data)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        return f"Подію '{data.get('title')}' збережено в Ci-Пам'ять."
    except Exception as e:
        return f"Помилка: {str(e)}"

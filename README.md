# Исследование лексики авторов Telegram-каналов
## Обзор репозитория

- `data` - папка со всеми данными для анализа:
  - `data/raw` - данные после парсинга экспортных данных
  - `data/frequencies` - общие частотные списки по категориям
  - `data/rate` - процент встречаемости слов от всего количества
  - `result.json` - процент встречаемости слов, встречающиеся во всех категориях
- `converter.py` - парсер экспортных данных
- `analyzer.py` - составитель частотных списков
- `rate_converter.py` - подсчёт процентов встречаемости слов
- `comparator.py` - сопоставитель слов из всех категорий
- `stop_words.txt` - фильтр слов
- `requirements.txt` - файл зависимостей
- `config.example.ini` - пример конфигурационного файла
- `config.ini` - рабочий конфигурационный файл 
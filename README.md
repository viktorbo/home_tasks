# Тестовое задание

## Требования для запуска тестов
 - `Python 3.x` (`x` > 5)
 - наличие интернета и доступа к тестируемому сервису (_данные для авторизации_)

## Описание
Автотесты для предоставленного `API`. 
Реализовано 149 тест кейсов (включая параметризацию). 
Об API дана не вся информация, а потому присутствуют падающие тест кейсы. 
Их наличие позволяет оценить состояние тестиромого `API` и обнаружить спорные моменты или **_баги_**. 
Логирование и описание работы методов реализовано с помощью `allure`. 
Код содержит комментарии по поводу некоторых тест кейсов и/или параметров. 
Также для кажого класса в коде присутствует описание для чего предназначен класс и реализуемые в нём функции. 
- **Стек**: `PyTest` + `Requests` 
- **Логирование**: `Allure`
- **Валидация**: `Hamcrest`, `Cerberus` и стандартные инструменты `Python`
- **Генерирование некоторых тестовых данных**: `Faker`

## Структура репозитория
```
├── README.md
├── framework
│   ├── api.py
│   └── helpers
│       ├── checker.py
│       ├── credentials.py
│       ├── simple_response.py
│       └── utils.py
├── requirements.txt
└── tests
    ├── conftest.py
    ├── test_delete_character_by_name.py
    ├── test_get_character_by_name.py
    ├── test_get_characters.py
    ├── test_post_character.py
    ├── test_post_reset.py
    └── test_put_character.py
```
- `requirements.txt` - список зависимостей и их версий для `Python`
- `tests` - реализация тестов
- `framework/api.py` - реализация класса для работы с `API`
- `framework/helpers/checker.py` - класс для реализации методов прверки данных
- `framework/helpers/credentials.py` - класс для работы с данными авторизации
- `framework/helpers/simple_response.py` - структура для модификации ответа на запросы
- `framework/helpers/utils.py` - вспомогательные функции

## Инструкция для запуска тестов
  1. (_**опционально**_) Установить консольное приложение `allure` (установить можно с помощью `scoop` в **Windows**,`brew` в **MacOS**, на **Linux** вероятно из исходников)
  2. С помощью команды `git clone <HTTP ссылка на репозиторий>` скачать репозиторий с тестами
  3. Перейти в корень скачанного (в пункте 2) репозитория и добавить путь к текущему каталогу в `PYTHONPATH` (например командой `export PYTHONPATH=$PYTHONPATH:$PWD`)
  4. Создать (если нужно) и **активировать** виртуальное окружение для наших тестов
  5. Установить зависимости для `Python` командой `python3 -m pip install -r ./requirements.txt`
  6. Установить данные для авторизации в качестве переменных окружения `TEST_LOGIN` и `TEST_PASSWORD`
  7. Запустить тесты командой (на **Windows** может отличаться) `pytest -s -v --reruns=2 --alluredir=<пусть к папке с результатами> .`
  8. (_**опционально**_) Открыть тестовый отчет командой `allure serve <пусть к папке с результатами>` (команда `serve` может быть заменена на комбинацию команд `generate` и `open`)
  
 Тестовый отчет будет выглядеть примерно так:
<img width="1440" alt="Снимок экрана 2022-07-06 в 18 01 48" src="https://user-images.githubusercontent.com/15130588/177581851-4ccbf179-9fc7-4ab4-aa1d-d4b7d59c75e4.png">
<img width="1440" alt="Снимок экрана 2022-07-06 в 18 02 23" src="https://user-images.githubusercontent.com/15130588/177581974-0b4161e7-b660-4b72-98e9-127833f49baa.png">

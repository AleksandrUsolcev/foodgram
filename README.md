# Foodgram
![Python version](https://img.shields.io/badge/python-3.9-yellow) ![Django version](https://img.shields.io/badge/django-3.2-red)

Сервис "Продуктовый помощник", на котором пользователи публикуют рецепты блюд, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Рецепты так же можно добавлять в список покупок и выгрузить себе в PDF формате.

## Технологии

- [Python](https://www.python.org/) 3.9+
- [django](https://github.com/django/django) 3.2
- [django-rest-framework](https://github.com/encode/django-rest-framework)
  3.14
- [djoser](https://djoser.readthedocs.io/en/latest/index.html) 2.1
- [reportlab](https://pypi.org/project/reportlab/) 3.6
- [react](https://github.com/facebook/react) 16

## Запуск проекта в dev режиме

Клонировать репозиторий, перейти в папку с бэкендом, установить и активировать виртуальное окружение

```
cd backend
python -m venv venv
# mac/linux
source venv/bin/activate
# win
source venv/Scripts/activate 
``` 

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
``` 

Выполнить миграции, импортировать ингредиенты и запустить проект

```
python manage.py migrate
python manage.py ingredients ../data/ingredients.csv
python manage.py runserver
``` 

## Запуск проекта в docker контейнере

будет готово ко второму этапу проверки

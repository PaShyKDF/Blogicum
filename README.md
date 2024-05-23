# Cоциальная сеть для публикации личных дневников

Это сайт, на котором пользователь может создать свою страницу и публиковать на ней сообщения («посты»). 
Для каждого поста нужно указать категорию — например «путешествия», «кулинария» или «python-разработка», а также опционально локацию, с которой связан пост, например «Остров отчаянья» или «Караганда».
Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся.
Пользователи смогут заходить на чужие страницы, читать и комментировать чужие посты.
У сайта настроена зона администратора, где можно управлять пользователями, подписками, комментариями и списком локаций.

### Используемые технологии:
![Static Badge](https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow) ![Static Badge](https://img.shields.io/badge/django-darkgreen?style=for-the-badge&logo=django&logoColor=white) ![Static Badge](https://img.shields.io/badge/sqlite-sqlite?style=for-the-badge&logo=sqlite&labelColor=072B8A&color=072B8A)


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:PaShyKDF/Social-network.git
```

```
cd blogicum
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/bin/activate
```

Установить зависимости:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Создать администратора:

```
python manage.py createsuperuser
```

Запустить проект:

```
python manage.py runserver
```

### Функционал:

- Регистрация;
- Создание/удаление/редактирование поста;
- Отложенная публикация поста;
- Комментирование публикации;
- Личный кабинет пользователя с публикациями.
- Зона администратора http://127.0.0.1/admin/
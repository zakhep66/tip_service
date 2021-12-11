# Название нашего проекта

[Ссылка на Figma](https://www.figma.com/file/HcDrVLu3JiS1BFXKwIvRTQ/хахатон?node-id=0%3A1)

# Установка

Для запуска на ПК должны быть установлены:
[Python 3.8](https://www.python.org/downloads/);
[Git](https://git-scm.com/);

Склонируйте репозиторий

```sh
$ git clone https://rn-git.codenrock.com/fintech/cnrprod-team-17897/showcase.git
```

### 1) Настройка Django

В корне проекта создайте виртуальное окружение и активируйте его

```sh
$ python -m venv venv (для Linux: python3 -m venv venv)
$ .\venv\Scripts\activate (для Linux: source ./venv/bin/activate)
```

#### Все последующие действия производить внутри виртуального окружения

Установите все необходимые зависимости для работы Django

```sh
$ pip install -r requirements.txt
```

Установите все необходимые миграции, убедитесь, что был создан файл db.sqlite3

```sh
$ python manage.py makemigrations (для Linux: python3 manage.py makemigrations)
$ python manage.py migrate (для Linux: python3 manage.py migrate)
```

Создайте суперпользователя для работы с админкой

```sh
$ python manage.py createsuperuser (для Linux: python3 manage.py createsuperuser)
```

Запустите проект

```sh
$ python manage.py runserver (для Linux: python3 manage.py runserver)
```

#### Перед загрузкой на github

Если вы устанавливали новые зависимости в Django, то сохраните их в requirenments.txt

```sh
$ pip freeze > requirements.txt
```
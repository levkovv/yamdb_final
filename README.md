# api_yamdb

![example workflow](https://github.com/levkovv/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание проекта
Командный учебный проект написанный в рамках обучения в Яндекс.Практикум.

На основе архитетуры REST API был реализован проект YaMDb, позволяющий пользователям оставлять отзывы на произведения. Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий может быть расширен пользователем с ролью администратор. В каждой категории есть произведения: книги, фильмы или музыка. Произведения можно присваивать жанр из предустановленных. Новые жанры могут создавать админитраторы. Обычные пользователи могут отправлять текстовые отзывы к произведениям и ставить оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усредненная оценка произведения - рейтинг. На одно произведение пользователь может ставить только один отзыв.

Проект был помещен в 3 Docker-контейнера: база данных postgresql, nginx и сам проект.

## Перед зпуском проекта
Необходимо создать файл .env в папке ```/infra```, который будет состоять из
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # название БД
POSTGRES_USER=postgres # пользователь БД
POSTGRES_PASSWORD=postgres # пароль от БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт
```

## Запуск проекта
1. Клонировать репозиторий с github
```
git clone https://github.com/levkovv/infra_sp2
```
2. Перейти в папку с проектом
```
cd infra_sp2
```
3. Перейти в папку infra
```
cd infra
```
4. Собрать docker контейнеры
```
docker-compose up
```
5. Создать и применить миграции в контейнере с приложением web
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
6. Создать суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
7. Собрать все статические файлы
```
docker-compose exec web python manage.py collectstatic --no-input
```
8. Документация со всеми эндпоинтами будет доступна по адресу
```
http://localhost/redoc/
```

## Для регистрации пользователя необходимо
1. Добавить нового пользователя. Отправить POST-запрос с параметрами ```email``` и ```username``` на эндпоинт ```/api/v1/auth/signup```
2. Сервис отправляет письмо с кодом подтверждения (```confirmation_code```) на указанный адрес ```email``` (на данном этапе письмо появится в папке ```sent_emails```)
3. Пользователь отправляет POST-запрос с параметрами ```username``` и ```confirmation_code``` на эндпоинт ```/api/v1/auth/token/```, в ответе на запрос ему приходит JWT-токен

###Развернутое приложение доступно по адресу
http://51.250.19.192


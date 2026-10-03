# Django

## Crear un proyecto

    django-admin startproject _config src

## Comprobar posibles problemas en el proyecto

    python src/manage.py check

## Ejecutar el servidor

    python src/manage.py runserver

## Crear una aplicación

    python src/manage.py startapp core src/core

## Preparar archivos de migración

    python src/manage.py makemigrations

## Aplicar migraciones a la base de datos

    python src/manage.py migrate

## Crear superusuario

    python src/manage.py createsuperuser

## Shell interactivo con las configuraciones de Django

    python src/manage.py shell

## Ejecutar pruebas automáticas

    python src/manage.py test

## Recopilar archivos estáticos

    python src/manage.py collectstatic
# My Movies

+ Ошибка доступа 403 при попытке войти в админку -- После обновления настроек Nginx заработало!

- Много гемора при разработке и настройке
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
Используй gunicorn с --workers, например: --workers 4 --worker-class sync 

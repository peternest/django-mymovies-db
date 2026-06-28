# My Movies

- Заменить в продуктовой версии на GUNICORN
(пока не стал делать из-за неудобства в разработке, использую dev server)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
Используй gunicorn с --workers, например: --workers 4 --worker-class sync 

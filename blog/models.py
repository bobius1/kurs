from django.db import models

# Create your models here.

class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    slug = models.SlugField(verbose_name='url', max_length=100)
    """Возвращает имя категории"""
    def __str__(self):
        return self.name
    """Задаём имя в единственном и множественном числе"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

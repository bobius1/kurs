from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# Create your models here.



class Category(MPTTModel):
    """Модель категорий новостей"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    slug = models.SlugField(verbose_name='url', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание', max_length=1000, default="", blank=True)
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительская категория',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    template = models.CharField(verbose_name="ШАблон", max_length=500, default="blog/post_list.html")
    published = models.BooleanField(verbose_name="Отображать?", default=True)
    paginated = models.PositiveIntegerField(verbose_name="Количество новостей на странице", default=5)
    sort = models.PositiveIntegerField(verbose_name="Порядок", default=0)

    # Возвращает имя категории
    def __str__(self):
        return self.name

    # Задаём имя в единственном и множественном числе
    class Meta:
        verbose_name = "Категория новостей"
        verbose_name_plural = "Категории новостей"


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(verbose_name='Тег', max_length=100)
    slug = models.SlugField(verbose_name='url', max_length=100, unique=True)
    published = models.BooleanField(verbose_name='Отображать?', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    """Модель постов"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(verbose_name='Заголовок', max_length=500)
    subtitle = models.CharField(verbose_name='Под заголовок', max_length=500, blank=True, null=True)
    slug = models.SlugField(verbose_name='url', max_length=500, unique=True)
    mini_text = models.TextField(verbose_name='Краткое содержание', max_length=3000)
    text = models.TextField(verbose_name='Содержание', max_length=10000000)
    created_data = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    edit_date = models.DateTimeField(
        verbose_name='Дата редактирования',
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField(verbose_name='Главная фотография', upload_to="post/", null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Тег", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        null=True
     )
    template = models.CharField(verbose_name="Шаблон", max_length=500, default="blog/post_detail.html")

    published = models.BooleanField(verbose_name="Опубликовать?", default=True)
    viewed = models.PositiveIntegerField(verbose_name="Просмотрено", default=0)
    status = models.BooleanField(verbose_name="Просмотрено", default=False)
    sort = models.PositiveBigIntegerField(verbose_name="Порядок", default=0)

    def get_absolute_url(self):
        return reverse("detail_post", kwargs={'category': self.category.slug, 'slug': self.slug})

    """Возвращает"""
    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Comment(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        # null=True,
        # blank=True
    )
    post = models.ForeignKey(Post, verbose_name="Статья", on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    created_data = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    moderation = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"



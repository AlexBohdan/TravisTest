from django.db import models
import django_filters


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Категории'

    title = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.title


class Event(models.Model):
    class Meta:
        verbose_name_plural = 'События'

    author = models.ForeignKey('account.Account', related_name='author')
    participants = models.ManyToManyField('account.Account', related_name='participants')

    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    short_description = models.TextField('Краткое описание', max_length=200, default='')

    categories = models.ManyToManyField(Category)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True, null=True)
    start_time = models.DateTimeField('Дата начала', null=True)

    len_location = models.CharField('Долгота', max_length=100, null=True)
    wid_location = models.CharField('Широта', max_length=100, null=True)


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['categories']
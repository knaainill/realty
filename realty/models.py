from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class ObjectCategory(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=50,
        unique=True,
    )
    desc = models.CharField(
        verbose_name=_('Описание'),
        max_length=1024,
        null=True,
        blank=True,
    )
    class Meta:
        verbose_name = _('Категория объектов')
        verbose_name_plural = _('Категории объектов')
    def __str__(self):
        return self.name


class Objects(models.Model):
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=250,
    )
    qty_room = models.IntegerField(
        verbose_name=_('Количество комнат'),
        null=True,
        blank=True,
    )
    area = models.FloatField(
        verbose_name=_('Площадь'),
        null=True,
        blank=True,
    )
    floor = models.CharField(
        verbose_name=_('Этажность'),
        max_length=32,
        null=True,
        blank=True,
    )
    residence = models.CharField(
        verbose_name=_('Жилой комплекс'),
        max_length=256,
        null=True,
        blank=True,
    )
    construction_company = models.CharField(
        verbose_name=_('Строительная компания'),
        max_length=256,
        null=True,
        blank=True,
    )
    locate = models.CharField(
        verbose_name=_('Расположение'),
        max_length=256,
        null=True,
        blank=True,
    )
    year = models.IntegerField(
        verbose_name=_('Год постройки'),
        null=True,
        blank=True,
    )
    repair = models.CharField(
        verbose_name=_('Ремонт'),
        max_length=256,
        null=True,
        blank=True,
    )
    document = models.CharField(
        verbose_name=_('Документ'),
        max_length=256,
        null=True,
        blank=True,
    )
    price = models.FloatField(
        verbose_name=_('Цена'),
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Менеджер'),
        on_delete=models.CASCADE,
        related_name='user',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'realty.ObjectCategory',
        verbose_name=_('Категория'),
        on_delete=models.CASCADE,
        related_name='category',
    )
    land_area = models.FloatField(
        verbose_name=_('Площадь участка'),
        null=True,
        blank=True,
    )
    wall_material = models.CharField(
        verbose_name=_('Материал стен'),
        max_length=1024,
        null=True,
        blank=True,
    )
    additional_buildings = models.CharField(
        verbose_name=_('Дополнительные построения'),
        max_length=2048,
        null=True,
        blank=True,
    )
    communications = models.CharField(
        verbose_name=_('Коммуникации'),
        max_length=512,
        null=True,
        blank=True,
    )
    is_separately = models.BooleanField(
        verbose_name=_('Находится отдельно'),
        null=True,
        blank=True,
    )
    appointment = models.CharField(
        verbose_name=_('Назначение'),
        max_length=512,
        null=True,
        blank=True,
    )
    lenght_width = models.CharField(
        verbose_name=_('Ширина и длина'),
        max_length=64,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = _('Объект')
        verbose_name_plural = _('Объекты')

    def __str__(self):
        return self.title

class Images(models.Model):
    object = models.ForeignKey(
        'realty.Objects',
        verbose_name=_('Объект'),
        on_delete=models.CASCADE,
        related_name='object',
    )
    pic = models.ImageField(
        upload_to='pics',
        verbose_name=_('Изображение'),
        blank=True
    )

    class Meta:
        verbose_name = _('Фото')
        verbose_name_plural = _('Фото')

    def __str__(self):
        return self.object.title
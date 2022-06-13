from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe


class Team(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Наименование команды')
    is_active = models.BooleanField(default=True, verbose_name='Актуальность')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Player(models.Model):
    last_name = models.CharField(max_length=200, db_index=True, verbose_name='Фамилия игрока')
    first_name = models.CharField(max_length=200, verbose_name='Имя игрока')
    middle_name = models.CharField(max_length=200, verbose_name='Отчество игрока')
    photo = models.ImageField(upload_to='player_photos/', blank=True, verbose_name='Фотография игрока')
    player_role = models.CharField(max_length=200, verbose_name='Амплуа игрока')
    progress_points = models.DecimalField(max_digits=8, decimal_places=1, verbose_name='Очки игрока')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players', verbose_name='Команда')
    is_active = models.BooleanField(default=True, verbose_name='Актуальность')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')

    class Meta:
        unique_together = ('last_name', 'team',)
        ordering = ['-progress_points', 'last_name']
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def full_name(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    full_name.short_description = 'ФИО игрока'

    def photo_img(self):
        if self.photo:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="50"/></a>'.format(self.photo.url))
        else:
            return 'Фотографии нет'

    photo_img.short_description = 'Фотография'
    photo_img.allow_tags = True

    def get_absolute_url(self):
        return reverse('gamers:employee_detail', args=[self.id])


class Fraction(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование фракции')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='fractions',
                             verbose_name='Лидирующая команда')
    leader = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fractions',
                               verbose_name='Руководитель фракции')
    players_list = models.ManyToManyField(Player, default=None, blank=True, related_name='players_set',
                                          verbose_name='Список игроков во фракции')
    is_active = models.BooleanField(default=True, verbose_name='Актуальность')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракции'

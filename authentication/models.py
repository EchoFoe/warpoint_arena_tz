from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('У пользователя должен быть уникальный никнейм (username)')

        if email is None:
            raise TypeError('У пользователя должна быть почта (email)')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if username is None:
            raise TypeError('У пользователя должен быть уникальный никнейм (username)')

        if email is None:
            raise TypeError('У пользователя должна быть почта (email)')

        if password is None:
            raise TypeError('У супер пользователя должен быть пароль (password)')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, db_index=True, unique=True, verbose_name='Никнейм')
    email = models.EmailField(max_length=40, db_index=True, unique=True, verbose_name='Почта')
    is_active = models.BooleanField(default=True, verbose_name='Актуальность пользователя')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_superuser = models.BooleanField(default=False, verbose_name='Статус суперпользователя')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания записи')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ('-created_at', 'username')
        index_together = (('id', 'username'),)
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'

    def __str__(self):
        return '%s: %s' % (self.email, self.username)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

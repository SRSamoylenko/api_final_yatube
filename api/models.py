from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models

from api.utils import wrap_text

User = get_user_model()


class Group(models.Model):
    """Model for a group object.

    Properties:
    title -- a name of a group.
    description -- group info.
    """
    title = models.CharField(
        verbose_name='Имя группы',
        max_length=200,
        help_text='Задайте имя вашей группы.',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст публикации',
        help_text=(
            'Введите текст публикации. '
            'Текст не должен быть пустым или состоять только из пробелов.'
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        help_text=('Выберите группу, в которой пост будет опубликован '
                   'или оставьте поле пустым.'),
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        text = wrap_text(self.text)
        return (
            f'Автор: {self.author}\n'
            f'Дата публикации: {self.pub_date.strftime("%d.%m.%Y")}\n'
            f'Текст:\n'
            f'{text}\n'
            f'\n'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Запись',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст комментария.',
        help_text='Добавьте комментарий.',
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        text = wrap_text(self.text)
        return (
            f'Автор: {self.author}\n'
            f'Дата публикации: {self.created.strftime("%d.%m.%Y")}\n'
            f'Пост: {self.post.id}\n'
            f'Текст:\n'
            f'{text}\n'
            f'\n'
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'following')

    def __str__(self):
        return (f'Автор: {self.following}\n'
                f'Подписчик: {self.user}\n')

    def save(self, *args, **kwargs) -> Optional:
        if self.following != self.user:
            return super().save(*args, **kwargs)
        return None

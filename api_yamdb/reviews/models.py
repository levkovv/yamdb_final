from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title_id',)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'date published',
        db_index=True,
        auto_now_add=True,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='title_author'
            ),
        )
        ordering = ('pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True
    )
    pub_date = models.DateTimeField(
        'date published',
        db_index=True,
        auto_now_add=True,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )

    class Meta:
        ordering = ('pub_date',)

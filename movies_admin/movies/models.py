import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    def __str__(self):
        return self.name

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:

        db_table = "content\".\"genre"
        verbose_name = _('genres')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):

    def __str__(self):
        return self.full_name
    
    full_name = models.TextField(_('full_name'))

    class Meta:

        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(UUIDMixin, TimeStampedMixin):

    def __str__(self):
        return self.title

    class FilmworkType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(
        _('rating'), 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        _('type'),
        choices=FilmworkType.choices, 
        default=FilmworkType.MOVIE,
        max_length=255,
    )
    genres = models.ManyToManyField(Genre, verbose_name=_('genres'), through='GenreFilmwork')
    roles = models.ManyToManyField(Person, verbose_name=_('roles'), through='PersonFilmwork')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:

        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')



class GenreFilmwork(UUIDMixin):

    film_work = models.ForeignKey('Filmwork', verbose_name=_('film_work'), on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre_filmwork')
        verbose_name_plural = _('genre_filmworks')


class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey('Filmwork', verbose_name=_('film_work'), on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"


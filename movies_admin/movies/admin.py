from django.contrib import admin
from .models import Filmwork
from .models import Genre
from .models import GenreFilmwork
from .models import Person
from .models import PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    search_fields = ('name', 'description', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, )

    list_display = ('title', 'type', 'creation_date', 'rating', )
    list_filter = ('type', 'genres', )
    search_fields = ('title', 'description', 'id', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

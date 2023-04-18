from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    search_fields = ('name', 'description', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres',)
    list_filter = ('type', 'creation_date',)
    search_fields = ('title', 'description', 'id',)
    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('filmwork_genre')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    
    list_display = ('full_name', 'gender', 'created',)
    list_filter = ('gender', 'created',)
    search_fields = ('full_name', 'id',)
from dt_schema import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


DEFAULT_EXTRACT_CHUNK_SIZE = 50
DEFAULT_LOAD_CHUNK_SIZE = 50

MAP_DATA_FIELDS = (
    ('created_at', 'created'),
    ('updated_at', 'modified'),
)

TABLES = (
    ('film_work', FilmWork,),
    ('genre', Genre,),
    ('genre_film_work', GenreFilmWork,),
    ('person', Person,),
    ('person_film_work', PersonFilmWork,),
)
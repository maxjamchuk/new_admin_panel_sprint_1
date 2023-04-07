import uuid
from dataclasses import asdict, dataclass, field, fields
from datetime import date, datetime


class KeyValueMixin():

    @classmethod
    def keys(cls):
        return [field.name for field in fields(cls)]

    def values(self):
        return asdict(self).values()


@dataclass
class CreatedModifiedMixin:
    created: datetime
    modified: datetime

    def __post_init__(self):
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created + '00', '%Y-%m-%d %H:%M:%S.%f%z')
        if isinstance(self.modified, str):
            self.modified = datetime.strptime(self.modified + '00', '%Y-%m-%d %H:%M:%S.%f%z')


@dataclass
class CreatedMixin:
    created: datetime

    def __post_init__(self):
        if isinstance(self.created, str):
            self.created = datetime.strptime(self.created + '00', '%Y-%m-%d %H:%M:%S.%f%z')


@dataclass
class UUIDMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork(CreatedModifiedMixin, KeyValueMixin):
    title: str
    creation_date: date
    type: str
    file_path: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    description: str = field(default=None)
    rating: float = field(default=0.0)
    certificate: str = field(default=None)

    def __post_init__(self):
        super().__post_init__()
        self.rating = 0.0 if self.rating is None else self.rating


@dataclass
class Genre(CreatedModifiedMixin, KeyValueMixin):
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    description: str = field(default=None)


@dataclass
class Person(CreatedModifiedMixin, KeyValueMixin):
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    gender: str = field(default=None)


@dataclass
class GenreFilmWork(CreatedMixin, KeyValueMixin):
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork(CreatedMixin, KeyValueMixin):
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
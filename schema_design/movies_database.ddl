-- ************************************** schema content
CREATE SCHEMA IF NOT EXISTS content;
-- ************************************** content.person
CREATE TABLE IF NOT EXISTS content.person (
    id uuid NOT NULL,
    full_name text NOT NULL,
    created timestamp with time zone NULL,
    modified timestamp with time zone NULL,
    CONSTRAINT PK_person PRIMARY KEY (id)
);
-- ************************************** content.genre
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid NOT NULL,
    name text NOT NULL,
    description text NULL,
    created timestamp with time zone NULL,
    modified timestamp with time zone NULL,
    CONSTRAINT PK_genre PRIMARY KEY (id)
);
-- ************************************** content.film_work
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid NOT NULL,
    title text NOT NULL,
    description text NULL,
    creation_date date NULL,
    rating float NULL,
    type text NOT NULL,
    created timestamp with time zone NULL,
    modified timestamp with time zone NULL,
    CONSTRAINT PK_film_work PRIMARY KEY (id)
);
-- ************************************** content.person_film_work
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role text NOT NULL,
    created timestamp with time zone NULL,
    CONSTRAINT PK_person_film_work PRIMARY KEY (id),
    CONSTRAINT FK_person_film_work_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    CONSTRAINT FK_person_film_work_person_id FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE
);
-- ************************************** content.genre_film_work
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone NULL,
    CONSTRAINT PK_genre_film_work PRIMARY KEY (id),
    CONSTRAINT FK_genre_film_work_film_work_id FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    CONSTRAINT FK_genre_film_work_genre_id FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE
);
-- ************************************** indexes
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON content.genre(name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work(film_work_id, person_id, role);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work(film_work_id, genre_id);
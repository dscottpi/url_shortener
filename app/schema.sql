DROP TABLE IF EXISTS url;

CREATE TABLE url (
    id integer primary key,
    short_url text not null,
    long_url text not null
)
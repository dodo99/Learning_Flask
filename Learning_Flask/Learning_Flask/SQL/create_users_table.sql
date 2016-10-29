CREATE TABLE users (
    uid serial PRIMARY KEY,
    firstname VARCHAR(100) not null,
    lastname VARCHAR(100) not null,
    email VARCHAR(120) not null unique,
    pwdhash VARCHAR(100) not null
);    
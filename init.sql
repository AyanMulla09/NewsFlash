\c news

CREATE TABLE asianews (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    image VARCHAR(255),
    link VARCHAR(255),
    date DATE NOT NULL
);
CREATE TABLE nytimes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    image VARCHAR(255),
    link VARCHAR(255),
    date DATE NOT NULL
);
CREATE TABLE guardian (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    image VARCHAR(255),
    link VARCHAR(255),
    date DATE NOT NULL
);
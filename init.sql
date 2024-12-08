\c news

CREATE TABLE asiantimes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    image VARCHAR(255),
    link VARCHAR(255),
    date DATE NOT NULL
);

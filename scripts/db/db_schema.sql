CREATE DATABASE bank_reviews;

CREATE TABLE banks (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(128) NOT NULL,
    app_id VARCHAR2(64) NOT NULL,
    current_rating NUMBER(3,1)
);

CREATE TABLE reviews (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    bank_id NUMBER REFERENCES banks(id),
    review CLOB,
    rating NUMBER,
    review_date DATE,
    source VARCHAR2(32),
    sentiment_label VARCHAR2(16),
    sentiment_score FLOAT,
    theme VARCHAR2(200)
);
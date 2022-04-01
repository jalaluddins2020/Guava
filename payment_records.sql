drop database if exists payment_recordsdb;

create database payment_recordsdb;
use payment_recordsdb;

CREATE TABLE IF NOT EXISTS payments (
    payment_id  VARCHAR(128) NOT NULL,
    listing_id   INT  NOT NULL,
    customer_id  INT  NOT NULL,
    price   FLOAT(10,2)   NOT NULL,
    date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY(listing_id)
);

INSERT INTO payments (payment_id, listing_id, customer_id, price, date_time) VALUES ("PAYID-MI5PAJI63V0799180830831E", 1, 1, 15.00, "2022-03-17 17:54:32");

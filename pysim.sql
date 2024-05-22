CREATE DATABASE pylife
USE pylife

CREATE TABLE pysims (
    sim_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    occupation VARCHAR(30),
    gender INT NOT NULL,
    partner INT NOT NULL,
    married TINYINT
)

CREATE TABLE date (
    day INT,
    month INT,
    year INT
)

INSERT INTO date (day, month, year)
VALUES (1 ,1 , 1)

CREATE TABLE friendship (
    pysim_id_1 INT NOT NULL,
    pysim_id_2 INT NOT NULL,
    friendkey VARCHAR(45) NOT NULL PRIMARY KEY
)
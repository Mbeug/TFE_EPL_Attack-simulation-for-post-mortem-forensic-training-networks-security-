CREATE USER 'bdduser'@'10.0.0.14' IDENTIFIED BY 'uclouvain';
GRANT ALL PRIVILEGES ON *.* TO 'bdduser'@'10.0.0.14';
FLUSH PRIVILEGES;
CREATE DATABASE testDB;
USE testDB;
CREATE TABLE editorial (id INT, name VARCHAR(20), email VARCHAR(20));
INSERT INTO editorial (id,name,email) VALUES(01,"Olivia","olivia@company.com");
INSERT INTO editorial (id,name,email) VALUES(02,"Bob","bob@company.com");
INSERT INTO editorial (id,name,email) VALUES(03,"Frank","frank@company.com");
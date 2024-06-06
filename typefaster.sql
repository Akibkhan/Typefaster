CREATE DATABASE TYPEFASTER;
USE TYPEFASTER;
show tables;
CREATE TABLE sentences(ID INT PRIMARY KEY auto_increment,Text VARCHAR(255));
INSERT INTO sentences VALUES(1,"Seeing photos of ancestors a century past"),(2,"Twirling the cord between my fingers"),(3,"The loud voice is famous to silence");
DROP TABLE leaderboard;
CREATE TABLE LEADERBOARD(ID INT primary KEY auto_increment,Name VARCHAR(50),Time INT,WPM INT)
CREATE DATABASE tournament;

CREATE TABLE Tournament(
	id SERIAL PRIMARY KEY,
	name TEXT,
	matches NUMERIC,
	wins NUMERIC
);

CREATE VIEW Standing AS 
SELECT id, name, wins, matches 
FROM Tournament 
ORDER BY wins DESC;
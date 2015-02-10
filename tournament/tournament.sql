-- Table definitions for the tournament project.
--
-- Put your SQL 'CREATE table' statements in this file; also 'CREATE view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE Table Tournament(
	id SERIAL,
	name TEXT,
	matches NUMERIC,
	wins NUMERIC
);

CREATE VIEW Standing AS 
SELECT id, name, wins, matches 
FROM Tournament 
ORDER BY wins DESC;
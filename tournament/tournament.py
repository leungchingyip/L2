#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():

    db = connect()
    c = db.cursor()
    c.execute("UPDATE Tournament SET matches=0, wins=0;")
    db.commit()
    db.close()
    """Remove all the match records FROM the database."""


def deletePlayers():

    db = connect()
    c = db.cursor()
    c.execute("TRUNCATE Tournament RESTART IDENTITY;")
    db.commit()
    db.close()
    """Remove all the player records FROM the database."""


def countPlayers():

    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(name) FROM Tournament;")
    countplayers = c.fetchall()
    return int(countplayers[0][0])
    db.close()
    """Returns the number of players currently registered."""


def registerPlayer(name):

    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Tournament (name, matches, wins) values((%s), 0, 0);", (name,))
    db.commit()
    db.close()
    """Adds a player to the Tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():

    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM Standing")
    return c.fetchall()
    db.close()

    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):

    db = connect()
    c = db.cursor()
    c.execute('''
        UPDATE Tournament SET wins=(CASE WHEN id=%d THEN wins+1
                                         WHEN id=%d THEN wins+0 END),
                              matches=matches+1
                              WHERE id IN (%d, %d);
    '''%(winner,loser, winner, loser,))
    db.commit()
    db.close()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    pairlist=[]
    db = connect()
    c = db.cursor()

    totalplayers= countPlayers()
    for i in range (1, totalplayers/2+1):
        offset_number = (i-1)*2
        c.execute("SELECT id, name FROM standing LIMIT 2 OFFSET %d" %(offset_number,))

        p = c.fetchall()
        p = p[0] +p[1]
        pairlist.insert(i, p)
    return pairlist
    db.close()

    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """



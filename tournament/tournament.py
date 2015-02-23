#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records FROM the database."""
    db = connect()
    c = db.cursor()
    c.execute("UPDATE Tournament SET matches=0, wins=0;")
    db.commit()
    db.close()
    


def deletePlayers():
    """Remove all the player records FROM the database."""
    db = connect()
    c = db.cursor()
    c.execute("TRUNCATE Tournament RESTART IDENTITY;")
    db.commit()
    db.close()
    


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(name) FROM Tournament;")
    countplayers = c.fetchall()
    return int(countplayers[0][0])
    db.close()
    


def registerPlayer(name):
    """Adds a player to the Tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Tournament (name, matches, wins) values((%s), 0, 0);", (name,))
    db.commit()
    db.close()



def playerStandings():
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
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM Standing")
    standing=c.fetchall()
    db.close()
    return standing



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('''
        UPDATE Tournament SET wins=(CASE WHEN id=%d THEN wins+1
                                         WHEN id=%d THEN wins+0 END),
                              matches=matches+1
                              WHERE id IN (%d, %d);
    '''%(winner, loser, winner, loser,))
    db.commit()
    db.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairlist=[]
    db = connect()
    c = db.cursor()
    c.execute("SELECT id, name FROM standing;")
    standing_list=c.fetchall()
    totalplayers= countPlayers()
    db.close()

    for i in range (0, totalplayers/2):
        p = standing_list[i*2] + standing_list[i*2+1] 
        pairlist.insert(i, p)
    return pairlist






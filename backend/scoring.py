import sqlite3
import math

dbPath = "WorldWanderer-main/databases/leaderboard.db"

# Store a single round result
def logRoundResult(roundNumber, distanceMeters, timeTaken, guessLat, guessLon, actualLat, actualLon):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO "tempdata-SingleMatchLogs"
        (roundNumber, distanceMeters, timeTaken, guessLat, guessLon, actualLat, actualLon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (roundNumber, distanceMeters, timeTaken, guessLat, guessLon, actualLat, actualLon))
    conn.commit()
    conn.close()

def calculateFinalScore(): # Score (per round) = 5000 * e ^ (-( (km / D) + (time / T) ))
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("SELECT distanceMeters, timeTaken FROM 'tempdata-SingleMatchLogs'")
    rows = cur.fetchall()
    conn.close()

    # constants determine how score is handled
    D = 1500.0 # distance decay (in km) - controls how harsh penalty distance is
    T = 30.0 # time decay (seconds) - controls how harsh time penalty is
    maxScore = 5000 # score user starts at.

    totalScore = 0

    for distanceMeters, timeSeconds in rows:
        km = distanceMeters / 1000.0

        decay = math.exp(-(km / D + timeSeconds / T))
        roundScore = maxScore * decay

        totalScore += roundScore

    return int(totalScore)


# Insert final score into leaderboard
def logFinalScore(playerName, finalScore, roundsPlayed, timeLimit):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    # Insert user
    cur.execute("""
        INSERT INTO databaseUsers (userName)
        VALUES (?)
    """, (playerName,))
    userID = cur.lastrowid

    # Use userID as matchID for now
    matchID = userID

    # Insert match result
    cur.execute("""
        INSERT INTO "leaderboard-wholeMatch"
        (userID, matchID, totalScore, roundsPlayed, timeLimit)
        VALUES (?, ?, ?, ?, ?)
    """, (userID, matchID, finalScore, roundsPlayed, timeLimit))

    conn.commit()
    conn.close()

# Clear previous match data
def clearSingleMatchLogsData():
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("DELETE FROM 'tempdata-SingleMatchLogs'")
    conn.commit()
    conn.close()
    
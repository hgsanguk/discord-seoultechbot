import sqlite3

discord_server_db = sqlite3.connect("server_settings.db", isolation_level=None)
cur = discord_server_db.cursor()


def initial():
    cur.execute("CREATE TABLE IF NOT EXISTS Server (server_id integer PRIMARY KEY, channel_id integer, notify_hour integer)")


def set_notification_channel(server, channel, notify_hour):
    try:
        cur.execute('INSERT INTO Server VALUES(?, ?, ?)', (server, channel, notify_hour))
    except sqlite3.IntegrityError:
        cur.execute('UPDATE Server SET channel_id=?, notify_hour=? WHERE server_id=?', (channel, notify_hour, server))


def get_channel(hour):
    cur.execute('SELECT channel_id FROM Server WHERE notify_hour=?', (hour,))
    return cur.fetchall()


def get_channel_all():
    cur.execute('SELECT channel_id FROM Server')
    return cur.fetchall()

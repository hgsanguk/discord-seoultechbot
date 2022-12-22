import sqlite3

discord_server_db = sqlite3.connect("server_settings.db", isolation_level=None)
cur = discord_server_db.cursor()


def initial():
    cur.execute("CREATE TABLE IF NOT EXISTS Server"
                "(server_id integer PRIMARY KEY, channel_id integer, notify_hour integer, server_option integer)")


def set_notification_channel(server, channel, notify_hour):
    try:
        cur.execute('INSERT INTO Server VALUES(?, ?, ?, ?)', (server, channel, notify_hour, 0))
    except sqlite3.IntegrityError:
        cur.execute('UPDATE Server SET channel_id=?, notify_hour=? WHERE server_id=?', (channel, notify_hour, server))


def set_dormitory_notification(server):
    cur.execute('SELECT channel_id, server_option FROM Server WHERE server_id=?', (server,))
    be_notified = cur.fetchall()
    if be_notified[0][1] == 0:
        cur.execute('UPDATE Server SET server_option=? WHERE server_id=?', (1, server))
    else:
        cur.execute('UPDATE Server SET server_option=? WHERE server_id=?', (0, server))
    return be_notified[0]


def get_channel(hour):
    cur.execute('SELECT channel_id FROM Server WHERE notify_hour=?', (hour,))
    return cur.fetchall()


def get_channel_dormitory():
    cur.execute('SELECT channel_id FROM Server WHERE server_option=?', (1,))
    return cur.fetchall()


def get_channel_all():
    cur.execute('SELECT channel_id FROM Server')
    return cur.fetchall()

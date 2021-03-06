import MySQLdb
import MySQLdb.cursors
# Naming rule:
# table : User, Table, User_action
# column : user, table, user_action
import sys
sys.path.append("..")
import config.config as cfg

# Connect
print "Connecting to the database..."
conn = MySQLdb.connect ( host = cfg.HOST, user = cfg.USER,\
                        passwd = cfg.PASSWORD,\
                         charset='utf8')
print "Connected."
# Get cursor
cur = conn.cursor(MySQLdb.cursors.DictCursor)

# Create database
#cur.execute('DROP DATABASE IF EXISTS tianchi_music')

cur.execute('CREATE DATABASE IF NOT EXISTS p2_tianchi_music')
conn.select_db(cfg.DBNAME)

print "Database tianchi_music is created and selected."

# Create user actions table
cur.execute('create table if not exists User_actions(\
`id` int not null auto_increment primary key,\
`user_id` char(32) not null,\
`song_id` char(32) not null,\
`gmt_create` int not null,\
`action_type` int not null,\
`ds` date not null )')

print "Table User_actions created."

cur.execute('create table if not exists Songs(\
`id` int not null auto_increment primary key,\
`song_id` char(32) not null,\
`artist_id` char(32) not null,\
`publish_time` date not null,\
`song_init_plays` int not null,\
`language` int not null,\
`gender` int not null)')

print "Table Songs created."

print "Openning files..."

count = cur.execute("SELECT * FROM User_actions limit 5")
if count == 0:
    user_actions_lines = open(cfg.USER_ACTIONS, 'r').readlines()
    print "Writing user actions..."
    for line in user_actions_lines:
        data = line.split(',')
        data[4] = data[4][0:4] + "-" + data[4][4:6] + "-" + data[4][6:8]
        cur.execute("insert into User_actions(user_id, song_id, gmt_create, action_type, ds) values (%s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4]))
        conn.commit()
    print "User actions data added."

count = cur.execute("SELECT * FROM Songs LIMIT 5")
if count == 0:
    songs_lines = open(cfg.SONGS, 'r').readlines()
    print "Writing songs..."
    for line in songs_lines:
        data = line.split(',')
        data[2] = data[2][0:4] + "-" + data[2][4:6] + "-" + data[2][6:8]
        cur.execute("insert into Songs(song_id, artist_id, publish_time, song_init_plays, language, gender) values (%s, %s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4], data[5]))
        conn.commit()
    print "Songs data added."

print "Start creating index..."
cur.execute("create index user_id_idx on User_actions(user_id);")
cur.execute("create index user_actions_song_id_idx on User_actions(song_id);")
cur.execute("create index songs_song_id_idx on Songs(song_id);")
cur.execute("create index songs_artist_id_idx on Songs(artist_id);")
conn.commit()

cur.close()
conn.close()
print "Finish"

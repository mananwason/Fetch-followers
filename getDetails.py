import MySQLdb
from twython import Twython
import time
APP_KEY = 'RRwz1GdeYEwblimUZvotuaVLT'
APP_SECRET = 'Z6Zv3OixKkwcLbDhMZnBRiHnWM0glaL0gFdKpv4Jjl8OVUY4mY'

# APP_KEY = 'gjZdaiDckLlyGLAYonCeJEsLo'
# APP_SECRET = 'dfzW7bK10KTOsMyJVxeraqP6wJ3ZcSxiREDBtJvotmN9g0WGOf'
USERNAME = "dtptraffic"
auth = {
    'pxKUh8LSKq6jZShXABl2gEZTI' : '9kKaSyj08Aelzm4SpBIAElfQkSKcbkpvH0oSVxa80lvktB2FjV',
    'IpP9LFdZTtzjW4Vv7DxZZwwni' : 'os0mEGwLFkTei9ZFCw6d9MaaqiUYH9E8uoYuE8hPmUFYvRGJwy',
    # 'RRwz1GdeYEwblimUZvotuaVLT' : 'Z6Zv3OixKkwcLbDhMZnBRiHnWM0glaL0gFdKpv4Jjl8OVUY4mY',
    'gjZdaiDckLlyGLAYonCeJEsLo' : 'dfzW7bK10KTOsMyJVxeraqP6wJ3ZcSxiREDBtJvotmN9g0WGOf',
        'A3N3k7SzVXiW56SPydOt8X8T8': 'LrXib3LqlCFARuzBNBADUQthe34HS6bGYMweUOfsCTvO9nkDP4',
        'iaekqPFNSRm1CuDYVjXiFcmNR': '7sAtZfc9o4N6DT6mMuUvXQuHD8iEFY2uKr5HtaYGBdvUBoOtG0',
        '1f7V1xrCBYMMlBTOacxfwg9XX': '9LrbdCwD5SoquJTaMhdxgN67Et8mFyTbP3ILgSLZXtj02nTkhr',
        'feSXOSUpOWUAtrEmRwU0CjliH': 'rxwu5cN3jOGJSoQVGnrM9XH6tkqZVhGm3OBK8QDNlaoiumDIZX'}
dict2 = auth.copy()

twitter = Twython(APP_KEY,APP_SECRET)

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="123123abc",  # your password
                     db="test1")  # name of the data base
cur = db.cursor()


calls = 0
def get_user_creation():

    details = getNewTwitterInstance().show_user(screen_name=USERNAME)
    global calls
    calls += 1
    print "1 calls", calls

    created= str(details['created_at'])
    cur.execute("DELETE FROM user")

    cur.execute('CREATE TABLE IF NOT EXISTS `user` (id INT NOT NULL AUTO_INCREMENT,name CHAR(100) NOT NULL, created_on VARCHAR(100) NOT NULL, PRIMARY KEY ( id ))')
    add_user = "INSERT INTO user(id,name, created_on) VALUES (null, %s, %s)"

    cur.execute(add_user, [USERNAME, created])
    db.commit()

# def get_creation_date(name):
#     details = twitter.show_user(screen_name=name)
#     print (details['created_at'] + name)# Account creation date
def save_follower(comma_separated_string, samplefollower):
    output = getNewTwitterInstance().lookup_user(user_id=comma_separated_string)
    global calls
    calls += 1
    print "2 calls", calls
    username_list = []
    print "LEN : ",len(samplefollower)
    created_at = []
    for user in output:
        username_list.append(user['screen_name'])
        created_at.append(user['created_at'])

    # insert into db
    for i in range(len(samplefollower)):
        add_user = "INSERT INTO followers(id, follower_id, name,created_at) VALUES (null, %s, %s, %s)"
        cur.execute(add_user, [samplefollower[i], username_list[i], created_at[i]])
        db.commit()


def get_name_by_id():
    #Delete all records
    cur.execute("DELETE FROM followers")
    cur.execute('CREATE TABLE IF NOT EXISTS `followers` (id INT NOT NULL AUTO_INCREMENT,follower_id VARCHAR(100),name CHAR(100) NOT NULL, created_on VARCHAR(100) NOT NULL, PRIMARY KEY ( id ))')
    global calls
    #get followers list
    next_cursor = -1
    followers1 = []
    while (next_cursor):
        # Getting the user's followers (should all be 1 line)
        get_followers = getNewTwitterInstance().get_followers_list(screen_name=USERNAME, count=200, cursor=next_cursor)
        calls += 1

        # For each user returned from our get_followers
        for follower in get_followers["users"]:
            # Add their screen name to our followers list
            followers1.append(follower['id'])
            # print len(followers)
            next_cursor = get_followers["next_cursor"]
        print calls

        # followers = twitter.get_followers_ids(screen_name=USERNAME, cursor=-1)
    # calls += 1
    # print len(followers.cursor)
    samplefollower = []

    for count, follower_id in enumerate(followers1):
        samplefollower.append(str(follower_id))
        if count % 100 == 0:
            comma_separated_string = ",".join(samplefollower)
            save_follower(comma_separated_string, samplefollower)
            samplefollower = []
        elif (len(followers1) - count) == 1:
            comma_separated_string = ",".join(samplefollower)
            save_follower(comma_separated_string, samplefollower)
def getNewTwitterInstance():
    global dict2
    global twitter
    if(calls % 28 == 0 and calls != 0):
        print "abc"
        if not bool(dict2):
            print "More api keys required"
            print "Sleeping for 15 minutes"
            for i in xrange(15, 0, -1):
                time.sleep(60)
                print "Counter minutes", i
            dict2 = auth.copy()
        key, secret = dict2.popitem()
        print key, " : ", secret
        twitter = Twython(key, secret)

    return twitter


get_user_creation()
get_name_by_id()
print calls

db.close()






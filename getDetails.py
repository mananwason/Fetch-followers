import MySQLdb
from twython import Twython
import time

# APP_KEY = 'RRwz1GdeYEwblimUZvotuaVLT'
# APP_SECRET = 'Z6Zv3OixKkwcLbDhMZnBRiHnWM0glaL0gFdKpv4Jjl8OVUY4mY'

APP_KEY = 'Gx0S1HzeYEbqciaOMnRQzxXlg'
APP_SECRET = 'BOExeYIb5jCcgI7hLMsvdhbpvYH3OuJ9MhYod24ot1AJzjFl4Q'
USERNAME = "misskaul"
auth = {
    'pxKUh8LSKq6jZShXABl2gEZTI': '9kKaSyj08Aelzm4SpBIAElfQkSKcbkpvH0oSVxa80lvktB2FjV',
    'IpP9LFdZTtzjW4Vv7DxZZwwni': 'os0mEGwLFkTei9ZFCw6d9MaaqiUYH9E8uoYuE8hPmUFYvRGJwy',
    'RRwz1GdeYEwblimUZvotuaVLT' : 'Z6Zv3OixKkwcLbDhMZnBRiHnWM0glaL0gFdKpv4Jjl8OVUY4mY',
    '3FepN482YqmrMFE4StfhbqJmu': 'wvf6mlRwZ6nZiMy8SAPokKW0SNcus2UhTF8jDX1hrEWeyR94Zp',
    'LW3M2aFYerBX1oayQUSRK1WcX': '2gSXUv17k2nD3cD2ldoPdh6f03V1wGGPoShD9t9xlSVpR5tndt',
    'rrhawfGI92JKyPOS562BcnqW3': 'zR8ZZP6FQgdxULRjapRaYbo2PaFO0750ohKwo3KTotS5mdXnCj',
    'fREAhpYreopAIUmWMsLO12kOj': 'Y8VAidl0aeTga1jd3Gt8w0GYMUO9RYjbGYQaqFHmwcGeiDvfyr',
    'QjKZfGHlCyhqaOiNXQmg7Kqtq': 'rpw72aMOnZ3amQj4xYF0mPUSRM5hCN2nfHJdgXe9RiYnNu56Pg',
    'Gx0S1HzeYEbqciaOMnRQzxXlg': 'BOExeYIb5jCcgI7hLMsvdhbpvYH3OuJ9MhYod24ot1AJzjFl4Q',
    'gjZdaiDckLlyGLAYonCeJEsLo': 'dfzW7bK10KTOsMyJVxeraqP6wJ3ZcSxiREDBtJvotmN9g0WGOf',
    'A3N3k7SzVXiW56SPydOt8X8T8': 'LrXib3LqlCFARuzBNBADUQthe34HS6bGYMweUOfsCTvO9nkDP4',
    'iaekqPFNSRm1CuDYVjXiFcmNR': '7sAtZfc9o4N6DT6mMuUvXQuHD8iEFY2uKr5HtaYGBdvUBoOtG0',
    '1f7V1xrCBYMMlBTOacxfwg9XX': '9LrbdCwD5SoquJTaMhdxgN67Et8mFyTbP3ILgSLZXtj02nTkhr',
    'feSXOSUpOWUAtrEmRwU0CjliH': 'rxwu5cN3jOGJSoQVGnrM9XH6tkqZVhGm3OBK8QDNlaoiumDIZX'
}
dict2 = auth.copy()

twitter = Twython(APP_KEY, APP_SECRET)

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="123123abc",  # your password
                     db="test1")  # name of the data base
cur = db.cursor()

calls = 0
counter = 0


def get_user_creation():
    details = getNewTwitterInstance().show_user(screen_name=USERNAME)
    global calls
    calls += 1
    print "1 calls", calls

    created = str(details['created_at'])
    cur.execute("DELETE from followers")

    cur.execute("DELETE FROM user")

    cur.execute(
        'CREATE TABLE IF NOT EXISTS `user` (id INT NOT NULL AUTO_INCREMENT,name CHAR(100) NOT NULL, created_on VARCHAR(100) NOT NULL, PRIMARY KEY ( id ))')
    add_user = "INSERT INTO user(id,name, created_on) VALUES (null, %s, %s)"

    cur.execute(add_user, [USERNAME, created])
    db.commit()


def save_follower(comma_separated_string, samplefollower):
    counter += 1
    output = getNewTwitterInstance().lookup_user(user_id=comma_separated_string)
    global calls
    global counter
    calls += 1
    # print "2 calls", calls
    username_list = []
    # print "LEN : ", len(samplefollower)
    created_at = []

    for user in output:
        username_list.append(user['screen_name'])
        created_at.append(user['created_at'])

    # insert into db
    sql = "SELECT user.id FROM user WHERE name = '%s'" % USERNAME
    # print sql
    cur.execute(sql)
    row = cur.fetchone()
    user_id = row[0]
    print "Counter :", counter
    print "username : ", len(username_list), "Follower id : ", len(samplefollower), "created at : ", len(created_at)
    for i in range(len(username_list)):
        print "I :", i
        add_user = "INSERT INTO followers(id, follower_id, name,created_at, user_id) VALUES (null, %s, %s, %s, %s)"
        cur.execute(add_user, [samplefollower[i], username_list[i], created_at[i], user_id])
        db.commit()


def get_name_by_id():
    # Delete all records
    # cur.execute("DELETE FROM followers")
    cur.execute(
        'CREATE TABLE IF NOT EXISTS `followers` (id INT NOT NULL AUTO_INCREMENT,follower_id VARCHAR(100),name CHAR(100) NOT NULL, created_on VARCHAR(100) NOT NULL, user_id  INT(11) DEFAULT NULL, PRIMARY KEY ( id, name))')
    global calls
    # get followers list
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
    if calls % 30 == 0 and calls != 0:
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

import pymysql.cursors
from collections import OrderedDict
from pymysql.cursors import DictCursorMixin, Cursor

class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict

connection= pymysql.connect(host="home.wisewolf.org",
                            user="dbuser",
                            password="dbuser",
                            db="db_team_proj2",
                            charset="utf8")
def get_cursor():
    return connection.cursor()

def get_dict_cursor():
    return connection.cursor(OrderedDictCursor)
from db import get_cursor

def get_court_civil_freq():
    cursor= get_cursor()
    cursor.execute('SELECT 법원이름, count(*)'
                   'FROM 민사판결 join 민사판결법원 '
                   'on 민사판결.판결ID= 민사판결법원.판결ID group by 법원이름;')
    return cursor.fetchall()

def get_court_criminal_freq():
    cursor= get_cursor()
    cursor.execute('SELECT 법원이름, count(*)'
                   'FROM 형사판결 join 형사판결법원 '
                   'on 형사판결.판결ID= 형사판결법원.판결ID group by 법원이름;')
    return cursor.fetchall()

def get_courts():
    cursor= get_cursor()
    cursor.execute('select * from 법원')
    return cursor.fetchall()
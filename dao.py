from db import get_cursor, get_dict_cursor

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

def get_court_civil_precedents(court_name):
    cursor= get_dict_cursor()
    cursor.execute('SELECT * '
                   'FROM 민사판결 join 민사판결법원 '
                   'on 민사판결.판결ID= 민사판결법원.판결ID '
                   'where 법원이름=%s;', (court_name))
    return cursor.fetchall()

def get_precedents(precedents_id):
    cursor= get_dict_cursor()
    cursor.execute('')
    return ''

def get_court_criminal_precedents(court_name):
    cursor= get_dict_cursor()
    cursor.execute('SELECT * '
                   'FROM 형사판결 join 형사판결법원 '
                   'on 형사판결.판결ID= 형사판결법원.판결ID '
                   'where 법원이름=%s;', (court_name))
    return cursor.fetchall()

def get_top_accused():
    cursor= get_dict_cursor()
    cursor.execute('select 사람ID, count(*) as count '
                   'from (SELECT 소송ID as 소송ID, 사람.사람ID as 사람ID '
                   'FROM 형사판결피고 join 사람 join 형사판결 '
                   'on 사람.사람ID= 형사판결피고.피고ID and 형사판결.판결ID= 형사판결피고.판결ID '
                   'group by 형사판결.소송ID, 사람.사람ID) as 범죄자 '
                   'group by 사람ID '
                   'order by count desc '
                   'limit 3;')
    return cursor.fetchall();

def get_accused_info(accused_id):
    cursor= get_dict_cursor()
    cursor.execute("select 형사판결.판결ID, 형사판결.소송ID, 피고ID, 벌금형량, 징역형량, 사회봉사형량, 집행유예형량, 사형선고여부, 무기징역선고여부, 환송여부 "
                   "from 형사판결피고 join 형사판결 join 사람 "
                   "on 형사판결피고.판결ID= 형사판결.판결ID and 형사판결피고.피고ID= 사람.사람ID "
                   "where 형사판결피고.피고ID= %s;", (accused_id))
    return cursor.fetchall();

def get_criminal_pie():
    cursor= get_dict_cursor()
    cursor.execute("select 관련죄, count(*) as count "
                   "from (select 판결ID from 형사판결 "
                   "group by 판결ID) as 형사소송 join 형사판결법 join 법 "
                   "on 형사소송.판결ID= 형사판결법.판결ID and 형사판결법.법조ID=법.법조ID and 형사판결법.법항ID=법.법항ID "
                   "where 관련죄 is not null "
                   "group by 관련죄;")
    return cursor.fetchall()

def get_servitude_pie():
    cursor= get_dict_cursor()
    cursor.execute("select 관련죄, cast(AVG(징역형량) as CHAR) as 평균 "
                   "from 형사판결피고 join 형사판결 join 형사판결법 join 법 "
                   "on 형사판결피고.판결ID= 형사판결.판결ID and 형사판결법.판결ID= 형사판결.판결ID and 법.법조ID= 형사판결법.법조ID and 법.법항ID= 형사판결법.법항ID "
                   "where 관련죄 is not null "
                   "group by 관련죄;")
    return cursor.fetchall()

def get_fine_pie():
    cursor = get_dict_cursor()
    cursor.execute("select 관련죄, cast(AVG(벌금형량) as CHAR) as 평균 "
                   "from 형사판결피고 join 형사판결 join 형사판결법 join 법 "
                   "on 형사판결피고.판결ID= 형사판결.판결ID and 형사판결법.판결ID= 형사판결.판결ID and 법.법조ID= 형사판결법.법조ID and 법.법항ID= 형사판결법.법항ID "
                   "where 관련죄 is not null "
                   "group by 관련죄;")
    return cursor.fetchall()

def get_criminal_precedent(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 형사판결 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_precedent(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 민사판결 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_evidence(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 형사판결증거 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_evidence(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 민사판결증거 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_defendant(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 형사판결피고 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_defendant(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 민사판결피고 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_plaintiff(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 형사소송원고.* "
                   "from 형사소송원고 join 형사판결 "
                   "on 형사소송원고.소송ID= 형사판결.소송ID "
                   "where 형사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_plaintiff(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 민사소송원고.* "
                   "from 민사소송원고 join 민사판결 "
                   "on 민사소송원고.소송ID= 민사판결.소송ID "
                   "where 민사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_judge(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 형사판결판사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_judge(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select * from 민사판결판사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_law(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 법.법분류, 법.법조ID, 법.법항ID, 법.법호ID, 법.법목ID, 법.관련죄 "
                   "from 형사판결법 join 법 "
                   "on 형사판결법.법항ID= 법.법항ID and 형사판결법.법조ID= 법.법조ID and 형사판결법.법목ID= 법.법목ID "
                   "where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_law(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 법.법분류, 법.법조ID, 법.법항ID, 법.법호ID, 법.법목ID, 법.관련죄 "
                   "from 민사판결법 join 법 "
                   "on 민사판결법.법항ID= 법.법항ID and 민사판결법.법조ID= 법.법조ID and 민사판결법.법목ID= 법.법목ID "
                   "where 판결ID= %s", (precedent_id))
    return cursor.fetchall()
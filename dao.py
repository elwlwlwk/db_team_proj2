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
    cursor.execute("SELECT 형사판결.판결ID, 형사판결.소송ID, 형사판결법원.법원이름, 판시사항, 판결단계, 판결날짜, 판결주문, 환송여부, 판결기각여부, 판결전문, 변호사국선여부, 국민참여재판여부 "
                   "FROM 형사판결 join 형사판결법원 "
                   "on 형사판결.판결ID= 형사판결법원.판결ID "
                   "where 형사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_precedent(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("SELECT 민사판결.판결ID, 민사판결.소송ID, 민사판결법원.법원이름, 판시사항, 판결단계, 판결날짜, 판결주문, 환송여부, 판결기각여부, 판결전문 "
                   "FROM 민사판결 join 민사판결법원 "
                   "on 민사판결.판결ID= 민사판결법원.판결ID "
                   "where 민사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_evidence(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 판결ID, 증거ID, 증거이미지, 증거설명 from 형사판결증거 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_evidence(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 판결ID, 증거ID, 증거이미지, 증거설명 from 민사판결증거 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_defendant(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 피고ID, 벌금형량, 징역형량, 사회봉사형량, 집행유예형량, 무기징역선고여부, 사형선고여부 from 형사판결피고 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_defendant(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 피고ID, 법원조정여부 from 민사판결피고 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_plaintiff(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 형사소송원고.원고ID "
                   "from 형사소송원고 join 형사판결 "
                   "on 형사소송원고.소송ID= 형사판결.소송ID "
                   "where 형사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_plaintiff(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 민사소송원고.원고ID, 민사소송원고.법원조정여부 "
                   "from 민사소송원고 join 민사판결 "
                   "on 민사소송원고.소송ID= 민사판결.소송ID "
                   "where 민사판결.판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_judge(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 판사ID from 형사판결판사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_judge(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 판사ID from 민사판결판사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_prosecutor(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 검사ID from 형사판결검사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_lawyer(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 로펌, 변호사ID from 형사판결변호사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_lawyer(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 로펌, 변호사ID from 민사판결변호사 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_criminal_witness(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 증인ID from 형사판결증인 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_civil_witness(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 증인ID from 민사판결증인 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_deputy(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 소송대리인ID from 민사판결소송대리인 where 판결ID= %s", (precedent_id))
    return cursor.fetchall()

def get_juror(precedent_id):
    cursor = get_dict_cursor()
    cursor.execute("select 배심원ID from 형사판결배심원 where 판결ID= %s", (precedent_id))
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

def get_criminal_precedent_by_charge(charge, dismiss, farewell):
    cursor = get_dict_cursor()
    cursor.execute("select 죄형사판결.판결ID, 죄형사판결.소송ID, 판결날짜, 판결단계, 환송여부, 판결기각여부, 국민참여재판여부, GROUP_CONCAT(관련죄) as 관련법 "
                   "from (select 형사판결.* "
                   "from 형사판결 join 형사판결법 join 법 "
                   "on 형사판결.판결ID= 형사판결법.판결ID and 형사판결법.법항ID= 법.법항ID and 형사판결법.법조ID= 법.법조ID and 형사판결법.법목ID= 법.법목ID "
                   "where 관련죄 like %s and 환송여부=%s and 판결기각여부=%s) as 죄형사판결 join 형사판결법 join 법 "
                   "on 죄형사판결.판결ID= 형사판결법.판결ID and 형사판결법.법항ID= 법.법항ID and 형사판결법.법조ID= 법.법조ID and 형사판결법.법목ID= 법.법목ID "
                   "group by 판결ID, 소송ID, 판결날짜, 판결단계, 환송여부, 판결기각여부, 국민참여재판여부", ('%'+charge+'%', farewell, dismiss))
    return cursor.fetchall()

def get_civil_precedent_by_charge(charge, dismiss, farewell):
    cursor = get_dict_cursor()
    cursor.execute("select 죄민사판결.판결ID, 죄민사판결.소송ID, 판결날짜, 판결단계, 환송여부, 판결기각여부, GROUP_CONCAT(관련죄) as 관련법 "
                   "from (select 민사판결.* from 민사판결 join 민사판결법 join 법 "
                   "on 민사판결.판결ID= 민사판결법.판결ID and 민사판결법.법항ID= 법.법항ID and 민사판결법.법조ID= 법.법조ID and 민사판결법.법목ID= 법.법목ID "
                   "where 관련죄 like %s and 환송여부=%s and 판결기각여부=%s) as 죄민사판결 join 민사판결법 join 법 "
                   "on 죄민사판결.판결ID= 민사판결법.판결ID and 민사판결법.법항ID= 법.법항ID and 민사판결법.법조ID= 법.법조ID and 민사판결법.법목ID= 법.법목ID "
                   "group by 판결ID, 소송ID, 판결날짜, 판결단계, 환송여부, 판결기각여부", ('%'+charge+'%', farewell, dismiss))
    return cursor.fetchall()
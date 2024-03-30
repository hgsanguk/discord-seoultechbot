import datetime
import sqlite3
import requests
from bs4 import BeautifulSoup

food_db = sqlite3.connect("food.db", isolation_level=None)
cur = food_db.cursor()


def initial():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS TechnoPark (year_week integer PRIMARY KEY, title text, uploaded_date integer unique, img_link text)")
    cur.execute("CREATE TABLE IF NOT EXISTS Student_Cafeteria_2 \
                (year_month_date integer PRIMARY KEY,"
                "menu1_name text, menu1_price text, menu1_side text,"
                "menu2_name text, menu2_price text, menu2_side text,"
                "dinner_name text, dinner_price text, dinner_side text)")


def student_cafeteria_2(tomorrow=False):
    basedate = datetime.date.today()
    if tomorrow:
        basedate += datetime.timedelta(days=1)
    try:
        response = requests.get('https://www.seoultech.ac.kr/life/student/food2/?location_code=20&food_date=' + basedate.strftime('%Y-%m-%d'))
        parser = BeautifulSoup(response.text, "html.parser")
        rows = parser.select('.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tr')
        menu1 = [rows[1].select('td:nth-child(1)')[0].text.strip(),
                 rows[1].select('td:nth-child(2)')[0].text.strip(),
                 rows[1].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]
        menu2 = [rows[2].select('td:nth-child(1)')[0].text.strip(),
                 rows[2].select('td:nth-child(2)')[0].text.strip(),
                 rows[2].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]
        rows = parser.select('.dts_design > div:nth-child(5) > div:nth-child(4) > table:nth-child(1) > tr')
        dinner_menu = [rows[1].select('td:nth-child(1)')[0].text.strip(),
                       rows[1].select('td:nth-child(2)')[0].text.strip(),
                       rows[1].select('td:nth-child(3)')[0].text.strip().replace('\t', '').replace('\r', '')]
        try:
            cur.execute('INSERT INTO Student_Cafeteria_2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (int(basedate.strftime('%y%m%d')),
                         menu1[0], menu1[1], menu1[2], menu2[0], menu2[1], menu2[2],
                         dinner_menu[0], dinner_menu[1], dinner_menu[2]))
            print(f'{datetime.datetime.now()}: 제2학생회관 크롤링 성공!')
        except sqlite3.IntegrityError:
            cur.execute('UPDATE Student_Cafeteria_2 SET menu1_name=?, menu1_price=?, menu1_side=?,'
                        'menu2_name=?, menu2_price=?, menu2_side=?, dinner_name=?, dinner_price=?, dinner_side=? '
                        'WHERE year_month_date=?',
                        (menu1[0], menu1[1], menu1[2], menu2[0], menu2[1], menu2[2], dinner_menu[0], dinner_menu[1], dinner_menu[2], int(datetime.date.today().strftime('%y%m%d'))))
            print(f'{datetime.datetime.now()}: 제2학생회관 크롤링 성공!')

        cur.execute('SELECT count(year_month_date) FROM Student_Cafeteria_2')
        count = cur.fetchall()[0][0]
        while count > 4:
            cur.execute('DELETE FROM Student_Cafeteria_2 WHERE year_month_date = (SELECT min(year_month_date) FROM Student_Cafeteria_2)')
            count -= 1
    except IndexError:
        if tomorrow:
            print(f'{datetime.datetime.now()}: 크롤링 실패. (내일의 식단 등록 안 됨)')
        else:
            print(f'{datetime.datetime.now()}: 크롤링 실패. 다음 주기에 다시 시도합니다. (오늘의 식단 등록 안 됨)')
    except requests.ConnectTimeout:
        print(f'{datetime.datetime.now()}: 크롤링 실패. 다음 주기에 다시 시도합니다. (학교 홈페이지 응답 없음)')



def technopark():
    try:
        response = requests.get('https://www.seoultp.or.kr/user/nd70791.do')
        parser = BeautifulSoup(response.text, "html.parser")
        bnum = str(parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')[0]).split("'")[5]
        title = parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')[0].text.strip()
        uploaded_date = parser.select('.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(4)')[0].text.strip().replace('.', '')
        response = requests.get('https://www.seoultp.or.kr/user/nd70791.do?View&boardNo=' + bnum)
        parser = BeautifulSoup(response.text, "html.parser")
        board_area = parser.select('.board-write > tbody:nth-child(3) > tr:nth-child(4)')[0]
        picture_link = 'https://www.seoultp.or.kr' + board_area.find_all(name='img')[0].get('src')
        try:
            cur.execute('INSERT INTO TechnoPark VALUES(?, ?, ?, ?)', (int(datetime.date.today().strftime('%y%W')),
                                                                      title, int(uploaded_date), picture_link))
            print(f'{datetime.datetime.now()}: 서울테크노파크 식단 크롤링 성공!')
        except sqlite3.IntegrityError:
            print(f'{datetime.datetime.now()}: 크롤링 실패. 다음 주기에 다시 시도합니다. (지난주 게시글 크롤링 시도)')
        cur.execute('SELECT count(year_week) FROM TechnoPark')
        count = cur.fetchall()[0][0]
        while count > 4:
            cur.execute('DELETE FROM TechnoPark WHERE year_week = (SELECT min(year_week) FROM TechnoPark)')
            count -= 1
    except requests.ConnectTimeout:
        print(f'{datetime.datetime.now()}: 크롤링 실패. 다음 주기에 다시 시도합니다. (테크노파크 홈페이지 응답 없음)')


def get_sc2_menu(date):
    cur.execute('SELECT menu1_name, menu1_price, menu1_side, '
                'menu2_name, menu2_price, menu2_side, '
                'dinner_name, dinner_price, dinner_side FROM Student_Cafeteria_2 WHERE year_month_date=?', (date,))
    return cur.fetchall()[0]


def get_technopark_menu(week):
    cur.execute('SELECT title, img_link FROM TechnoPark WHERE year_week=?', (week,))
    return cur.fetchall()[0]

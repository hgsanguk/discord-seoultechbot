import sqlite3
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

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


def load_browser(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def student_cafeteria_2():
    driver = load_browser('https://www.seoultech.ac.kr/life/student/food2/')
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.location:nth-child(1) > label:nth-child(2) > span:nth-child(2)")))
        element.click()
        driver.implicitly_wait(4)
        row1 = driver.find_element(By.CSS_SELECTOR,
                                   '.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)')
        menu1 = [row1.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text,
                 row1.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text,
                 row1.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
        row2 = driver.find_element(By.CSS_SELECTOR,
                                   '.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)')
        menu2 = [row2.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text,
                 row2.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text,
                 row2.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
        row3 = driver.find_element(By.CSS_SELECTOR,
                                   '.dts_design > div:nth-child(5) > div:nth-child(4) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)')
        dinner_menu = [row3.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text,
                       row3.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text,
                       row3.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
        driver.close()
        try:
            cur.execute('INSERT INTO Student_Cafeteria_2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (int(datetime.date.today().strftime('%y%m%d')),
                         menu1[0], menu1[1], menu1[2], menu2[0], menu2[1], menu2[2],
                         dinner_menu[0], dinner_menu[1], dinner_menu[2]))
            print('제2학생회관 크롤링 성공!')
        except sqlite3.IntegrityError:
            cur.execute('UPDATE Student_Cafeteria_2 SET menu1_name=?, menu1_price=?, menu1_side=?,'
                        'menu2_name=?, menu2_price=?, menu2_side=?, dinner_name=?, dinner_price=?, dinner_side=? '
                        'WHERE year_month_date=?',
                        (menu1[0], menu1[1], menu1[2], menu2[0], menu2[1], menu2[2], dinner_menu[0], dinner_menu[1], dinner_menu[2], int(datetime.date.today().strftime('%y%m%d'))))
            print('제2학생회관 크롤링 성공!')
    except NoSuchElementException:
        print('크롤링 실패. 다음 주기에 다시 시도합니다. (오늘의 식단표 없음)')
        driver.close()


def technopark():
    driver = load_browser('https://www.seoultp.or.kr/user/nd70791.do')
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)")))
        last_post = driver.find_element(By.CSS_SELECTOR, '.board-list > tbody:nth-child(4) > tr:nth-child(1)')
        title = last_post.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
        uploaded_date = int(last_post.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.replace('.', ''))
        element.click()
        driver.implicitly_wait(4)
        board = driver.find_element(By.CSS_SELECTOR, '.table-cont')
        pic = board.find_element(By.TAG_NAME, 'img')
        picture_link = pic.get_attribute('src')
        driver.close()
        try:
            cur.execute('INSERT INTO TechnoPark VALUES(?, ?, ?, ?)',
                        (int(datetime.date.today().strftime('%y%W')),
                         title, uploaded_date, picture_link))
            print('서울테크노파크 식단 크롤링 성공!')
        except sqlite3.IntegrityError:
            print('크롤링 실패. 다음 주기에 다시 시도합니다. (지난주 게시글 크롤링 시도)')
    except NoSuchElementException:
        print('크롤링 실패. 다음 주기에 다시 시도합니다. (페이지의 레이아웃 변경됨)')
        driver.close()


def get_sc2_menu(date):
    cur.execute('SELECT menu1_name, menu1_price, menu1_side, '
                'menu2_name, menu2_price, menu2_side, '
                'dinner_name, dinner_price, dinner_side FROM Student_Cafeteria_2 WHERE year_month_date=?', (date,))
    return cur.fetchall()[0]


def get_technopark_menu(week):
    cur.execute('SELECT title, img_link FROM TechnoPark WHERE year_week=?', (week,))
    return cur.fetchall()[0]



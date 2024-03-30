import sqlite3
import requests
import datetime
from bs4 import BeautifulSoup

notice_db = sqlite3.connect("notice.db", isolation_level=None)
cur = notice_db.cursor()


def initial():
    cur.execute("CREATE TABLE IF NOT EXISTS University (board_index integer PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS Affairs (board_index integer PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scholarship (board_index integer PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS Dormitory (board_index integer PRIMARY KEY)")


def get_notice(board_name, table_name):
    response = requests.get('https://www.seoultech.ac.kr/service/info/' + board_name + '/')
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.select('.tbl_list > tbody:nth-child(4) > tr')
    new_notice = []
    for row in rows:
        try:
            title = row.select('td:nth-child(2) > a')[0].text.strip()
            author = row.select('td:nth-child(4)')[0].text.strip()
            url = row.select('td:nth-child(2) > a')[0].get('href')
            bidx = int(url.split('&')[5].strip('bidx='))
            try:
                cur.execute('INSERT INTO ' + table_name + ' VALUES(?)', (bidx,))
                new_notice.append([title, author, 'https://www.seoultech.ac.kr/service/info/' + board_name + url])
            except sqlite3.IntegrityError:
                continue
        except IndexError:
            continue
    cur.execute('SELECT count(board_index) FROM ' + table_name)
    count = cur.fetchall()[0][0]
    while count > 200:
        cur.execute('DELETE FROM ' + table_name + ' WHERE board_index = (SELECT min(board_index) FROM ' + table_name + ')')
        count -= 1
    return new_notice


def get_domi_notice():
    response = requests.get('https://domi.seoultech.ac.kr/do/notice/')
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.select('.list_3 > li')
    new_notice = []
    for row in rows:
        title = row.select('a:nth-child(1)')[0].text.strip()
        url = row.select('a:nth-child(1)')[0].get('href')
        bidx = int(url.split('&')[2].strip('bidx='))
        try:
            cur.execute('INSERT INTO Dormitory VALUES(?)', (bidx,))
            response = requests.get('https://domi.seoultech.ac.kr/do/notice/' + url)
            parser = BeautifulSoup(response.text, "html.parser")
            try:
                author = parser.select('.date > span:nth-child(2) > font:nth-child(1)')[0].text
            except IndexError:
                author = parser.select('.date > span:nth-child(3) > font:nth-child(1)')[0].text
            new_notice.append([title, author, 'https://domi.seoultech.ac.kr/do/notice/' + url])
        except sqlite3.IntegrityError:
            continue
    cur.execute('SELECT count(board_index) FROM Dormitory')
    count = cur.fetchall()[0][0]
    while count > 100:
        cur.execute('DELETE FROM Dormitory WHERE board_index = (SELECT min(board_index) FROM Dormitory)')
        count -= 1
    return new_notice


def get_univ_schedule():
    response = requests.get('https://eclass.seoultech.ac.kr/ilos/main/main_schedule_view.acl?viewDt=' + datetime.date.today().strftime('%Y%m%d'))
    parser = BeautifulSoup(response.text, "html.parser")
    rows = parser.find_all(class_='changeDetile schedule-Detail-Box')
    schedule = []
    for row in rows:
        schedule.append(row.text.strip())
    return schedule

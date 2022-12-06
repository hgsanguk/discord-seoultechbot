import sqlite3
import requests
from bs4 import BeautifulSoup as bs

notice_db = sqlite3.connect("notice.db", isolation_level=None)
cur = notice_db.cursor()


def initial():
    cur.execute("CREATE TABLE IF NOT EXISTS University (board_index integer PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS Affairs (board_index integer PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS Scholarship (board_index integer PRIMARY KEY)")


def requests_board(url):
    response = requests.get(url)
    parser = bs(response.text, "html.parser")
    rows = parser.select('.tbl_list > tbody:nth-child(4) > tr')
    return rows


def univ_notice():
    rows = requests_board('https://www.seoultech.ac.kr/service/info/notice/')
    new_notice = []
    for row in rows:
        try:
            title = row.select('td:nth-child(2) > a')[0].text.strip()
            author = row.select('td:nth-child(4)')[0].text.strip()
            date = row.select('td:nth-child(5)')[0].text.strip()
            url = row.select('td:nth-child(2) > a')[0].get('href')
            bidx = int(url.split('&')[5].strip('bidx='))
            try:
                cur.execute('INSERT INTO University VALUES(?)', (bidx,))
                new_notice.append([title, author, date, 'https://www.seoultech.ac.kr/service/info/notice' + url])
            except sqlite3.IntegrityError:
                continue
        except IndexError:
            continue
    return new_notice


def affairs_notice():
    rows = requests_board('https://www.seoultech.ac.kr/service/info/matters/')
    new_notice = []
    for row in rows:
        try:
            title = row.select('td:nth-child(2) > a')[0].text.strip()
            author = row.select('td:nth-child(4)')[0].text.strip()
            date = row.select('td:nth-child(5)')[0].text.strip()
            url = row.select('td:nth-child(2) > a')[0].get('href')
            bidx = int(url.split('&')[5].strip('bidx='))
            try:
                cur.execute('INSERT INTO Affairs VALUES(?)', (bidx,))
                new_notice.append([title, author, date, 'https://www.seoultech.ac.kr/service/info/matters' + url])
            except sqlite3.IntegrityError:
                continue
        except IndexError:
            continue
    return new_notice


def scholarship_notice():
    rows = requests_board('https://www.seoultech.ac.kr/service/info/janghak')
    new_notice = []
    for row in rows:
        try:
            title = row.select('td:nth-child(2) > a')[0].text.strip()
            author = row.select('td:nth-child(4)')[0].text.strip()
            date = row.select('td:nth-child(5)')[0].text.strip()
            url = row.select('td:nth-child(2) > a')[0].get('href')
            bidx = int(url.split('&')[5].strip('bidx='))
            try:
                cur.execute('INSERT INTO Scholarship VALUES(?)', (bidx,))
                new_notice.append([title, author, date, 'https://www.seoultech.ac.kr/service/info/janghak' + url])
            except sqlite3.IntegrityError:
                continue
        except IndexError:
            continue
    return new_notice

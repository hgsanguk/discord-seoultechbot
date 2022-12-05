import requests
from bs4 import BeautifulSoup as bs


if __name__ == '__main__':
    response = requests.get('https://www.seoultech.ac.kr/service/info/notice/')
    parser = bs(response.text, "html.parser")
    rows = parser.select('.tbl_list > tbody:nth-child(4) > tr')
    for row in rows:
        try:
            print(row.select('td:nth-child(2) > a:nth-child(1)')[0].text.strip())
            print(row.select('td:nth-child(4)')[0].text.strip())
            print(row.select('td:nth-child(5)')[0].text.strip() + '\n')
        except IndexError:
            continue
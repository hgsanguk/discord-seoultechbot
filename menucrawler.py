from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def load_browser():
    driver = webdriver.Firefox()
    options = webdriver.FirefoxOptions()
    options.add_argument('headless')
    driver.implicitly_wait(2)
    return driver

def student_cafeteria_2():
    driver = load_browser()
    driver.get('https://www.seoultech.ac.kr/life/student/food2/')
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.location:nth-child(1) > label:nth-child(2) > span:nth-child(2)")))
        element.click()
        driver.implicitly_wait(4)
        row0 = driver.find_element(By.CSS_SELECTOR, '.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)')
        element0 = [row0.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text,
                    row0.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text,
                    row0.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
        row1 = driver.find_element(By.CSS_SELECTOR,'.dts_design > div:nth-child(5) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)')
        element1 = [row1.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text,
                    row1.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text,
                    row1.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
        driver.close()
        return element0, element1
    except NoSuchElementException:
        driver.close()
        return ['', '', '제2학생회관에 등록된 오늘의 식단표가 없습니다.'], ['', '', '제2학생회관에 등록된 오늘의 식단표가 없습니다.']


def technopark():
    driver = load_browser()
    driver.get('https://www.seoultp.or.kr/user/nd70791.do')
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)")))
    week = driver.find_element(By.CSS_SELECTOR, '.board-list > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(2)').text
    element.click()
    driver.implicitly_wait(4)
    board = driver.find_element(By.CSS_SELECTOR, '.table-cont')
    pic = board.find_element(By.TAG_NAME, 'img')
    picturelink = pic.get_attribute('src')
    driver.close()
    return week, picturelink

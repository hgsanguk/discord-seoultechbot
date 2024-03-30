# 로거 가져오기
import seoultechbot
logger = seoultechbot.Logger.setup('crawler')

from seoultechbot.dbconnector import dbconnector

dbconnector.execute("CREATE TABLE IF NOT EXISTS University (board_index integer PRIMARY KEY)")
dbconnector.execute("CREATE TABLE IF NOT EXISTS Affairs (board_index integer PRIMARY KEY)")
dbconnector.execute("CREATE TABLE IF NOT EXISTS Scholarship (board_index integer PRIMARY KEY)")
dbconnector.execute("CREATE TABLE IF NOT EXISTS Dormitory (board_index integer PRIMARY KEY)")
dbconnector.execute("CREATE TABLE IF NOT EXISTS TechnoPark (year_week integer PRIMARY KEY, title text, uploaded_date integer unique, img_link text)")
dbconnector.execute("CREATE TABLE IF NOT EXISTS Student_Cafeteria_2 \
                    (year_month_date integer PRIMARY KEY,"
                    "menu1_name text, menu1_price text, menu1_side text,"
                    "menu2_name text, menu2_price text, menu2_side text,"
                    "dinner_name text, dinner_price text, dinner_side text)")
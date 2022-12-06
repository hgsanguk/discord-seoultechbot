# TechBot - Discord Bot for SEOULTECH
## 소개
Discord.py를 이용하여 서울과학기술대학교의 식당의 메뉴~~와 공지사항~~을 알려주는 봇입니다.
현재는 학식 알림만 이용 가능하며 공지사항 알림과 다양한 기능은 추후 업데이트 예정입니다.

## 코드 실행 전 준비 사항
### Packages
1. discord.py
2. selenium
3. requests
4. BeautifulSoup

해당 패키지들은 로컬 저장소에서 `pip install -r techbot-packages.txt` 명령어로 한 번에 설치 가능합니다.

### Internet Browsers
해당 코드에서는 Selenium에서 Web Driver로 Firefox와 이 브라우저에 쓰이는 엔진인 Gecko를 사용합니다.
다른 브라우저 사용 시 그에 맞는 버전의 Web Driver를 로걸 저장소와 같은 위치에 다운로드하고, `menucrawler.py`의 아래 부분을 알맞게 수정하시면 됩니다.
``` python 
...
from selenium.webdriver.firefox.options import Options
...
def load_browser(url):
    ...
    driver = webdriver.Firefox(options=options)
    ...
```

### Discord Bot Token
해당 프로그램은 Discord 계정과 [Discord Developers Portal](https://discord.com/developers/)에서 Applications > Bot의 토큰을 요구합니다. 토큰을 발급받아 `discord.py`의 마지막 줄을 수정하여 자신의 봇에 적용할 수 있습니다.

```python
bot.run('Your Discord Bot Token')
```
위의 코드처럼 str 형식으로 디스코드 봇 토큰을 입력하거나, 
```python
import os
...
bot.run(os.getenv('DiscordBotToken'))
```
토큰 노출이 걱정된다면 위의 코드처럼 운영체제의 환경변수로 저장하고 이를 불러와 코드를 실행할 수 있습니다.


## 파일 설명
* `discordbot.py`: Discord 봇의 동작에 필요한 핵심적인 코드입니다.
* `server_settings.py`: SQLite3을 이용하여 각 서버에서 설정한 알림 시간을 저장 및 수정하는 코드입니다.
* `menucrawler.py`: SQLite3과 Selenium을 이용하여 학교 홈페이지에서 식단을 크롤링하고 데이터베이스에 저장, 불러오는 코드입니다.
* `noicecrawler.py`: SQLite3과 requests, BeautifulSoup을 이용하여 학교 공지사항을 데이터베이스에 저장, 불러오는 코드입니다.


## 작동 스크린샷
작성 중...

## 배포
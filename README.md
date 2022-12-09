# TechBot Project - Discord Bot for SEOULTECH
## Introduction
discord.py를 이용하여 서울과학기술대학교의 식당의 메뉴와 공지사항을 자동으로 알려주고, ~~각종~~ 편의기능을 제공하는 Discord 봇 프로젝트 입니다.

학교 공지사항의 접근성을 높히고 빈번히 오작동하는 에브리타임 기능인 오늘의 학식을 대체하기 위해, 서울과기대 학우 분들이 많이 사용하는 메신저 'Discord'의 API를 이용하는 자동화 채팅 봇을 개발하기로 했습니다.

서울과학기술대학교 컴퓨터공학과의 2022학년도 2학기 전공선택 과목 '오픈소스소프트웨어', '데이터베이스'의 개인 프로젝트로 시작하여, 해당 코드를 사용한 봇을 배포했습니다.
스스로 사용할 목적으로 만든 봇이라서 꾸준히 유지보수, 기능 추가와 최적화를 거칠 계획입니다.

## Developer
* 21101476 이상욱

## Release
우측의 Releases를 클릭하여 이 프로젝트의 안정적인 버전을 사용한 '테크봇'을 초대할 수 있습니다.
봇/코드 업데이트 시 변경사항도 Releases를 통해 안내할 예정입니다.

해당 봇은 자동 알림을 위해 모든 채널을 감지하지 않으며, 입장 메세지를 보내지 않습니다. 따라서 봇 초대 시 반드시 `/도움` 명령어를 입력하여 설명을 읽어보시길 바랍니다.

### Features and Commands
* 공지사항과 학식 자동 알림
  * 2시간 간격으로 학교 홈페이지의 학교공지사항, 학사공지, 장학공지를 체크하여, 새 공지사항이 올라왔다면 `/알림설정` 명령어를 사용한 채널에 알림을 보냅니다.
  * 디스코드 서버의 관리자(혹은 메세지 관리 권한 소유자)가 지정한 시간에 제2학생회관과 테크노파크의 식단을 출력합니다.


* 봇 조작 명령어
  * `/도움`: 명령어의 목록을 볼 수 있습니다.
  * `/알림설정 n`: 해당 명령어를 친 채널이 알림을 받을 채널이 됩니다. 옵션은 아래를 참고하세요.
    **해당 명령어의 사용자는 관리자 권한, 또는 메세지 관리 권한이 있어야 합니다.**
    * `n = 0`: 학식 알림을 받지 않습니다. 숫자를 입력하지 않는 경우도 해당됩니다.
    * `9 <= n <= 12`: `n`시 정각에 제2학생화관과 테크노파크의 식단을 알립니다.
    * 봇 초대 후 이 명령어를 입력하지 않으면 공지사항 알림, 학식 자동 알림을 받을 수 없습니다. 아래의 명령어는 정상작동 합니다.


* 학교 생활 명령어
  * `/2학`: 오늘의 제2학생회관의 점심, 저녁 식단 메뉴를 출력합니다.
  * `/테파`: 이번 주 테크노파크의 식단 메뉴를 이미지로 출력합니다.
  * `/날씨 n`: 캠퍼스가 있는 공릉동의 n시간 뒤 날씨 예보를 출력합니다. n이 없을 경우 현재 날씨를 출력합니다. (`0 <= n <= 4`)


* 계획 중
  * ~~`/2학 내일`~~: 내일의 제2학생회관의 점심, 저녁 식단 메뉴를 출력합니다.
  * ~~`/생활관공지`~~: 생활관 공지 자동 알림 기능을 켜고 끕니다.


### Working Screenshots
작성 중...

### Bug Report
문제 발생 시 반드시 **해당 서버, 채널의 ID와 함께** issue를 작성해주시기 바랍니다.

---
## Getting Started with My Bot
명령어는 python3이 설치된 Linux 환경을 기준으로 설명했으며, 명령어를 제외한 나머지 설명은 Windows 환경에서도 동일합니다.
### Get Code
```shell
$ git clone https://github.com/az0t0/discord-seoultechbot.git
```
git을 사용해 위의 명령어로 최신 버전의 로컬 저장소를 clone하거나, Releases에서 안정적인 버전의 코드를 내려받을 수 있습니다.
### Require Packages
1. discord.py
2. selenium
3. requests
4. beautifulsoup4

해당 패키지들은 로컬 저장소 내에서 `$ pip install -r techbot-packages.txt` 명령어로 한 번에 설치 가능합니다.

### Internet Browser
이 봇은 Selenium을 사용하므로 Web Driver를 요구합니다. 이 코드의 경우 Firefox와 이 브라우저에 쓰이는 엔진인 Gecko를 사용합니다.
다른 브라우저 사용 시 그에 맞는 버전의 Web Driver를 로걸 저장소의 src와 같은 위치에 다운로드하고, `menucrawler.py`의 아래 부분을 알맞게 수정하시면 됩니다.
``` python 
...
from selenium.webdriver.firefox.options import Options
...
def load_browser(url):
    ...
    driver = webdriver.Firefox(options=options)
    ...
```

### Token
Discord 봇을 만들기 위해 Discord 계정과 [Discord Developers Portal](https://discord.com/developers/)의 Applications > 내 앱 > Bot에서 모든 Intents 옵션과 토큰이 필요합니다.


또한 `/날씨 n` 명령어를 사용하려면 [오픈 API의 기상청 단기예보 조회서비스](https://www.data.go.kr/data/15084084/openapi.do)에서 인증키를 발급 받아야 합니다.

토큰을 요구하는 부분은 아래와 같습니다.

```python
...
import os
...
token_path = os.path.dirname(os.path.abspath(__file__)) + "/token"
token_file = open(token_path, "r", encoding="utf-8").read().split()
discord_bot_token = token_file[0]
weather_api_token = token_file[1]
...
@bot.command()
async def 날씨(ctx, args='0'):
    try:
        args = int(args)
        if 0 <= args < 5:
            data = weather.get_weather(weather_api_token, args)
            ...
...
bot.run(discord_bot_token)
```
`discordbot.py`와 같은 경로에 `token` 파일(확장자 없음)을 만들어 첫번째 줄에는 **Discord 봇의 토큰**, 두번째 줄에는 오픈 API에서 발급받은 **일반 인증키**를 입력하면 됩니다.
**토큰 노출 예방을 위해 `token` 파일이 `.gitignore`에 추가 되어있는지 반드시 확인하세요.**

### Run
```shell
$ cd /discord-seoultechbot/src
$ nohup python3 discord.py > discordbot.log 2>&1 &
```
백그라운드에서 봇이 실행되며, `discordbot.log` 파일에서 로그를 확인해볼 수 있습니다.
[Discord Developers Portal](https://discord.com/developers/)의 Applications > 내 앱 > OAuth2에서 bot 체크 후 생성되는 링크를 통해 봇을 초대할 수 있습니다.


---
## About Files
### Repository 내
* `discordbot.py`: Discord 봇의 동작에 필요한 핵심적인 코드입니다.
* `server_settings.py`: SQLite3을 이용하여 각 서버에서 설정한 알림 시간을 저장 및 수정하는 코드입니다.
* `menucrawler.py`: SQLite3과 Selenium을 이용하여 학교 홈페이지에서 식단을 크롤링하고 데이터베이스에 저장, 불러오는 코드입니다.
* `noticecrawler.py`: SQLite3과 requests, BeautifulSoup을 이용하여 학교 공지사항을 데이터베이스에 저장, 불러오는 코드입니다.
* `weather.py`: 정부의 오픈 API와 requests를 이용하여 캠퍼스의 날씨 예보를 불러오는 코드입니다.

### Runtime
* `food.db`: 학교 홈페이지에서 크롤링 한 식단을 저장하는 데이터베이스 파일입니다.
* `notice.db`: 학교 공지사항의 게시글 번호를 저장하는 데이터베이스 파일입니다.
* `server_settings.db`: 각 서버에서 설정한 알림 받을 채널의 ID를 저장하는 데이터베이스 파일입니다.


## Reference
* [Permission Check Discord.py Bot](https://stackoverflow.com/questions/52593777/permission-check-discord-py-bot): `/알림설정` 사용 시 권한 체크 방법에 참고했습니다.
* [[봇 개발] 4. 디스코드 봇 만들기 - 상태 표시 下](https://gall.dcinside.com/mgallery/board/view?id=discord&no=5724): 상태 메세지를 순환 표시하기 위해 참고하였습니다.
* [[봇 개발] 5. 디스코드 봇 만들기 - Embed](https://gall.dcinside.com/mgallery/board/view/?id=discord&no=5852): Embed 코드 작성에 참고하였습니다.
* [[Python] 공공 open API 실습 프로젝트](https://velog.io/@yebinlee/Python-API-%EC%8B%A4%EC%8A%B5): 날씨 API 응용, json 파싱에 참고하였습니다.

## License
* 이 프로젝트의 라이센스는 GNU GPL 3.0이며, 자세한 내용은 `LICENSE`를 참고하시기 바랍니다.
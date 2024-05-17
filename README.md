# SeoulTechBot - Discord Bot for SEOULTECH
## Introduction
discord.py를 이용하여 서울과학기술대학교의 식당의 메뉴와 공지사항을 자동으로 알려주고, 편의기능을 제공하는 Discord 봇입니다.

학교 공지사항의 접근성을 높히고 빈번히 오작동하는 에브리타임 기능인 오늘의 학식을 대체하기 위해, 서울과기대 학우 분들이 많이 사용하는 메신저 Discord의 자동화 채팅 봇을 개발하기로 했습니다.

서울과학기술대학교 컴퓨터공학과의 2022학년도 2학기 전공선택 과목 '오픈소스소프트웨어', '데이터베이스'의 개인 프로젝트로 시작하여, 해당 코드를 사용한 봇을 배포했습니다.
스스로 사용할 목적으로 만든 프로젝트라서 꾸준히 유지보수, 기능 추가와 최적화를 거칠 계획입니다.


## Release
[링크](https://discord.com/oauth2/authorize?client_id=1039918713413050438)를 클릭하여 이 프로젝트의 안정적인 버전을 사용한 '테크봇'을 초대할 수 있습니다.
혹은, 자신의 봇으로 운영하고 싶은 경우 아래의 Getting Started with My Bot 항목을 참조해주세요.
봇/코드 업데이트 시 변경사항은 Releases와 [SeoulTechBot 공식 서버](https://discord.gg/wRXRHB7mr6)의 `#봇-공지`채널을 통해 안내할 예정입니다.


### Features and Commands
* 공지사항과 학식 자동 알림
  * 오늘의 학사일정이 있을 경우 매일 자정 알림을 보냅니다.
  * 봇 관리자가 지정한 간격으로 학교 홈페이지의 학교공지사항, 학사공지, 장학공지, 생활관공지를 스크래핑하며, 새 공지사항이 올라왔다면 알림을 보냅니다.
  * ~~일정한 간격으로 단과대학 공지사항, 학과 공지사항을 스크래핑하며, 새 공지사항이 올라왔다면 알림을 보냅니다.~~
  * 디스코드 서버의 관리자가 지정한 시간에 제2학생회관과 테크노파크의 식단 알림을 보냅니다.


* 봇 조작 명령어
  * `/도움`: 테크봇의 명령어 목록과 설명을 볼 수 있습니다.
  * `/설정 [옵션]`: 봇을 설정하는 명령어입니다.
    * `[옵션]`
      * `[알림 설정]`: 해당 명령어를 입력한 채널이 각종 알림을 받을 채널이 됩니다.
        * `[식당 메뉴]`: `9시/10시/11시/12시` 중 원하는 알림 시간 선택
        * `[대학교 공지사항]`: 해당 옵션 선택 시 학교공지사항, 학사공지, 장학공지는 기본으로 활성화. 기숙사 알림 수신 여부는 `받음/받지않음` 중 선택 가능
        * ~~`[단과대학 공지사항]`~~: 공지사항 알림 받을 단과대학 복수 선택 (추후 지원 예정)
        * ~~`[학과공지사항]`~~: 원하는 `[단과대학]`를 선택 후 공지사항 알림 받을 학과 복수 선택 (추후 지원 예정)
        * ~~`[기타]`~~: 대학원 공지사항, 기숙사 식당 메뉴, 취업 등 알림 선택 (추후 지원 예정)
      * `[알림 해제]`: 서버에서 설정한 알림을 선택하여 해제가 가능합니다.
      * `[초기화]`: 서버에서 설정한 알림을 일괄 해제합니다.
    * **해당 명령어의 사용자는 관리자 권한이 있어야 합니다.**
    * 봇 초대 후 이 명령어를 사용해야 각종 알림을 받을 수 있습니다.
  * `/정보`: 서버에서 받는 알림의 종류와 봇의 정보를 보여줍니다.
  * `/핑`: 봇과 Discord 서버 간의 평균 지연시간을 보여줍니다.


* 학교 생활 명령어
  * `/2학 [요일]`: 제2학생회관의 오늘 식단(점심, 저녁)을 보여줍니다. 2024년 5월 8일 기준으로 점심의 간단 snack 메뉴는 항상 같으므로 생략합니다.
    * `[요일]` 옵션으로 원하는 요일의 제2학생회관 식단을 확인 가능합니다.
  * `/테파`: 테크노파크의 이번 주 식단표를 이미지로 보여줍니다.
  * `/날씨`: 캠퍼스가 있는 공릉2동의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.

### Screenshots
#### 식단과 공지사항 푸시 알림
![/알림설정 명령어 사용](https://user-images.githubusercontent.com/113516890/210235310-7ca6037d-9979-40d5-828e-a04b8b5c59dd.png)

![공지사항 자동알림](https://user-images.githubusercontent.com/113516890/210235400-d9f9caa9-1e2e-4f36-a309-ae18b73eb85c.png)

#### 일정 알림
![오늘의 일정 자동 알림](https://user-images.githubusercontent.com/113516890/217039793-aaa4d150-f5fc-4881-af2c-e1735adcc5a0.png)

#### `/2학`, `/테파` 명령어 사용
![/테파 명령어 사용](https://user-images.githubusercontent.com/113516890/210235490-47ab2ff2-5b1c-437c-9df0-8c69d29d4b4c.png)

#### `/날씨` 명령어 사용
![/날씨 명령어 사용](https://user-images.githubusercontent.com/113516890/210235614-51a4259c-2635-4dae-b11b-030b99352573.png)

### Bug Report
문제 발생 시 반드시 **해당 서버, 채널의 ID, (봇 운영자일 경우)로그와 함께** issue를 작성하거나, [SeoulTechBot 공식 서버](https://discord.gg/wRXRHB7mr6)의 피드백 채널에서 문제를 알려주시기 바랍니다.

---
## Getting Started with My Bot
Discord 봇을 운영하기 위해선 Discord 계정과 [Discord Developers Portal](https://discord.com/developers/)에서 Applications을 만든 후, Bot의 토큰이 필요합니다.
또한 `/날씨` 명령어를 활성화하려면 [오픈 API의 기상청 단기예보 조회서비스](https://www.data.go.kr/data/15084084/openapi.do)에서 인증키를 발급 받아야 합니다.
토큰을 입력하지 않을 경우에도 봇의 실행은 가능하나, 날씨 관련 기능이 비활성화됩니다.

[Discord Developers Portal](https://discord.com/developers/)의 Applications > 내 앱 > OAuth2에서 `application_command`와 `bot`을 체크 후 링크를 생성하여 봇을 초대할 수 있습니다.

```shell
$ git clone https://github.com/hgsanguk/seoultechbot.git
```
git을 사용해 위의 명령어로 원하는 경로에 이 저장소를 clone하여 최신 버전의 코드를 받을 수 있습니다.

### Run with Docker
(작성 중)

### Run Manually
```shell
$ cd seoultechbot
$ pip install -r requirements.txt
```
clone한 저장소로 이동한 다음, 필요한 패키지를 설치합니다. 의존성 충돌 방지를 위해 venv를 활성화한 상태에서 패키지를 설치할 것을 권장합니다.


```shell
$ nohup python3 run.py &
```
백그라운드에서 봇이 실행되며, clone한 저장소 디렉토리의 `data/logs/seoultechbot.log`에서 로그를 확인해볼 수 있습니다.


## License
* 이 프로젝트의 라이센스는 GNU GPL 3.0이며, 자세한 내용은 `LICENSE`를 참고하시기 바랍니다.
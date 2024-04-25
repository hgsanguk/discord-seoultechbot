import os
from seoultechbot import SeoulTechBot

# 봇 실행
if __name__ == "__main__":
    SeoulTechBot().run(os.getenv("STBOT_DISCORD_BOT_TOKEN"), log_handler=None)

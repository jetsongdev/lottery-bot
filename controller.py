import os
import sys
from dotenv import load_dotenv
from typing import Optional

import auth
import lotto645
import win720
import notification
import time


def _setup_and_login():
    load_dotenv(override=True)
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if slack_webhook_url and slack_webhook_url.startswith("YOUR_"):
        slack_webhook_url = None

    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if discord_webhook_url and discord_webhook_url.startswith("YOUR_"):
        discord_webhook_url = None

    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if telegram_bot_token and telegram_bot_token.startswith("YOUR_"):
        telegram_bot_token = None

    telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if telegram_chat_id and telegram_chat_id.startswith("YOUR_"):
        telegram_chat_id = None

    if slack_webhook_url:
        webhook_url = slack_webhook_url
    else:
        webhook_url = discord_webhook_url

    auth_ctrl = auth.AuthController()
    auth_ctrl.login(username, password)

    return auth_ctrl, username, webhook_url, telegram_bot_token, telegram_chat_id

def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(authCtrl, cnt, _mode)
    response['balance'] = authCtrl.get_user_balance()
    return response

def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    item['balance'] = authCtrl.get_user_balance()
    return item

def buy_win720(authCtrl: auth.AuthController, username: str):
    pension = win720.Win720()
    response = pension.buy_Win720(authCtrl, username)
    response['balance'] = authCtrl.get_user_balance()
    return response

def check_winning_win720(authCtrl: auth.AuthController) -> dict:
    pension = win720.Win720()
    item = pension.check_winning(authCtrl)
    item['balance'] = authCtrl.get_user_balance()
    return item

def send_message(mode: int, lottery_type: int, response: dict, webhook_url: Optional[str],
                 telegram_bot_token: Optional[str] = None, telegram_chat_id: Optional[str] = None):
    notify = notification.Notification()

    if mode == 0:
        if lottery_type == 0:
            notify.send_lotto_winning_message(response, webhook_url, telegram_bot_token, telegram_chat_id)
        else:
            notify.send_win720_winning_message(response, webhook_url, telegram_bot_token, telegram_chat_id)
    elif mode == 1:
        if lottery_type == 0:
            notify.send_lotto_buying_message(response, webhook_url, telegram_bot_token, telegram_chat_id)
        else:
            notify.send_win720_buying_message(response, webhook_url, telegram_bot_token, telegram_chat_id)

def check():
    auth_ctrl, _, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = check_winning_lotto645(auth_ctrl)
    send_message(0, 0, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

    time.sleep(10)

    response = check_winning_win720(auth_ctrl)
    send_message(0, 1, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def buy():
    load_dotenv(override=True)
    count = int(os.environ.get('COUNT'))
    mode = "AUTO"

    auth_ctrl, username, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = buy_lotto645(auth_ctrl, count, mode)
    send_message(1, 0, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

    time.sleep(10)

    auth_ctrl.http_client.session.cookies.clear()
    auth_ctrl, username, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = buy_win720(auth_ctrl, username)
    send_message(1, 1, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def lotto_buy():
    load_dotenv(override=True)
    count = int(os.environ.get('COUNT'))
    auth_ctrl, _, webhook_url, tg_token, tg_chat_id = _setup_and_login()
    mode = "AUTO"

    response = buy_lotto645(auth_ctrl, count, mode)
    send_message(1, 0, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def win720_buy():
    auth_ctrl, username, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = buy_win720(auth_ctrl, username)
    send_message(1, 1, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def lotto_check():
    auth_ctrl, _, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = check_winning_lotto645(auth_ctrl)
    send_message(0, 0, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def win720_check():
    auth_ctrl, _, webhook_url, tg_token, tg_chat_id = _setup_and_login()

    response = check_winning_win720(auth_ctrl)
    send_message(0, 1, response=response, webhook_url=webhook_url, telegram_bot_token=tg_token, telegram_chat_id=tg_chat_id)

def run():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    if sys.argv[1] == "buy":
        buy()
    elif sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "buy_lotto":
        lotto_buy()
    elif sys.argv[1] == "buy_win720":
        win720_buy()
    elif sys.argv[1] == "check_lotto":
        lotto_check()
    elif sys.argv[1] == "check_win720":
        win720_check()
  

if __name__ == "__main__":
    run()

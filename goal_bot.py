"""Post a message to Telegram and/or Discord the moment a goal goes in, for
every football match in play.

Usage:
    FIVEDOLLARFOOTBALL_API_KEY=fb_live_... DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/... python goal_bot.py
    FIVEDOLLARFOOTBALL_API_KEY=fb_live_... TELEGRAM_BOT_TOKEN=123:abc TELEGRAM_CHAT_ID=-100123 python goal_bot.py

Environment:
    FIVEDOLLARFOOTBALL_API_KEY   required
    DISCORD_WEBHOOK_URL          a channel webhook address
    TELEGRAM_BOT_TOKEN           a bot token from @BotFather
    TELEGRAM_CHAT_ID             the chat, group or channel to post to
    POLL_SECONDS                 seconds between polls (default 60)

With neither Discord nor Telegram configured the alerts are only printed.
"""

import os
import sys
import time

import requests
from fivedollarfootball import APIError, Client

POLL_SECONDS = int(os.environ.get("POLL_SECONDS", "60"))


def notify(text):
    """Send to whichever of Telegram and Discord is configured."""
    try:
        if os.environ.get("TELEGRAM_BOT_TOKEN"):
            requests.post(
                f'https://api.telegram.org/bot{os.environ["TELEGRAM_BOT_TOKEN"]}/sendMessage',
                json={"chat_id": os.environ["TELEGRAM_CHAT_ID"], "text": text}, timeout=10,
            ).raise_for_status()
        if os.environ.get("DISCORD_WEBHOOK_URL"):
            requests.post(
                os.environ["DISCORD_WEBHOOK_URL"], json={"content": text}, timeout=10,
            ).raise_for_status()
    except requests.RequestException as err:
        # A failed delivery must not stop the bot.
        print(f"could not deliver: {err}", file=sys.stderr, flush=True)
    print(text, flush=True)


def main():
    key = os.environ.get("FIVEDOLLARFOOTBALL_API_KEY")
    if not key:
        sys.exit("Set FIVEDOLLARFOOTBALL_API_KEY. Free keys: https://5dollarfootballapi.com")
    if os.environ.get("TELEGRAM_BOT_TOKEN") and not os.environ.get("TELEGRAM_CHAT_ID"):
        sys.exit("TELEGRAM_BOT_TOKEN is set; set TELEGRAM_CHAT_ID as well.")

    client = Client(key)
    scores = {}  # fixture id -> (home goals, away goals) at the last poll

    while True:
        try:
            # One call: every match in play right now.
            matches = client.fixtures(status="live", per_page=500)
        except APIError as err:
            print(f"API error {err.status_code} {err.code}: {err.message}", file=sys.stderr, flush=True)
            matches = []

        for m in matches:
            score = (m["goals"]["home"] or 0, m["goals"]["away"] or 0)
            before = scores.get(m["id"])
            # The first time a match is seen only sets its baseline.
            if before is not None and sum(score) > sum(before):
                minute = "HT" if m["status_code"] == "half" else f'{m["status_code"]}\''
                notify(f'GOAL {minute}  {m["teams"]["home"]["name"]} {score[0]}-{score[1]} '
                       f'{m["teams"]["away"]["name"]}  ({m["league"]["name"]})')
            scores[m["id"]] = score

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

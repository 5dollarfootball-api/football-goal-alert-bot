# Football goal alert bot for Telegram and Discord (Python)

A message in your Telegram chat or Discord channel the moment a goal goes in, for every football match in play. One file, **one API call a minute**.

Built on the [5DollarFootballAPI](https://5dollarfootballapi.com), a cheap football data API. Runs on the **free plan** (top-5 European leagues, no credit card).

```
GOAL 13'  Al Urooba U21 1-0 Al Dhaid U21  (UAE Youth League)
GOAL 62'  Otrant-Olympic Ulcinj 2-2 OFK Mladost DG  (Montenegro Prva Liga)
GOAL 31'  FC Masar 1-0 El Daklyeh  (Egypt Division 2)
```

See the walkthrough, with sample output: **[5dollarfootballapi.com/examples/goal-alert-bot](https://5dollarfootballapi.com/examples/goal-alert-bot)**

The alerts above came from a run with an Ultra key, which returns every league. A free key returns live matches from the top-5 leagues.

## Run it

1. Get a free API key at [5dollarfootballapi.com](https://5dollarfootballapi.com).
2. Pick where the alerts go (one or both):

   **Discord** — in the channel: *Edit channel → Integrations → Webhooks → New webhook → Copy webhook URL*.

   **Telegram** — message [@BotFather](https://t.me/BotFather), send `/newbot` and keep the token. Add the bot to your chat or channel, send a message there, then open `https://api.telegram.org/bot<token>/getUpdates` and read `chat.id`.

3. Install and run:

```bash
pip install -r requirements.txt

# Discord
FIVEDOLLARFOOTBALL_API_KEY=fb_live_your_key \
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/... \
python goal_bot.py

# Telegram
FIVEDOLLARFOOTBALL_API_KEY=fb_live_your_key \
TELEGRAM_BOT_TOKEN=123456:ABC... TELEGRAM_CHAT_ID=-1001234567890 \
python goal_bot.py
```

With neither configured, the alerts are only printed — handy for a first run. Set `POLL_SECONDS` to change how often it asks (default 60).

## How it works

One request per poll, whatever the number of matches:

| Call | What it returns |
|---|---|
| `GET /v1/fixtures?status=live&per_page=500` | Every match in play right now, with its current score, on one page. |

The bot keeps the score it saw for each match on the previous poll. When the total goes up, it sends an alert. The first time it sees a match it only records the score, so starting the bot mid-match does not replay earlier goals.

Reference: [`/v1/fixtures`](https://5dollarfootballapi.com/docs/fixtures) · [Python client](https://github.com/5dollarfootball-api/football-api-python-sdk)

## Plans and polling

Polling once a minute is 60 requests an hour, which is the free plan's allowance. Pro ($5/mo) covers 130+ competitions at 10 requests a minute, enough to poll every 10 seconds (`POLL_SECONDS=10`); Ultra ($25/mo) covers every league. [Pricing](https://5dollarfootballapi.com/pricing)

## Take it further

- Compare `m["corners"]` the same way to alert on corners, or on a match reaching a corner count.
- Compare `m["cards"]` to alert on red cards.
- Add `include=["events"]` to the call to get the minute of each goal from the match timeline.
- Pass `league=id` to follow one competition only.

## More examples

- [football-live-score-app](https://github.com/5dollarfootball-api/football-live-score-app) — a live scoreboard in one Node.js file
- [football-odds-backtest](https://github.com/5dollarfootball-api/football-odds-backtest) — simple bets settled at opening vs closing odds
- [football-odds-movement-chart](https://github.com/5dollarfootball-api/football-odds-movement-chart) — chart every price move of a match
- [football-corner-stats-table](https://github.com/5dollarfootball-api/football-corner-stats-table) — a league corner table from one call
- [All examples](https://5dollarfootballapi.com/examples)

## License

[MIT](LICENSE). Football data by [5DollarFootballAPI](https://5dollarfootballapi.com).

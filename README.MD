### Telegram bot for tracking personal expenses and budgeting
<br>

You need to set next environment variables:

`TELEGRAM_API_TOKEN` — bot API token

`TELEGRAM_ACCESS_ID` — Telegram account ID from which messages will be received (messages from other accounts are ignored)

`TZ` — your timezone

#### Installation guide
1. Build `Docker` image
```
docker build -t tg_money_saver ./
```
1. Run `Docker` container
```
docker run -d tg_money_saver
```
# Discord Greeting Bot

For greeting

## Tech stack

1. Python

2. Docker

## Docker

0. Make sure you already have docker installed

1. Build docker
```
docker build -t greeting-bot .
```

2. Run docker
```
docker run --rm -e DISCORD_TOKEN=<YOUR_DISCORD_TOKEN> greeting-bot
```

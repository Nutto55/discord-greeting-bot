FROM python:3.12-alpine

WORKDIR /app

ENV DISCORD_TOKEN=$DISCORD_TOKEN
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends ffmpeg

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD [ "python3", "-u", "bot.py"]

import os
from datetime import datetime, timedelta
import dateutil.parser
import discord
import feedparser
from urls import URLS

client = discord.Client()


@client.event
async def on_ready():
    DISCORD_CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID'))
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(f'{client.user} is now active.')

    for url in URLS:
        feed = feedparser.parse(url)
        entries = feed.get('entries')

        for entry in entries:
            published = dateutil.parser.parse(entry.published)

            if datetime.now(published.tzinfo) - timedelta(hours=6) < published:
                title = entry.title
                link = entry.links[0].get('href')
                verbose_published = published.strftime('%d/%m/%Y, %H:%M')
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                await channel.send(f'[{verbose_published}]\n{title}\n{link}')

    await client.close()


client.run(os.environ.get('DISCORD_TOKEN'))

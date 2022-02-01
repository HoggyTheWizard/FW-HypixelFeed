from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
from config import url
import feedparser
import asyncio

blacklisted_words = ["@everyone", "@here"]

last_triggered_id = None


async def main():
    thread_id = last_triggered_id
    while True:
        webhook = DiscordWebhook(url=url, rate_limit_retry=True)
        feed = feedparser.parse("https://hypixel.net/forums/-/index.rss")
        latest_post = feed.entries[0]
        if latest_post["id"] != thread_id:
            thread_id = latest_post["id"]

            embed = DiscordEmbed(color=0x7289da)
            embed.set_author(name="Hypixel - Minecraft Server and Maps")
            embed.set_title(latest_post['title'])
            embed.set_url(latest_post['link'])

            soup = BeautifulSoup(latest_post["summary"], "html.parser")
            text = soup.get_text()

            # filter
            for word in blacklisted_words:
                text.replace(word, "<REDACTED>")

            embed.set_description(text)
            webhook.add_embed(embed)
            webhook.avatar_url = "https://cdn.discordapp.com/attachments/746444509226991686/937884437482455060/" \
                                 "Screenshot_2022-01-15_163712.png"
            webhook.execute()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

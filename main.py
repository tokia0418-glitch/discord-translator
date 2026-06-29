import os
import discord
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from langdetect import detect

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.strip()
    if not text:
        return

    try:
        lang = detect(text)
    except Exception:
        return

    try:
        embed = discord.Embed(title="🌏 Translation")

        if lang == "ja":
            en = GoogleTranslator(source="ja", target="en").translate(text)
            ko = GoogleTranslator(source="ja", target="ko").translate(text)
            embed.add_field(name="🇺🇸 English", value=en, inline=False)
            embed.add_field(name="🇰🇷 한국어", value=ko, inline=False)

        elif lang == "en":
            ja = GoogleTranslator(source="en", target="ja").translate(text)
            ko = GoogleTranslator(source="en", target="ko").translate(text)
            embed.add_field(name="🇯🇵 日本語", value=ja, inline=False)
            embed.add_field(name="🇰🇷 한국어", value=ko, inline=False)

        elif lang == "ko":
            ja = GoogleTranslator(source="ko", target="ja").translate(text)
            en = GoogleTranslator(source="ko", target="en").translate(text)
            embed.add_field(name="🇯🇵 日本語", value=ja, inline=False)
            embed.add_field(name="🇺🇸 English", value=en, inline=False)
        else:
            return

        await message.reply(embed=embed)

    except Exception as e:
        await message.channel.send(f"Translation error: {e}")

client.run(TOKEN)

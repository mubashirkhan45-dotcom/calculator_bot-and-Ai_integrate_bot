import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# =========================
# CALCULATOR COMMANDS
# =========================

@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(f"Result: {a + b}")

@bot.command()
async def sub(ctx, a: float, b: float):
    await ctx.send(f"Result: {a - b}")

@bot.command()
async def mul(ctx, a: float, b: float):
    await ctx.send(f"Result: {a * b}")

@bot.command()
async def div(ctx, a: float, b: float):
    if b == 0:
        await ctx.send("Cannot divide by zero.")
    else:
        await ctx.send(f"Result: {a / b}")

# =========================
# AI COMMAND
# =========================

@bot.command()
async def ai(ctx, *, prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        if len(answer) > 1900:
            answer = answer[:1900]

        await ctx.send(answer)

    except Exception as e:
        await ctx.send(f"Error: {e}")

# =========================
# HELP COMMAND
# =========================

@bot.command()
async def commandslist(ctx):
    embed = discord.Embed(
        title="Calculator + AI Bot",
        color=0x00ff00
    )

    embed.add_field(
        name="Calculator",
        value="""
!add 5 3
!sub 10 2
!mul 4 6
!div 20 5
""",
        inline=False
    )

    embed.add_field(
        name="AI",
        value="""
!ai What is Python?
!ai Write a poem
""",
        inline=False
    )

    await ctx.send(embed=embed)

bot.run(TOKEN)
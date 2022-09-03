import os

from discord import Intents, Game, Message
from discord.ext.commands import CommandNotFound

from modules.vault import get_bot_config

from models.bot_model import CustomBot

prefix = ['a.', 'A.']
bot = CustomBot(
    command_prefix=prefix,
    intents=Intents.all()
)

DISCORD_TOKEN = get_bot_config("DISCORD_TOKEN")


@bot.event
async def on_ready():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension("cogs." + file[:-3])
            print(f'Loaded cog {file}')
    print('Bot is ready!')


@bot.event
async def on_message(message : Message):
    if message.content == f'<@{bot.user.id}>':
        await message.reply(
            f'**Prefix của bot là: `{prefix[0]}` or `{prefix[1]}`\nVà `{prefix[0]}help` để xem các lệnh của bot :)**'
        )
    await bot.process_commands(message)


@bot.event
async def on_command_error(_, error):
    if isinstance(
        error,
        CommandNotFound
    ):
        return
    raise error


async def startup_tasks():
    """
    Run after bot is ready
    """

    await bot.wait_until_ready()

    await bot.change_presence(
        activity=Game(
            name="prefix is a. or A."
        )
    )

bot.setup_hook = startup_tasks

bot.run(DISCORD_TOKEN)
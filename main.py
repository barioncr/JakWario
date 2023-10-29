import discord
from discord import app_commands
import memegenerator
import random

TOKEN = 'MTE2NzQxNjI2NzIyNTk3Mjc4Ng.G_8k0i.cV8DYV-e_DRH9vo2IO4Zw6oXg-YR7pwjJUaTMA'
MY_GUILD = discord.Object(id=880925303332012093)

class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = Bot(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'{client.user} подключился!')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
async def ememe(interaction: discord.Interaction, top_text: str, bottom_text: str):
    memegenerator.make_ememe(top_text, bottom_text)
    send_ememe = discord.File(fp='tempememe.png')
    await interaction.response.send_message(file=send_ememe)


@client.tree.command()
async def viper(interaction: discord.Interaction):
    vipa = discord.File(fp='viper/' + f'({random.randint(1, 905)}).jpg')
    await interaction.response.send_message(file=vipa)


client.run(TOKEN)

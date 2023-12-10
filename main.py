import discord
from discord import app_commands
import memegenerator
from numpy import random


MY_GUILD = discord.Object(id=880925303332012093)


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


bot_intents = discord.Intents.default()
bot_intents.message_content = True
client = Bot(intents=bot_intents)


@client.event
async def on_ready():
    print(f'{client.user} подключился!')


# game_start = False

@client.tree.command()
async def hangman(interaction: discord.Interaction, start: bool, letter: str):
    if start:
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')
        word = random.choice(hangman.words)
    else:
        result, attempts = hangman.check(word, letter)


@client.tree.command(name='ememe', description='A meme using random submitted template.')
async def ememe(interaction: discord.Interaction, top_text: str = '', bottom_text: str = ''):
    memegenerator.make_meme(top_text, bottom_text, 'ememe')
    send_ememe = discord.File(fp='tempememe.png')
    await interaction.response.send_message(file=send_ememe)


@client.tree.command(name='hmeme', description='A meme using random memeshappen template.')
async def hmeme(interaction: discord.Interaction, top_text: str = '', bottom_text: str = ''):
    memegenerator.make_meme(top_text, bottom_text, 'hmeme')
    send_hmeme = discord.File(fp='tempememe.png')
    await interaction.response.send_message(file=send_hmeme)


@client.tree.command(name='skele', description='Badass command.')
async def skele(interaction: discord.Interaction, message: str):
    meme = random.choice(memegenerator.skeletons)
    meme.add_captions(message)
    await interaction.response.send_message(file=discord.File(fp='skeletal.png'))


@client.tree.command(name='submit',
                     description="Submit a template for /ememe.")
async def submit(interaction: discord.Interaction, submission: discord.Attachment):
    allowed = ('jpg', 'jpeg', 'png')
    chk = submission.filename[submission.filename.index('.') + 1:].lower()
    if chk in allowed:
        fname = f'{random.randint(0, 99999)} - {submission.filename}'
        await submission.save(f'ememe/{fname}')
        await interaction.response.send_message(f'Submitted `{fname}` to ememe (stands for Epic Meme)!')
    else:
        await interaction.response.send_message(
            'I appreciate your submissions but if you flood the characters with duplicates '
            'using the same captions I am forced to remove them as it is span as far as I am concerned.')


@client.tree.command()
async def viper(interaction: discord.Interaction):
    vipa = discord.File(fp='viper/' + f'({random.randint(1, 905)}).jpg')
    await interaction.response.send_message(file=vipa)


@client.tree.command(name='join', description='Joins voice to spy on server members')
async def join(interaction: discord.Interaction):
    vc = interaction.user.voice
    if client.voice_clients:
        await interaction.response.send_message('Уже в голосовом канале.')
    elif vc:
        try:
            await vc.channel.connect()
            await interaction.response.send_message(f'Connected to {vc.channel.name}')
        except TimeoutError:
            await interaction.response.send_message('Something went wrong')
    else:
        await interaction.response.send_message(f'{interaction.user.name} is a fake friend (not in voice)')


@client.tree.command()
async def leave(interaction: discord.Interaction):
    if client.voice_clients:
        await client.voice_clients[0].disconnect()
        await interaction.response.send_message(f'Leaving {client.voice_clients[0].channel}')
    else:
        await interaction.response.send_message("I'm not in a voice channel")


if __name__ == '__main__':
    with open('_bot_token') as TOKEN:
        client.run(TOKEN.readline())

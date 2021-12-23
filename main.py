import discord
import json

# Load secrets from secrets.json
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

# Load constant strings from strings.json
with open('strings.json') as strings_file:
    strings = json.load(strings_file)


def get_site_embed(url, name, color, image_url=strings['img-default-site-thumbnail']):
    embed = discord.Embed(
        title=name,
        description=f'[사이트로 이동하기]({url})',
        colour=color
    )
    embed.set_thumbnail(url=image_url)
    return embed


class MainClient(discord.Client):
    async def on_ready(self):
        activity = discord.Activity(name='새나무제', type=discord.ActivityType.playing)
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        if message.author.bot or message.author == client.user:
            return  # Do nothing (Don't reply)

        # Defining to a variable
        message_content = message.content
        channel = message.channel

        # Open site
        if message_content.startswith('새나무 구글'):
            await channel.send(embed=get_site_embed(
                url='https://www.google.com',
                name='Google',
                color=0x347deb,
                image_url=strings['img-google-thumbnail']
            ))


client = MainClient()
client.run(secrets["token"])

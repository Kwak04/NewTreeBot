import discord
import json

# Load secrets from secrets.json
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

# Load constant strings from strings.json
with open('strings.json') as strings_file:
    strings = json.load(strings_file)


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
                url='https://www.google.com/',
                name='Google',
                color=0x4081ec,
                image_url=strings['img-google-thumbnail']
            ))

        if message_content.startswith('새나무 유튜브'):
            await channel.send(embed=get_site_embed(
                url='https://www.youtube.com/',
                name='YouTube',
                color=0xf63731,
                image_url=strings['img-youtube-thumbnail']
            ))

        if message_content.startswith('새나무 네이버'):
            await channel.send(embed=get_site_embed(
                url='https://www.naver.com/',
                name='네이버',
                color=0x03e062,
                image_url=strings['img-naver-thumbnail']
            ))

        if message_content.startswith('새나무 온라인 클래스'):
            await channel.send(embed=get_site_embed(
                url='https://www.ebsoc.co.kr/',
                name='EBS 온라인 클래스',
                color=0xa7cd54,
                image_url=strings['img-ebs-thumbnail']
            ))

        if message_content.startswith('새나무 클래스룸'):
            await channel.send(embed=get_site_embed(
                url='https://classroom.google.com/',
                name='Google Classroom',
                color=0x189c5c,
                image_url=strings['img-classroom-thumbnail']
            ))

        if message_content.startswith('새나무 메가스터디'):
            await channel.send(embed=get_site_embed(
                url='https://www.megastudy.net/',
                name='메가스터디',
                color=0x007ef7,
                image_url=strings['img-megastudy-thumbnail']
            ))


client = MainClient()
client.run(secrets["token"])


def get_site_embed(url, name, color, image_url=strings['img-default-site-thumbnail']):
    embed = discord.Embed(
        title=name,
        description=f'[사이트로 이동하기]({url})',
        colour=color
    )
    embed.set_thumbnail(url=image_url)
    return embed

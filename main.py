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


def log(title, description, user=''):
    if user == '':
        print(f'[{title}] {description}')
    else:
        print(f'{user}: [{title}] {description}')


class MainClient(discord.Client):
    async def on_ready(self):
        activity = discord.Activity(name='새나무제', type=discord.ActivityType.playing)
        await self.change_presence(activity=activity)

        log('NOW ONLINE', f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.author.bot or message.author == client.user:
            return  # Do nothing (Don't reply)

        # Defining to a variable
        message_content = message.content
        channel = message.channel

        # Open site
        if message_content.startswith('새나무 구글'):
            site_name = 'Google'
            await channel.send(embed=get_site_embed(
                url='https://www.google.com/',
                name=site_name,
                color=0x4081ec,
                image_url=strings['img-google-thumbnail']
            ))
            log('사이트 이동', site_name, user=message.author)

        if message_content.startswith('새나무 유튜브'):
            site_name = 'YouTube'
            await channel.send(embed=get_site_embed(
                url='https://www.youtube.com/',
                name=site_name,
                color=0xf63731,
                image_url=strings['img-youtube-thumbnail']
            ))
            log('사이트 이동', site_name, user=message.author)

        if message_content.startswith('새나무 네이버'):
            site_name = '네이버'
            await channel.send(embed=get_site_embed(
                url='https://www.naver.com/',
                name=site_name,
                color=0x03e062,
                image_url=strings['img-naver-thumbnail']
            ))
            log('사이트 이동', site_name, user=message.author)

        if message_content.startswith('새나무 온라인 클래스'):
            site_name = 'EBS 온라인 클래스'
            await channel.send(embed=get_site_embed(
                url='https://www.ebsoc.co.kr/',
                name=site_name,
                color=0xa7cd54,
                image_url=strings['img-ebs-thumbnail']
            ))
            log('사이트 이동', site_name, user=message.author)

        if message_content.startswith('새나무 클래스룸'):
            site_name = 'Google Classroom'
            await channel.send(embed=get_site_embed(
                url='https://classroom.google.com/',
                name=site_name,
                color=0x189c5c,
                image_url=strings['img-classroom-thumbnail']
            ))
            log('사이트 이동', 'YouTube', user=message.author)

        if message_content.startswith('새나무 메가스터디'):
            site_name = '메가스터디'
            await channel.send(embed=get_site_embed(
                url='https://www.megastudy.net/',
                name=site_name,
                color=0x007ef7,
                image_url=strings['img-megastudy-thumbnail']
            ))
            log('사이트 이동', site_name, user=message.author)


client = MainClient()
client.run(secrets["token"])

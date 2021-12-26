import discord
import json
from datetime import datetime
import random

# Load secrets from secrets.json
with open('secrets_beta.json', 'r', encoding='UTF8') as secrets_file:
    secrets = json.load(secrets_file)

# Load constant strings from strings.json
with open('strings.json', 'r', encoding='UTF8') as strings_file:
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


def dump_new_record(data_block, score, user):
    # Write data
    data_block[str(user.id)] = {
        'count': score,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Dump data
    with open('updownscore.json', 'w', encoding='UTF8') as updown_score_file:
        json.dump(data_block, updown_score_file, indent=2, ensure_ascii=False)


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
        message_author = message.author
        channel = message.channel

        # Swear words detector
        # This deletes the original message, and replace it with a spoiler(hidden)  message
        #
        swear_words = ['씨발', '싸발', 'ㅅㅂ', '시발', '좆', 'ㅈ같', '병신', 'ㅄ', 'ㅂㅅ', '쌍', '썅', 'ㅆ', '새끼']
        for word in swear_words:
            if word in message_content:
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    log('ERROR', 'Unable to delete message')
                else:
                    await channel.send(discord.Embed(
                        title='욕설이 감지되었습니다.',
                        description=strings['msg-swear-detector'].format(message),
                        colour=0xff0000  # Red
                    ))
                    log('욕 감지됨', f'감지된 욕: {word}', user=message_author)

        # Current time
        #
        if message_content.startswith('새나무 몇 시') or message_content.startswith('새나무 몇시'):
            current_time = datetime.now()

            await channel.send(embed=discord.Embed(
                title='현재 날짜 및 시간입니다.',
                description=strings['msg-time'].format(current_time),
                colour=0xffe600
            ))
            log('현재 날짜/시각', strings['msg-time-without-line-break'].format(current_time), user=message_author)

        # Open site
        #
        if message_content.startswith('새나무 구글'):
            site_name = 'Google'
            await channel.send(embed=get_site_embed(
                url='https://www.google.com/',
                name=site_name,
                color=0x4081ec,
                image_url=strings['img-google-thumbnail']
            ))
            log('사이트 이동', site_name, user=message_author)

        if message_content.startswith('새나무 유튜브'):
            site_name = 'YouTube'
            await channel.send(embed=get_site_embed(
                url='https://www.youtube.com/',
                name=site_name,
                color=0xf63731,
                image_url=strings['img-youtube-thumbnail']
            ))
            log('사이트 이동', site_name, user=message_author)

        if message_content.startswith('새나무 네이버'):
            site_name = '네이버'
            await channel.send(embed=get_site_embed(
                url='https://www.naver.com/',
                name=site_name,
                color=0x03e062,
                image_url=strings['img-naver-thumbnail']
            ))
            log('사이트 이동', site_name, user=message_author)

        if message_content.startswith('새나무 온라인 클래스'):
            site_name = 'EBS 온라인 클래스'
            await channel.send(embed=get_site_embed(
                url='https://www.ebsoc.co.kr/',
                name=site_name,
                color=0xa7cd54,
                image_url=strings['img-ebs-thumbnail']
            ))
            log('사이트 이동', site_name, user=message_author)

        if message_content.startswith('새나무 클래스룸'):
            site_name = 'Google Classroom'
            await channel.send(embed=get_site_embed(
                url='https://classroom.google.com/',
                name=site_name,
                color=0x189c5c,
                image_url=strings['img-classroom-thumbnail']
            ))
            log('사이트 이동', 'YouTube', user=message_author)

        if message_content.startswith('새나무 메가스터디'):
            site_name = '메가스터디'
            await channel.send(embed=get_site_embed(
                url='https://www.megastudy.net/',
                name=site_name,
                color=0x007ef7,
                image_url=strings['img-megastudy-thumbnail']
            ))
            log('사이트 이동', site_name, user=message_author)

        # UPDOWN game
        #
        if message_content.startswith('새나무 업다운') or message_content.startswith('새나무 UPDOWN'):
            number = random.randint(1, 100)
            guessed_number = 0
            count = 0

            await channel.send(embed=discord.Embed(
                title='UPDOWN 게임을 시작합니다.',
                description='1부터 100 사이의 숫자를 맞춰주세요!',
                colour=0x0dffb6  # Mint
            ))
            log('UPDOWN', f'게임을 시작합니다. | 정답: {number}', user=message_author)

            def check(m):
                return m.author == message_author and m.content.isdigit()

            while guessed_number != number:  # Until the guess is right
                answer = await self.wait_for('message', check=check)
                guessed_number = int(answer.content)
                count += 1

                # Basic condition check
                if not (1 <= guessed_number <= 100):
                    await channel.send(embed=discord.Embed(
                        title='1부터 100까지의 수만 입력하실 수 있습니다.',
                        description='수를 다시 입력해 주세요.',
                        colour=0xff0000  # Red
                    ))

                # UP
                elif guessed_number < number:
                    await channel.send(embed=discord.Embed(
                        title='UP!',
                        description='정답은 입력하신 숫자보다 큽니다!',
                        colour=0xff7c2b  # Brown
                    ))
                    log('UPDOWN', f'Up!   | {guessed_number} < {number}', user=message_author)

                # DOWN
                elif guessed_number > number:
                    await channel.send(embed=discord.Embed(
                        title='DOWN!',
                        description='정답은 입력하신 숫자보다 작습니다!',
                        colour=0xff7c2b  # Brown
                    ))
                    log('UPDOWN', f'Down! | {guessed_number} > {number}', user=message_author)

            # GAME OVER

            # Load updownscore.json
            with open('updownscore.json', 'r', encoding='UTF8') as updown_score_file:
                my_updown_score = json.load(updown_score_file)

            # Check if this is a new record
            try:
                previous_count_record = my_updown_score[str(message_author.id)]['count']
            except KeyError:  # Previous record is not existing, so it becomes your first new record!
                dump_new_record(my_updown_score, count, message_author)
            else:
                if previous_count_record <= count:  # Less is more :) (exceptionally in this game)
                    pass  # Not your new record, so do nothing
                else:  # This is your new record!!!
                    dump_new_record(my_updown_score, count, message_author)

            await channel.send(embed=discord.Embed(
                title='맞추셨습니다!',
                description=f'시도 횟수: {count}',
                colour=0x0dff62  # Green
            ))
            log('UPDOWN', f'게임이 종료되었습니다. | 시도 횟수: {count}', user=message_author)

        # Check my score
        if message_content.startswith('새나무 내 점수') or message_content.startswith('새나무 내 기록'):
            # Check if the author has a nickname
            author_name = message_author.nick
            if author_name is None:
                author_name = message_author.name

            with open('updownscore.json', 'r', encoding='UTF8') as updown_score_file:
                my_updown_score = json.load(updown_score_file)[str(message_author.id)]
                try:
                    my_count = my_updown_score['count']
                    my_date = my_updown_score['date']
                except KeyError:
                    await channel.send(embed=discord.Embed(
                        title=f'{author_name}님의 플레이 기록이 없습니다.',
                        description='이번 기회에 한번 도전해 보시는 건 어떨까요?',
                        colour=0xff0000  # Red
                    ))
                    log('업다운 점수 확인', '플레이 기록 없음', user=message_author)
                else:
                    await channel.send(embed=discord.Embed(
                        title=f'{author_name}님의 최고 기록!',
                        description=f'총 {my_count}번 만에 수를 맞추셨습니다.\n({my_date}에 경신됨)',
                        colour=0x4287f5  # Blue
                    ))
                    log('업다운 점수 확인', f'최고 기록: {my_count}', user=message_author)

        # Check out the highest score in the server
        if message_content.startswith('새나무 랭킹'):
            with open('updownscore.json', 'r', encoding='UTF8') as updown_score_file:
                updown_scores = json.load(updown_score_file)

            scores_list = list()
            highest_score_people_list = list()  # Consisted of user_ids

            for user_id in updown_scores:
                scores_list.append(updown_scores[user_id]['count'])

            highest_score = min(scores_list)  # Less is more

            for user_id in updown_scores:
                if updown_scores[user_id]['count'] == highest_score:
                    highest_score_people_list.append(user_id)

            highest_score_people_string = ''
            for highest_score_people in highest_score_people_list:
                highest_score_people_string += f'<@{highest_score_people}> '

            await channel.send(embed=discord.Embed(
                title='현재 전체 최고 기록입니다.',
                description=strings['msg-ranking-updown'].format(highest_score, highest_score_people_string),
                colour=0x4287f5
            ))
            log('업다운 랭킹 확인', strings['msg-ranking-updown'].format(highest_score, highest_score_people_string),
                user=message_author)


client = MainClient()
client.run(secrets['token'])

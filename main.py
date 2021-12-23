import discord
import json

# Load secrets from secrets.json
with open('secrets.json') as secrets_file:
    secrets = json.load(secrets_file)


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


client = MainClient()
client.run(secrets["token"])

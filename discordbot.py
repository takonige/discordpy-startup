import asyncio

import discord
import youtube_dl

from discord.ext import commands
#この辺は何やってるかわからないけどそのまま引用
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


bot = commands.Bot(command_prefix=commands.when_mentioned_or("_"),
                   description='Relatively simple music bot example')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
#この辺は何やってるかわからないけどそのまま引用ここまで

@bot.event
async def on_message(message):

    if message.content.startswith("_p "):
        await message.author.voice.channel.connect()#vc接続
        message.content=message.content.replace("_p ","")
        async with message.channel.typing():
            player = await YTDLSource.from_url(message.content, loop=asyncio.get_event_loop())#多分再生用の素材を作ってるとこ
            message.author.guild.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)#再生してるとこ
            await message.channel.send('Now playing: {}'.format(player.title))  #再生中のタイトルをsend

    if message.content.startswith("_dis"):
        await message.author.guild.voice_client.disconnect()  #VC切断


bot.run("TOKEN")

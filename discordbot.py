from discord.ext import commands
import os
import traceback
import youtube_dl

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_ready:
    await ctx.send(now_rdy)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)

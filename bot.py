import discord
from time import monotonic
from discord.ext import commands
import DiscordUtils

client = commands.Bot(command_prefix='?', intents = discord.Intents.all())
token = "TOKEN"
music = DiscordUtils.Music()
color_em = discord.Colour.random()

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))  

@client.command()
async def ping(ctx):
    before = monotonic()
    message = await ctx.send("Pong!")
    ping = (monotonic() - before) * 100
    embed = discord.Embed(title=f'Pong! `{int(ping)}ms`', color=color_em)
    await message.edit(embed = embed)

@client.command(aliases=['j'])
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        embed = discord.Embed(title="Lu gada di voice channel bro!", color=color_em)
        return await ctx.send(embed=embed)     
    await ctx.author.voice.channel.connect()
    embed = discord.Embed(title='Udah masuk bro!',color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['l', 'dc'])
async def leave(ctx):
    voicetrue = ctx.author.voice
    voicetrue_me = ctx.guild.me.voice
    if voicetrue is None:
        embed = discord.Embed(title="Lu gada di voice channel bro!", color=color_em)
        return await ctx.send(embed=embed)
    if voicetrue_me is None:
        embed = discord.Embed(title="Gw lagi gada di voice channel bro!", color=color_em)
        return await ctx.send(embed=embed)
    await ctx.voice_client.disconnect()   
    embed = discord.Embed(title='Udah keluar bro!', color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['p'])
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        embed = discord.Embed(title=f"Mainkan - `{song.name}`", color=color_em)
        await ctx.send(embed=embed)
    else:
        song = await player.queue(url, search=True)
        embed = discord.Embed(title=f"`{song.name}` - Di tambahkan ke queue", color=color_em)
        await ctx.send(embed=embed)

@client.command(aliases=['q'])
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    embed = discord.Embed(title=f"{', '.join([song.name for song in player.current_queue()])}", color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    embed = discord.Embed(title=f"Dijeda - {song.name}", color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    embed = discord.Embed(title=f"Dilanjut - {song.name}", color=color_em)
    await ctx.send(embed=embed)


@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.skip()
    embed = discord.Embed(title=f"Dilanjut - {song.name}", color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        embed = discord.Embed(title=f'Dilooping - {song.name}', color=color_em)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Gak looping - {song.name}', color=color_em)
        await ctx.send(embed=embed)

@client.command(aliases=['np'])
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    embed = discord.Embed(title=f"Lagu yg sedang di putar - {song.name}", color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['rm'])
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    embed = discord.Embed(title=f"Diremove - {song.name} dari queue", color=color_em)
    await ctx.send(embed=embed)

client.run(token)

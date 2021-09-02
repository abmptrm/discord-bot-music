import discord
from time import monotonic
from discord.ext import commands
import DiscordUtils

client = commands.Bot(command_prefix='?', intents = discord.Intents.all())
client.remove_command('help')
token = "token"
music = DiscordUtils.Music()
color_em = discord.Colour.random()

@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )  

#=====================HELP COMMAND============================#


play_music = ['play', 'p','stop', 'pause', 'resume', 'queue', 'q', 'ping', 'join', 'j', 'leave', 'dc', 'skip', 'loop', 'nowplaying', 'np', 'remove', 'rm', 'help']
description = ['[BOT MUSIC]', 'prefix = ?']

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Command RickyGanteng Bot", description=f"`{description[0]}` `{description[1]}`", color=color_em)
    embed.set_author(name="RickyGanteng Bot", icon_url="https://cdn.discordapp.com/attachments/772834462513889312/877816016388911104/Ao53q5X4_tcdSxq32_81hbk_sNGuJ9VQaczu2iOGTb1vXDH9cWxcTt6-20OITxIvgKDYG6r4qVl0vdkYkG1rFwtkfazlJ59DezYR.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/772834462513889312/877816016388911104/Ao53q5X4_tcdSxq32_81hbk_sNGuJ9VQaczu2iOGTb1vXDH9cWxcTt6-20OITxIvgKDYG6r4qVl0vdkYkG1rFwtkfazlJ59DezYR.png")
    embed.add_field(name="JOIN", value="`?join`  atau  `?j`  atau  `?connect`", inline=False)
    embed.add_field(name="PLAY", value="`?play <nama music>`  atau  `?p <nama music>`", inline=False)
    embed.add_field(name="PAUSE", value="`?pause`", inline=False)
    embed.add_field(name="RESUME", value="`?resume`", inline=False)
    embed.add_field(name="STOP", value="`?stop`", inline=False)
    embed.add_field(name="QUEUE", value="`?queue`  atau  `?q`", inline=False)
    embed.add_field(name="VOLUME", value="`?volume <angka>`  atau  `?vol <angka>`", inline=False)
    embed.add_field(name="NOW PLAYING", value="`?nowplaying`  atau  `?np`", inline=False)
    embed.add_field(name="REMOVE", value="`?remove <angka>`  atau  `?rm <angka>`", inline=False)
    embed.add_field(name="LEAVE", value="`?leave`  atau  `?l`  atau  `?dc`  atau  `?disconnect`", inline=False)
    await ctx.send(embed=embed)

#=====================MUSIC COMMAND============================#

@client.command()
async def ping(ctx):
    before = monotonic()
    message = await ctx.send("Pong!")
    ping = (monotonic() - before) * 100
    embed = discord.Embed(title=f'Pong! `{int(ping)}ms`', color=color_em)
    await message.edit(embed = embed)

@client.command(aliases=['j', 'connect'])
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        embed = discord.Embed(title="Lu gada di voice channel bro!", color=color_em)
        return await ctx.send(embed=embed)     
    await ctx.author.voice.channel.connect()
    embed = discord.Embed(title='Udah masuk bro!',color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['l', 'dc', 'disconnect'])
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
        embed = discord.Embed(title="Mainkan", description=f'`{song.name}`', color=color_em)
        await ctx.send(embed=embed)
    else:
        song = await player.queue(url, search=True)
        embed = discord.Embed(title=f"Di tambahkan ke queue", description=f'`{song.name}`', color=color_em)
        await ctx.send(embed=embed)

@client.command(aliases=['q'])
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    embed = discord.Embed(description=f"{' ==#== '.join([song.name for song in player.current_queue()])}", color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    embed = discord.Embed(title=f"Dijeda", description=f'`{song.name}`', color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    embed = discord.Embed(title=f"Dilanjut  {song.name}", color=color_em)
    await ctx.send(embed=embed)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        embed = discord.Embed(title=f"Dilanjut dari",  description=f'`{data[1].name}`', color=color_em)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Dilanjut ', description=f'`{data[0].name}`', color=color_em)
        await ctx.send(embed=embed)

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        embed = discord.Embed(title=f'Dilooping',  description=f'`{song.name}`', color=color_em)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Gak looping  {song.name}', color=color_em)
        await ctx.send(embed=embed)

@client.command(aliases=['np'])
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    embed = discord.Embed(title=f"Lagu yg sedang di putar",  description=f'`{song.name}`', color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['rm'])
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    embed = discord.Embed(title=f"Diremove dari queue",description=f" `{song.name}` ", color=color_em)
    await ctx.send(embed=embed)

@client.command(aliases=['vol'])
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) 
    embed = discord.Embed(title='Volume diganti', description=f'`{song.name}`  ke  `{volume*100}%`', color=color_em)
    # await ctx.send(f"Changed volume for {song.name} to {volume*100}%")
    await ctx.send(embed=embed)

client.run(token)

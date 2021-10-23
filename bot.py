import discord
from discord import Embed as embed
from discord import Colour as color
from discord.ext import commands
import DiscordUtils 
from time import sleep
from time import monotonic

bot = commands.Bot(command_prefix="?", intents = discord.Intents.all(), help_command=None)
token = "TOKEN"
music = DiscordUtils.Music()

@bot.event 
async def on_ready():
    print("Bot Ready {0.user}".format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="?help 🎸"))

@bot.command(pass_context=True)
async def help(ctx):
    emd = embed(title="🎸 **Bot Command** 🎸", description="**PREFIX** = ` ? `", color=color.random())
    emd.set_thumbnail(url="Your Photo")
    emd.add_field(name="**•** Music (18)", value="`join`, `leave`, `dc`, `play`, `p`, `pause`, `resume`, `stop`, `loop`, `queue`, `q`, `nowplaying`, `np`, `skip`, `volume`, `vol`, `remove`, `rm`", inline=False)
    emd.add_field(name="**•** Utils (2)", value="`invite`, `ping`", inline=False)
    await ctx.send(embed=emd)

@bot.command()
async def invite(ctx):
    message = await ctx.send("Thanks!")
    emd = embed(title="Bot 🤖", description="[**Click here!**]("LINK INVITE BOT")", color=color.random())
    await message.edit(embed= emd)
    await message.add_reaction("🎉")

@bot.command()
async def ping(ctx):
    before = monotonic()
    message = await ctx.send("Pong!")
    ping = (monotonic() - before) * 100
    emd = embed(title=f'📡 Pong! `{int(ping)}ms`', color=color.random())
    await message.edit(embed = emd)
    await message.add_reaction("📡")

@bot.command()
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        embed = discord.Embed(title="⛔ You are not connected to the voice channel", color=color.random())
        return await ctx.send(embed=embed)  
    await ctx.author.voice.channel.connect()
    embed = discord.Embed(title='Joined ✅',color=color.random())
    await ctx.send(embed=embed)
    
@bot.command(name="leave", aliases=["dc"])
async def leave(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()

    voicetrue = ctx.author.voice
    voicetrue_me = ctx.guild.me.voice
    if voicetrue is None:
        embed = discord.Embed(title="⛔ You are not connected to the voice channel !", color=color.random())
        return await ctx.send(embed=embed)
    if voicetrue_me is None:
        embed = discord.Embed(title="I'm not on to voice channel", color=color.random())
        return await ctx.send(embed=embed)
    await bot.voice_clients[0].disconnect()   
    embed = discord.Embed(title='Leave ✅', color=color.random())
    await ctx.send(embed=embed)

    sleep(1.0)
    await bot.voice_clients.disconnect()

@bot.command(name="play", aliases=["p"])
async def play(ctx, *, url):

    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        emd = embed(title=f"Playing `{song.name}`")
        await ctx.send(embed=emd)
    else:
        song = await player.queue(url, search=True)
        emd = embed(title=f"Queued `{song.name}`")
        await ctx.send(embed=emd)
        
        
@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    emd = embed(title=f"Paused `{song.name}`")
    await ctx.send(embed=emd)
    # await ctx.send(f"Paused {song.name}")
    
@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    emd = embed(title=f"Resumed `{song.name}`")
    await ctx.send(embed=emd)
    # await ctx.send(f"Resumed {song.name}")
    
@bot.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song =  player.stop()
    emd = embed(title=f"Stopped `{song.name}`")
    await ctx.send(embed=emd)
    # await ctx.send("Stopped")
    
@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        emd = embed(title=f"Enabled loop for `{song.name}`")
        await ctx.send(embed=emd)
        # await ctx.send(f"Enabled loop for {song.name}")
    else:
        emd = embed(title=f"Disabled loop for `{song.name}`")
        await ctx.send(embed=emd)
        # await ctx.send(f"Disabled loop for {song.name}")
    
@bot.command(name="queue", aliases=["q"])
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    nl = ")` \n **•** `(".join([song.name for song in player.current_queue()])
    bc = "\n"
    ti = "**•**"
    emd = embed(title="Queue", description=f"{ti} `({nl})`{bc}")
    await ctx.send(embed=emd)
    # await ctx.send(f"`({')`\n `('.join([song.name for song in player.current_queue()])})`\n")
    
@bot.command(name="nowplaying", aliases=["np"])
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    emd = embed(title=f"Now Playing `{song.name}`")
    await ctx.send(embed=emd)
    # await ctx.send(song.name)
    
@bot.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        emd = embed(title=f"Skipped from `{data[0].name}`")
        await ctx.send(embed=emd)
        # await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        emd = embed(title=f"Skipped `{data[0].name}`")
        await ctx.send(embed=emd)
        # await ctx.send(f"Skipped {data[0].name}")

@bot.command(name="volume", aliases=["vol"])
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) 
    emd = embed(title=f"Changed volume for `{song.name}` to `{volume*100}%`")
    await ctx.send(embed=emd)
    # await ctx.send(f"Changed volume for {song.name} to {volume*100}%")
    
@bot.command(name="remove", aliases=["rm"])
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    emd = embed(title=f"Removed `{song.name}` from queue")
    await ctx.send(embed=emd)
    # await ctx.send(f"Removed {song.name} from queue")



bot.run(token)

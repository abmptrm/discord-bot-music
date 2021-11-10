import discord
from discord import player
import discordSuperUtils
from time import monotonic
from time import sleep
from discord.ext import commands
from discord import Embed as embed
from discord import Colour as color
from discordSuperUtils import MusicManager


client_id = "8c4b6ca346d749d0a065d768f2fdf4fb"
client_secret = "53734343746a4b47b12991f95f021813"

bot = commands.Bot(command_prefix="?", help_command=None)
MusicManager = MusicManager(bot, client_id=client_id,
                                  client_secret=client_secret, spotify_support=True)

# help_command=None

# MusicManager = MusicManager(bot, client_id=client_id,
#                                   client_secret=client_secret, spotify_support=True)

# if using spotify support use this instead ^^^


@MusicManager.event()
async def on_music_error(ctx, error):
    raise error  # add your error handling here! Errors are listed in the documentation.


@MusicManager.event()
async def on_queue_end(ctx):
    print(f"The queue has ended in {ctx}")
    # You could wait and check activity, etc...


@MusicManager.event()
async def on_inactivity_disconnect(ctx):
    print(f"I have left {ctx} due to inactivity..")


@MusicManager.event()
async def on_play(ctx, player):
    # await ctx.send(f"Playing {player}")
    emds = embed(description=f"🎶**Playing**  `{player}`", color=color.random())
    emds.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    message = await ctx.send(embed=emds)
    await message.add_reaction("🎸")


@bot.event
async def on_ready():
    # database = discordSuperUtils.DatabaseManager.connect(...)
    # await MusicManager.connect_to_database(database, ["playlists"])

    print(f"{bot.user} is ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="?help 🎸"))

@bot.command(pass_context=True)
async def help(ctx):
    emd = embed(title="🎸 **Bot Command** 🎸", description="**PREFIX** = ` ? `", color=color.random())
    emd.add_field(name="**•** Music (15)", value="(`join`), (`leave`, `dc`), (`play`, `p`), (`pause`), (`resume`), (`loop`), (`loopstatus`, `ls`), (`queueloop`, `ql`), (`queue`, `q`), (`nowplaying`, `np`), (`skip`), (`volume`, `vol`), (`shuffle`), (`rewind`), ", inline=False)
    emd.add_field(name="**•** Utils (3)", value="(`help`), (`invite`), (`ping`)", inline=False)
    await ctx.send(embed=emd)

@bot.command()
async def invite(ctx):
    message = await ctx.send("Thanks!")
    emd = embed(title="Invite Ricktify 🎸", description="[**Click here!**](https://discord.com/api/oauth2/authorize?client_id=878538776564088832&permissions=8&scope=bot)", color=color.random())
    await message.edit(embed= emd)
    await message.add_reaction("🎉")

@bot.command()
async def ping(ctx):
    before = monotonic()
    message = await ctx.send("Pong!")
    ping = (monotonic() - before) * 100
    emd = embed(description=f"📡 Pong! `{int(ping)}ms`", color=color.random())
    emd.set_footer(text=f"Requested by {message.author.name}", icon_url=ctx.author.avatar_url)
    await message.edit(embed = emd)
    await message.add_reaction("📡")


@bot.command(aliases=["dc"])
async def leave(ctx):
    if await MusicManager.leave(ctx):
        # await ctx.send("Left Voice Channel")
        emd = embed(description="Disconnected", color=color.random())
        message = await ctx.send(embed=emd)
        await message.add_reaction("✅")


@bot.command(aliases=["nowplaying"])
async def np(ctx):
    if player := await MusicManager.now_playing(ctx):
        duration_played = await MusicManager.get_player_played_duration(ctx, player)
        # You can format it, of course.

        # await ctx.send(
        #     f"Currently playing: {player}, \n"
        #     f"Duration: {duration_played}/{player.duration}"
        # )
        
        emd = embed(description=f"**Now Playing** \n🎶Playing : `{player}`\nDuration : {duration_played}/{player.duration}", color=color.random())
        message = await ctx.send(embed=emd)
        await message.add_reaction("🎸")


@bot.command()
async def join(ctx):
    if await MusicManager.join(ctx):
        # await ctx.send("Joined Voice Channel")
        emd = embed(description="Connected", color=color.random())
        message = await ctx.send(embed=emd)
        await message.add_reaction("✅")

@bot.command(aliases=["p"])
async def play(ctx, *, query: str):
    if not ctx.voice_client or not ctx.voice_client.is_connected():
        await MusicManager.join(ctx)

    async with ctx.typing():
        players = await MusicManager.create_player(query, ctx.author)

    if players:
        if await MusicManager.queue_add(players=players, ctx=ctx) and not await MusicManager.play(ctx):
            emd = embed(description="🎸 Added to queue", color=color.random())
            emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🎸")
            # await ctx.send("Added to queue")

    else:
        await ctx.send("Query not found.")


@bot.command()
async def lyrics(ctx, query: str = None):
    if response := await MusicManager.lyrics(ctx, query):
        title, author, query_lyrics = response

        splitted = query_lyrics.split("\n")
        res = []
        current = ""
        for i, split in enumerate(splitted):
            if len(splitted) <= i + 1 or len(current) + len(splitted[i + 1]) > 1024:
                res.append(current)
                current = ""
                continue
            current += split + "\n"

        page_manager = discordSuperUtils.PageManager(
            ctx,
            [
                embed(
                    # title=f"{title}** by **{author}",
                    # description=x, color=color.random()
                    description=f"**{title}** by **{author}**\n\n{x}",color=color.random()
                ).add_field(name=f"(Page {i + 1}/{len(res)})", value="**>>**").set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

                for i, x in enumerate(res)
            ],
            public=True,
        )
        await page_manager.run()

        
    else:
        # await ctx.send("No lyrics found.")
        emds = embed(description="⛔ No lyrics found.", color=color.red())
        # emds.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=emds)
        await message.add_reaction("⛔")


@bot.command()
async def pause(ctx):
    if await MusicManager.pause(ctx):
        # await ctx.send("Player paused.")
        emd = embed(description=f"🎶 **Paused**", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=emd)
        await message.add_reaction("⏸️")


@bot.command()
async def resume(ctx):
    if await MusicManager.resume(ctx):
        # await ctx.send("Player resumed.")
        emd = embed(description=f"🎶 **Resumed**", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=emd)
        await message.add_reaction("▶️")

@bot.command(aliases=["vol"])
async def volume(ctx, volume: int):
    await MusicManager.volume(ctx, volume)
    emd = embed(description=f"🎶 **Volume** : {volume}", color=color.random())
    emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    message = await ctx.send(embed=emd)
    await message.add_reaction("🔊")


@bot.command()
async def loop(ctx):
    is_loop = await MusicManager.loop(ctx)

    if is_loop is not None:
        # await ctx.send(f"Looping toggled to {is_loop}")
        emd = embed(description=f"🎶 **Looping toggled to** {is_loop}", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=emd)
        await message.add_reaction("🔁")


@bot.command()
async def shuffle(ctx):
    is_shuffle = await MusicManager.shuffle(ctx)

    if is_shuffle is not None:
        # await ctx.send(f"Shuffle toggled to {is_shuffle}")
        emd = embed(description=f"🎶 **Shuffle toggled to** {is_shuffle}", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=emd) 
        await msg.add_reaction("🔀")


@bot.command()
async def autoplay(ctx):
    is_autoplay = await MusicManager.autoplay(ctx)

    if is_autoplay is not None:
        # await ctx.send(f"Autoplay toggled to {is_autoplay}")
        emd = embed(description=f"Autoplay toggled to {is_autoplay}", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emd)
        


@bot.command(aliases=["ql"])
async def queueloop(ctx):
    is_loop = await MusicManager.queueloop(ctx)

    if is_loop is not None:
        # await ctx.send(f"Queue looping toggled to {is_loop}")
        emd = embed(description=f"Queue looping toggled to {is_loop}", color=color.random())
        emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=emd)
        await message.add_reaction("🔁")

@bot.command()
async def skip(ctx, index: int = None):
    await MusicManager.skip(ctx, index)

@bot.command(aliases=["q"])
async def queue(ctx):
    if ctx_queue := await MusicManager.get_queue(ctx):
        
        formatted_queue = [
            # f"`{x.title}` **>** {x.requester and x.requester.mention}"
            f"{x.title}"
            for x in ctx_queue.queue[ctx_queue.pos + 1 :]
        ]

        embeds = discordSuperUtils.generate_embeds(
            formatted_queue,
            "Queue",
            f"`Now Playing` **:** `{await MusicManager.now_playing(ctx)}`",
            25,
            string_format="{}",
        )
        # embeds.

        page_manager = discordSuperUtils.PageManager(ctx, embeds, public=True)
        await page_manager.run()


@bot.command()
async def rewind(ctx, index: int = None):
    await MusicManager.previous(ctx, index, no_autoplay=True)
    emd = embed(description="**Rewind**", color=color.random())
    emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    message = await ctx.send(embed=emd)
    await message.add_reaction("🔂")


@bot.command(aliases=["loopstatus"])
async def ls(ctx):
    if queue := await MusicManager.get_queue(ctx):
        loop = queue.loop
        loop_status = None

        if loop == discordSuperUtils.Loops.LOOP:
            loop_status = "Looping enabled."

        elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
            loop_status = "Queue looping enabled."

        elif loop == discordSuperUtils.Loops.NO_LOOP:
            loop_status = "No loop enabled."

        if loop_status:
            # await ctx.send(loop_status)
            emd = embed(description=f"{loop_status}", color=color.random())
            emd.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🔁")


bot.run("TOKEN")

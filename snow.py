import discord
import random
from discord.ext import commands
from discord import app_commands
import aiohttp
import aiosqlite
from easy_pil import *
import asyncio
from aiohttp import web
import io

intents = discord.Intents.all()
TOKEN = ""
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.db: aiosqlite.Connection

async def get_r34(query: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=50&{query}&json=1") as resp:
            return random.choice(await resp.json())['file_url']

@bot.event
async def on_message(message):
     if message.author == bot.user:
         return
     if message.content.startswith("hi"):
         await message.channel.send("Shut up faggot")
     if message.content.startswith("avery"):
         await message.channel.send("Kobashi is the fucking GOAT")
     if message.content.startswith("meow"):
         await message.channel.send("nya~")
     if message.content.startswith("nerd emoji"):
         emoji = '🤓'
         await message.add_reaction(emoji)
     if message.content.startswith("GFY"):
        emoji = '<:GOFUCKYOURSELF:1078324546773463060>'
        await message.add_reaction(emoji)
     author = message.author
     guild = message.guild
     async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        level = await cursor.fetchone()
        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))
            await bot.db.commit()
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        if level < 5:
            xp += random.randint(1, 5)
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        else:
            rand = random.randint(1,(level//4))
            if rand == 1:
                xp += random.randint(1, 5)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        if xp >= 100:
            level = level + 1
            await cursor.execute("SELECT role FROM roles WHERE guild = ? AND level = ?", (message.guild.id, level))
            role = await cursor.fetchone()
            await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
            if role:
                role = message.guild.get_role(role[0])
                await message.author.add_roles(role)
                await message.channel.send(f"{message.author} has received the {role.name} role")
            #if role:
                #role = role[0]
                #role = guild.get_role(role)
                #try:
                    #await author.add_roles(role)
                    #await message.channel.send(f"{author.mention} has gayed to level **level** {level} and earned {role.name}")
                #except discord.HTTPException:
                    #await message.channel.send(f"{author.mention} has gayed to faggot level {level} (cant get gayer)")
            await message.channel.send(f"{author.mention} has gayed to faggot level {level}")
     await bot.db.commit()
     if message.author.bot: return
     content = message.content.lower()
     #if "snow" in content:
         #await bot.get_user(180124680647213056).send(f"{message.author} said {message.content}")

     await bot.process_commands(message)
    #easy call and response code, + level system(broke)

@bot.command(aliases=['lb'])
async def leaderboard(ctx: commands.Context):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC", (ctx.guild.id,))
        data = await cursor.fetchall()
        data_str = ""
        c = 0
        for i in data:
            data_str += f"{c + 1}. **{ctx.guild.get_member(i[2])}** - Level {i[0]} | {i[1]} XP\n"
            if c == 9:
                break
            c += 1

        embed = discord.Embed(title=f"Leaderboard for {ctx.guild.name}", description=data_str)
        await ctx.send(embed=embed)

@bot.command(aliases=['lvl', 'rank', 'r'])
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id), )
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id), )
        level = await cursor.fetchone()
        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
            await bot.db.commit()
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        user_data = {
        "name": f"{member.name}#{member.discriminator}",
        "xp": xp,
        "level": level,
        "next_level_xp": 100,
        "percentage": xp,}

        background = Editor(Canvas((900, 300), color ="#07e6f7"))
        profile_picture = await load_image_async(str(member.avatar.url))
        profile = Editor(profile_picture).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, color="#070606")
        background.paste(profile, (30, 30))

        background.rectangle((30, 220), width = 650, height = 40, color ="#ffffff")
        background.bar((30,220), max_width= 650, height = 40, percentage=user_data["percentage"], color="#e60d0d", radius = 20,)
        background.text((200,40), user_data["name"], font=poppins, color ="#ffffff")

        background.rectangle((200,100), width = 350, height= 2, fill ="#ffffff")
        background.text(
            (200,130),
            f"Level - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}",
            font = poppins_small,
            color = "#ffffff",)

        file = discord.File(fp=background.image_bytes, filename="levelcard.png")
        await ctx.send(file=file)

@bot.command()
async def rewards(ctx):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT levelsys FROM")

@bot.event
async def on_ready():
    setattr(bot, "db", await aiosqlite.connect('level.db'))
    async with bot.db.cursor() as cursor:
        await cursor.execute("CREATE TABLE IF NOT EXISTS levels(level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS levelsettings(levelsys BOOL, role INTEGER, levelreq INTEGER, guild INTEGER)")
        await cursor.execute("CREATE TABLE IF NOT EXISTS roles(role INTEGER, guild INTEGER, level INTEGER)")
        await bot.db.commit()
    try:
        synced = await bot.tree.sync()
        print(f"Synced{len(synced)} command(s)")
    except Exception as e:
        print(e)
    #message for when bot boots up to confirm its working
@bot.tree.command(name="shut")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"shut up {interaction.user.mention}")
#slash command 1

@bot.tree.command(name="parrot")
@app_commands.describe(thing_to_say = "Post ur message here")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(thing_to_say)
#slash command 2

@bot.command()
async def addrole(ctx: commands.Context, role: discord.Role, level: int):
    async with bot.db.cursor() as cursor:
        await cursor.execute("INSERT INTO roles (role, guild, level) VALUES (?, ?, ?)", (role.id, ctx.guild.id, level))
    await bot.db.commit()
    await ctx.send("done")

@bot.command()
async def gayrr(ctx: commands.Context):
    if not ctx.channel.is_nsfw():
        return await ctx.send('use in an nsfw channel')
    num = random.randint(1, 6)
    if num != 6:
        return await ctx.send("you got lucky this time...")
    img = await get_r34("tags=femboy+anal")
    await ctx.send(img)

@bot.command()
async def straightrr(ctx: commands.Context):
    if not ctx.channel.is_nsfw():
        return await ctx.send('use in an nsfw channel')
    num = random.randint(1, 6)
    if num != 6:
        return await ctx.send("you got lucky this time...")
    img = await get_r34("tags=straight")
    await ctx.send(img)

@bot.command()
async def rule34(ctx: commands.Context):
    if not ctx.channel.is_nsfw():
        return await ctx.send('use in an nsfw channel')
    img = await get_r34("tags=straight")
    await ctx.send(img)

@bot.command()
async def rule34gay(ctx: commands.Context):
    if not ctx.channel.is_nsfw():
        return await ctx.send('use in an nsfw channel')
    img = await get_r34("tags=femboy+anal")
    await ctx.send(img)

@bot.command()
async def roll(ctx):
    await ctx.send(random.randint(1,69))

@bot.command()
async def blossom(ctx):
    await ctx.send('Blossom got caught with a choker lol')
#replies with a string that is defined in the send

@bot.command()
async def lesbeon(ctx):
    await ctx.send("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/2d5710c1-6133-426b-ac1d-463ea3a3d2a7/dfthotw-3dcaeac3-2061-44d7-a98f-329a2c02c186.png/v1/fill/w_986,h_810,q_70,strp/lesbian_espeon_by_rhe_ima_dfthotw-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTA1MiIsInBhdGgiOiJcL2ZcLzJkNTcxMGMxLTYxMzMtNDI2Yi1hYzFkLTQ2M2VhM2EzZDJhN1wvZGZ0aG90dy0zZGNhZWFjMy0yMDYxLTQ0ZDctYTk4Zi0zMjlhMmMwMmMxODYucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.SWRvYHOEDR3xEEmCP-ONMS0nQ5lESUHtnf7lSgva6tk")

@bot.command()
async def dip(ctx):
    await ctx.send("https://tenor.com/view/nileseyy-niles-peace-out-disappear-meme-disappearing-guy-checking-out-gif-25558985")

@bot.command()
async def astolfo(ctx):
    await ctx.send("https://tenor.com/view/astolfo-gif-25520245")

@bot.command()
async def astolfobounce(ctx):
    await ctx.send("https://tenor.com/view/astolfo-gif-21758557")

@bot.command()
async def KYS(ctx):
    await ctx.send("https://tenor.com/view/ltg-low-tier-god-lightning-you-should-kys-now-gif-24662293")

@bot.command()
async def bridget(ctx):
    await ctx.send("https://tenor.com/view/guilty-gear-bridget-gif-26419214")

@bot.command()
async def bridgetbag(ctx):
    await ctx.send("https://tenor.com/view/bridget-guilty-gear-bounce-meme-gif-27437636")

@bot.command()
async def deadchat(ctx):
    await ctx.send("https://tenor.com/view/guilty-gear-elphelt-valentine-elphelt-valentine-dead-chat-gif-23324678")

@bot.command()
async def ServerIcon(ctx):
    icon_url = ctx.guild.icon.url
    await ctx.send(icon_url)
#returns the servers icon

@bot.command()
async def UserIcon(ctx, user:discord.Member):
    icon_url = user.display_avatar.url
    await ctx.send(icon_url)
#returns a pinged users icon

@bot.command()
async def kick(ctx, user: discord.Member):
    member = ctx.author
    guild = bot.get_guild(762470802687787051)
    Admin = guild.get_role(762471280627810324)
    if Admin in member.roles:
        await user.kick(reason=None)
    else:
        await ctx.send(f"You can only moderate members below your role!")
        return
#Kicks a pinged user when the admin role is true in the blizzard

@bot.command()
async def ban(ctx, user:discord.Member):
    member = ctx.author
    guild = bot.get_guild(762470802687787051)
    Admin = guild.get_role(762471280627810324)
    if Admin in member.roles:
        await user.ban(reason=None, delete_message_seconds=600)
    else:
        await ctx.send(f"You can only moderate members below your role!")
        return
#bans a pinged user when said user has admin role in blizzard
@bot.command()
async def purge(ctx, Number):
    member = ctx.author
    guild = bot.get_guild(762470802687787051)
    Admin = guild.get_role(762471280627810324)
    if Admin in member.roles:
        await ctx.channel.purge(limit=int(Number), oldest_first=False, bulk=True, reason=None)
    else:
        await ctx.send(f"You can't use this command.")
        return
#purges 100 messages

@bot.command()
async def Salamence(ctx):
    Salamence = "https://cdn.donmai.us/original/bd/ff/bdff25cfcd33e2a18402614719a0ee77.jpg"
    DracoMeteor = "https://external-preview.redd.it/6Q1vYZQNn2TNLPmqdx0tTVDFPRvpIRfOFn9nWvCYpfs.jpg?auto=webp&s=3c4312ba20d949faf92d635315c21dc1e706a6d0"
    Attack = "https://cdnb.artstation.com/p/assets/images/images/032/382/121/large/fernando-alberto-carrazco-cano-salamence-attackingweb.jpg?1606270520"
    Headbutt = "https://cdn.donmai.us/original/30/b6/30b62efffaaffb1ff5c267e7d25063ca.jpg"
    Flying2 = "https://cdn.wallpapersafari.com/18/76/d6p70y.jpg"
    Buddies = "https://c4.wallpaperflare.com/wallpaper/336/735/824/ishmam-pokemon-salamence-bagon-hd-wallpaper-preview.jpg"
    Flying = "https://cdn.donmai.us/original/53/d7/53d7aa3cd122b9c6e7e732fa8bb227c9.jpg"
    Mega = "https://e1.pxfuel.com/desktop-wallpaper/650/895/desktop-wallpaper-mega-salamence-by-rabid-salamence.jpg"
    DoubleEdge = "https://cdn.weasyl.com/~drakarts/submissions/852830/bc83a33f7720cade6dc677adb1b5c1ebc4e7a94a70419de3f9bc09de5ccb393d/drakarts-mega-salamence-draco-meteor.jpg"
    May = "https://i.pinimg.com/originals/83/71/92/8371923962a6232fa73cf0405697d385.jpg"
    Protect = "https://64.media.tumblr.com/45df0731fee9a78af0cfd24e2b41f8af/e424e9d6a6666913-29/s1280x1920/40f7d97197795dcbcd0ecc311de6c4aa27031387.png"
    List = [Salamence, DracoMeteor, Attack, Headbutt, Flying2, Buddies, Flying, Mega, DoubleEdge, May, Protect]
    await ctx.send(random.choice(List))
#summons random salamence image from the variables

@bot.command()
async def faggot(ctx):
    A = "https://cdn.donmai.us/original/cd/f9/cdf929020cbab0449c108631e98656e1.png"
    A2 = "https://i.imgflip.com/62mcpv.jpg"
    A3 = "https://64.media.tumblr.com/18f70b0c79246a43e831df59794bac36/tumblr_p9tq092etA1rpzrrmo1_1280.png"
    A4 = "https://preview.redd.it/n49q452gdtm61.png?auto=webp&s=a36a9cc1be815720d3d27392337de5965457fe6c"
    A5 = "https://i.redd.it/i8m0dt26dtr71.jpg"
    A6 = "https://i.pinimg.com/736x/d6/14/02/d614029a12805d51d2edb3a43729b7ac.jpg"
    A7 = "https://pm1.aminoapps.com/6526/0d93e36de089401617105aa84959ba1e0bcafc46_hq.jpg"
    A8 = "https://i.kym-cdn.com/photos/images/original/001/292/040/bbb.jpg"
    A9 = "https://pm1.aminoapps.com/6610/e5e5e5309e285740acfbeefdea4252c306deb909_hq.jpg"
    A10 = "https://i.pinimg.com/474x/58/6c/4f/586c4f1ddae82a51383962378cd10039.jpg"
    A11 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7ea12bea-1e4d-48c0-b35c-8697f0e734e9/deeb9jm-c64aa75b-17df-47ed-9593-5a06d4bf09fb.jpg/v1/fill/w_774,h_1033,q_70,strp/monster_energy_astolfo_by_nekoboxzaza_deeb9jm-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTM2NiIsInBhdGgiOiJcL2ZcLzdlYTEyYmVhLTFlNGQtNDhjMC1iMzVjLTg2OTdmMGU3MzRlOVwvZGVlYjlqbS1jNjRhYTc1Yi0xN2RmLTQ3ZWQtOTU5My01YTA2ZDRiZjA5ZmIuanBnIiwid2lkdGgiOiI8PTEwMjQifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.nNdgSZ9iQFfUUj6FRt-0ythVBojDb4v_y5oNi3c5mGg"
    A12 = "https://i.kym-cdn.com/photos/images/original/002/019/882/515"
    A13 = "https://art.ngfiles.com/images/2001000/2001030_sanrioboyfriend_old-astolfo-monster-meme.jpg?f1628309888"
    AstolfoCosplay = "https://tenor.com/view/astolfo-cosplay-emiru-tikrok-rockefeller-street-gif-17205441"
    AstolfoSpin = "https://tenor.com/view/astolfo-gif-22218017"
    AstolfoDance = "https://tenor.com/view/astolfo-fate-dance-gif-22449552"
    Astolfo = "https://i.redd.it/19wv66k6pyg61.png"
    AstolfoLounge = "https://images.alphacoders.com/889/889928.png"
    AstolfoThink = "https://media.discordapp.net/attachments/634638016698384395/1118352986779942922/1190187-FateApocrypha-FGO-Fate-Series-bicolored-hair-french-braid.jpg?width=578&height=662"
    B = "https://preview.redd.it/bridget-looks-sick-heres-a-quick-fanart-v0-ivbo5t023qg91.jpg?width=640&crop=smart&auto=webp&s=06aef7e605befbcbf08eec1729318ec1da5acf6c"
    B2 = "https://pbs.twimg.com/media/Fc764O6acAETplr?format=jpg&name=4096x4096"
    B3 = "https://64.media.tumblr.com/5235fa4e629229f83cdd8d979d9ba703/733b5c559430b666-08/s1280x1920/f61fe9e1cd164962f0ae0bd3b50455ef2c10836c.png"
    B4 = "https://preview.redd.it/lt2mohqa6rg91.jpg?auto=webp&s=7f1b0ac3af6bae02058bb3f5bd95bfccda757dbc"
    B5 = "https://static.zerochan.net/Bridget.%28GUILTY.GEAR%29.full.2783164.png"
    C = "https://pbs.twimg.com/media/C-hqYdUXYAAQy2T.jpg"
    C2 = "https://hentaitrap.com/uploads/posts/cover/medium/217/2175723-46c14.jpg"
    FelixCosplay = "https://tenor.com/view/felix-argyle-trap-funny-cosplay-re-zero-gif-26551204"
    FelixGaming = "https://tenor.com/view/felix-re-zero-felix-argyle-speech-bubble-speech-gif-25397116"
    F = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/d3456178-ab60-492f-bcdf-00f062f9ade3/dc70iu4-e0e6d33a-49a3-4588-b2bf-fd534bd31d28.jpg/v1/fill/w_636,h_900,q_75,strp/felix_argyle__nsfw_opt__by_axsens_dc70iu4-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9OTAwIiwicGF0aCI6IlwvZlwvZDM0NTYxNzgtYWI2MC00OTJmLWJjZGYtMDBmMDYyZjlhZGUzXC9kYzcwaXU0LWUwZTZkMzNhLTQ5YTMtNDU4OC1iMmJmLWZkNTM0YmQzMWQyOC5qcGciLCJ3aWR0aCI6Ijw9NjM2In1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.VWlgbez60tPHErHM_U5dsKc3-NJhSPJjg6uadiX9KaQ"
    FelixPeace = "https://tenor.com/view/felix-argyle-cute-smile-gif-13483003"
    F2 = "https://i.imgur.com/RB7NmO4.jpeg"
    F3 = "https://cdn.donmai.us/original/6e/21/6e218f9b91bc069292ac1204e8f5c005.png"
    F4 = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/edafe512-ec8d-4a8e-a354-b450f5d0a387/deyj329-5af65aef-b14c-4d83-a768-6a17ee55d940.png/v1/fill/w_1192,h_670,q_70,strp/felix_argyle_fanart_by_403yonjj_deyj329-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTA4MCIsInBhdGgiOiJcL2ZcL2VkYWZlNTEyLWVjOGQtNGE4ZS1hMzU0LWI0NTBmNWQwYTM4N1wvZGV5ajMyOS01YWY2NWFlZi1iMTRjLTRkODMtYTc2OC02YTE3ZWU1NWQ5NDAucG5nIiwid2lkdGgiOiI8PTE5MjAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.EURe6APKUWwmlLfyFzkDwZu5PR-oO3jd1aCWjLIngag"
    FelixEars = "https://tenor.com/view/felix-argyle-gif-11149329"
    F5 = "https://cdn.donmai.us/sample/ea/67/__felix_argyle_re_zero_kara_hajimeru_isekai_seikatsu_drawn_by_matemi__sample-ea670f4201a4ea293c12c562cf18b0f2.jpg"
    F6 = "https://c4.wallpaperflare.com/wallpaper/189/848/961/anime-re-zero-starting-life-in-another-world-crusch-karsten-felix-argyle-wallpaper-preview.jpg"
    Hideiri = "https://tenor.com/view/hideri-hideri-kanzaki-anime-cute-girl-gif-17772038"
    HidSwag = "https://tenor.com/view/hideri-anime-traps-gif-11098597"
    Suprise = "https://tenor.com/view/blend_s-opening-surprise-anime-trap-gif-10374568"
    Milk = "https://tenor.com/view/classovatrash-wise_wolfy-wise-den-rileydreal1-gif-20220881"
    WithMen = "https://media.discordapp.net/attachments/721821486599503937/985149863366909974/DEA44F13-882A-4C71-BA49-76214CA1DB35-1-1.gif"
    AstolfoMaid = "https://media.discordapp.net/attachments/422460091749498881/950915869226188820/You_4.gif"
    SupriseCosplay = "https://tenor.com/view/blend-s-cosplay-its-a-trap-smile-sweet-sister-sadistic-suprise-service-bon-appétit-s-gif-26244710"
    List = [AstolfoCosplay, AstolfoSpin, AstolfoDance, FelixCosplay, FelixGaming, FelixPeace, FelixEars, Hideiri, HidSwag,
            Suprise, SupriseCosplay, Milk, Astolfo, AstolfoThink, AstolfoLounge, A, A2, A3, A4, A5, F, F2, F3, F4,
            F5, F, WithMen, AstolfoMaid, F6, B, B2, B3, B4, A6, A7, A8, B5, C, A9, A10, C2, A11, A12, A13]
    await ctx.send(random.choice(List))

@bot.command()
async def boykisser(ctx):
    SeeMen = "https://tenor.com/view/mauzy-mice-gif-17645860421574879161"
    Boykisser = "https://tenor.com/view/mauzymice-boykisser-jumpscare-boy-kisser-mauzy-mice-gif-8912233332616251301"
    Boykisser2 = "https://tenor.com/view/boykisser-boykisser-meme-gif-gif-27524383"
    BoyText = "https://tenor.com/view/silly-cat-mauzy-mice-boys-texting-gif-17756669638833090229"
    IWouldNever = "https://tenor.com/view/mauzy-mice-gif-11387475430588773838"
    Boykisser3 = "https://tenor.com/view/mauzymice-cat-gif-27571568"
    WhereMenAt = "https://tenor.com/view/mauzymice-mauzy-mauzy-mice-silly-silly-cat-gif-16562063169824368899"
    faggot = "https://tenor.com/view/mauzymice-cat-gif-7844744970396116880"
    faggot2 = "https://tenor.com/view/mauzy-mice-gif-15066541285631110359"
    cutemen = "https://tenor.com/view/mauzy-mice-silly-cat-boys-gif-13246211575307806790"
    bk4 = "https://media.discordapp.net/attachments/945059919906873405/1099424772514926782/attachment-17.gif"
    List = [SeeMen, Boykisser, Boykisser2, Boykisser3, BoyText, IWouldNever, WhereMenAt, faggot, faggot2, cutemen, bk4]
    await ctx.send(random.choice(List))
#summons gay shit

async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cataas.com/cat') as r:
            if r.status == 200:
                await ctx.send(file=discord.File(fp=io.BytesIO(await r.read()), filename="whatever.jpg"))
 #summons random cat image from that site

@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dog.ceo/api/breeds/image/random') as r:
            if r.status == 200:
                await ctx.send(file=discord.File(fp=io.BytesIO(await r.read())))
#summons random dog image from that site (broken)

#the next two blocks are reaction roles for "The Blizzard"

@bot.command()
async def react(ctx):
    msg=await ctx.send("React here for roles! wolfgasm: Elder Student. Swag: Swag Gang. Qoggies: Dumbass.")
    global msg_id
    msg_id = msg.id

    wolfgasm = '<:wolfgasm:817931164202827788>'
    swag = '<:Swag:1120807757063397396>'
    qoggies = '<:Qoggies:1120807941558251580>'
    if msg.content == "React here for roles! wolfgasm: Elder Student. Swag: Swag Gang. Qoggies: Dumbass.":
        await msg.add_reaction(wolfgasm)
        await msg.add_reaction(swag)
        await msg.add_reaction(qoggies)
#has the bot summon and react to a message "React here for roles!"

# returns with a message that says "<word> me daddy"
@bot.command()
async def daddy(ctx, bruh):
    await ctx.send(f'{bruh} me daddy')

@bot.command()
async def bkrate(ctx: commands.Context):
    gay = random.randint(0, 100)
    msg = "not even a boyliker damn"
    if gay > 25:
        msg = "kinda gay ngl"
    if gay > 50:
        msg = "damn pretty fuckin gay"
    if gay > 75:
        msg = "holy shit you're a fag"

    embed = discord.Embed(title=f"Boykisser Rating: {gay}% :rainbow_flag:", description=msg)
    await ctx.send(embed=embed)

@bot.command()
async def gkrate(ctx: commands.Context):
    gay = random.randint(0, 100)
    msg = "bro doesnt like women"
    if gay > 25:
        msg = "mid tier rizz"
    if gay > 50:
        msg = "holy shit they get play"
    if gay > 75:
        msg = "bros making out with a girl right now"

    embed = discord.Embed(title=f"Girlkisser Rating: {gay}% :rainbow_flag:", description=msg)
    await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(reaction):
    guild = bot.get_guild(762470802687787051)
    User = guild.get_member(reaction.user_id)
    Student = guild.get_role(776634196684439572) #equipped with wolfgasm
    Dumbass = guild.get_role(960678410349314048) #equipped with qoggies
    SwagGang = guild.get_role(818768572779462688) #equipped with swag
    if msg_id == reaction.message_id:
        if reaction.emoji.name == 'Qoggies':
            await User.add_roles(Dumbass)
        if reaction.emoji.name == 'wolfgasm':
            await User.add_roles(Student)
        if reaction.emoji.name == 'Swag':
            await User.add_roles(SwagGang)
bot.run(TOKEN)

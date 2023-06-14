import discord
import random
from discord.ext import commands
from discord import app_commands
import aiohttp
import asyncio
from aiohttp import web
import io

intents = discord.Intents.all()
TOKEN = "rainy loves men!"
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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
     if message.author.bot: return
     content = message.content.lower()
     if "snow" in content:
         await bot.get_user(180124680647213056).send(f"{message.author} said {message.content}")

     await bot.process_commands(message)
    #easy call and response code

@bot.event
async def on_ready():
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
async def roll(ctx):
    await ctx.send(random.randint(1,69))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def erika(ctx):
    await ctx.send('Erika fucking sucks!')

@bot.command()
async def sabby(ctx):
    await ctx.send('CHEESEBURGER SUPREMACY')

@bot.command()
async def blossom(ctx):
    await ctx.send('Blossom got caught with a choker lol')
#replies with a string that is defined in the send

@bot.command()
async def taco(ctx):
    await ctx.send('TacoBruh is really dumb!')

@bot.command()
async def cowgif(ctx):
    await ctx.send("http://imgur.com/gallery/YiMUiop")

@bot.command()
async def lesbeon(ctx):
    await ctx.send("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/2d5710c1-6133-426b-ac1d-463ea3a3d2a7/dfthotw-3dcaeac3-2061-44d7-a98f-329a2c02c186.png/v1/fill/w_986,h_810,q_70,strp/lesbian_espeon_by_rhe_ima_dfthotw-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTA1MiIsInBhdGgiOiJcL2ZcLzJkNTcxMGMxLTYxMzMtNDI2Yi1hYzFkLTQ2M2VhM2EzZDJhN1wvZGZ0aG90dy0zZGNhZWFjMy0yMDYxLTQ0ZDctYTk4Zi0zMjlhMmMwMmMxODYucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.SWRvYHOEDR3xEEmCP-ONMS0nQ5lESUHtnf7lSgva6tk")

@bot.command()
async def astolfo(ctx):
    await ctx.send("https://tenor.com/view/astolfo-gif-25520245")

@bot.command()
async def astolfobounce(ctx):
    await ctx.send("https://tenor.com/view/astolfo-gif-21758557")

@bot.command()
async def borgor(ctx):
    await ctx.send("https://s23209.pcdn.co/wp-content/uploads/2022/07/220602_DD_The-Best-Ever-Cheeseburger_267-1024x1536.jpg")
#sends image linked in the send

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
    guild = bot.get_guild(1117192931258925097)
    Admin = guild.get_role(1117193766449729636)
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
    AstolfoCosplay = "https://tenor.com/view/astolfo-cosplay-emiru-tikrok-rockefeller-street-gif-17205441"
    AstolfoSpin = "https://tenor.com/view/astolfo-gif-22218017"
    AstolfoDance = "https://tenor.com/view/astolfo-fate-dance-gif-22449552"
    Astolfo = "https://i.redd.it/19wv66k6pyg61.png"
    AstolfoLounge = "https://images.alphacoders.com/889/889928.png"
    AstolfoThink = "https://rare-gallery.com/uploads/posts/1190187-FateApocrypha-FGO-Fate-Series-bicolored-hair-french-braid.jpg"
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
            F5, F, WithMen, AstolfoMaid]
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
    msg=await ctx.send("React here for roles! wolfgasm: Elder Student. Swag: Swag Gang. Qoggies: Dumbass. Liliblush: NSFW.")
    global msg_id
    msg_id = msg.id

    wolfgasm = '<:wolfgasm:817931164202827788>'
    swag = '<:Swag:812663160917721118>'
    qoggies = '<:Qoggies:762484869854003231>'
    Liliblush = '<:LiliBlush:767942752657866763>'
    if msg.content == "React here for roles! wolfgasm: Elder Student. Swag: Swag Gang. Qoggies: Dumbass. Liliblush: NSFW.":
        await msg.add_reaction(wolfgasm)
        await msg.add_reaction(swag)
        await msg.add_reaction(qoggies)
        await msg.add_reaction(Liliblush)
#has the bot summon and react to a message "React here for roles!"

# returns with a message that says "<word> me daddy"
@bot.command()
async def daddy(ctx, bruh):
    await ctx.send(f'{bruh} me daddy')

@bot.event
async def on_raw_reaction_add(reaction):
    guild = bot.get_guild(762470802687787051)
    User = guild.get_member(reaction.user_id)
    Student = guild.get_role(776634196684439572) #equipped with wolfgasm
    Dumbass = guild.get_role(960678410349314048) #equipped with qoggies
    SwagGang = guild.get_role(818768572779462688) #equipped with swag
    NSFW = guild.get_role(818050950874791936) #equipped with Liliblush
    if msg_id == reaction.message_id:
        if reaction.emoji.name == 'LiliBlush':
            await User.add_roles(NSFW)
        if reaction.emoji.name == 'Qoggies':
            await User.add_roles(Dumbass)
        if reaction.emoji.name == 'wolfgasm':
            await User.add_roles(Student)
        if reaction.emoji.name == 'Swag':
            await User.add_roles(SwagGang)

bot.run(TOKEN)

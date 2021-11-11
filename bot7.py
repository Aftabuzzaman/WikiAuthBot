from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from tinydb import TinyDB, Query

bot = Client(intents=Intents(messages=True, guilds=True, members=True, typing=True, presences=False))
slash = SlashCommand(bot, sync_commands=True)

bot = commands.Bot(command_prefix=".redundant",intents=Intents(messages=True, guilds=True, members=True, typing=True, presences=False))
slash = SlashCommand(bot, override_type = True, sync_commands=True)

Ft=Query()

@slash.slash(name="whois", 
            guild_ids=guild_ids,
            description="Search a user's linked Wikimedia account. Leave blank for your own.",
            options=[
                create_option(
                    name="user",
                    description="Select the user or input their Discord ID.",
                    option_type=6 or 4,
                    required=False
                )
            ])
async def whois(self, ctx, user: discord.User=None):
    tdb = TinyDB('Wiki/auth.json')
    rdb = TinyDB('Wiki/responses.json')
    t = rdb.search(Ft.lang=='EN')[0]
    await ctx.respond()
    if user == None:
        user = ctx.author
    try:
        usr = tdb.search(Ft.id==user.id)[0]
    except:
        try:
            usr=tdb.search(Ft.id==int(usr))[0]
        except:
            await ctx.send(content=f'{user} is not authenticated.')
    else:
        apiurl = "https://en.wikipedia.org/w/api.php?action=query&meta=globaluserinfo&guiuser={usr['wnam']}&guiprop=groups%7Cmerged%7Cunattached&format=json"
        GAIurl = "https://en.wikipedia.org/w/index.php?title=Special%3ACentralAuth/"
        col = 0xCCCCCC   
        dat = get(apiurl.replace("{usr['wnam']}",usr['wnam']))
        dat.raise_for_status()
        dat = dat.json()['query']['globaluserinfo']
        try:
            if dat['groups'] != []:
                ggps = f"{t['gGroups:']} {', '.join(dat['groups'])}"
            else:
                ggps = ''
        except:
            await ctx.send(content='''Sorry, this user's authentication appears to be outdated, they will need to re-auth to fix this.''')
        else:
            wiki=[]
            edits = 0
            for s in dat['merged']:
                if s['editcount'] > 0:
                    edits = edits + s['editcount']
                    try:
                        if s['groups'] == 'groups':
                            raise IndexError
                        gps = f"{t['Groups:']} {', '.join(s['groups'])}"
                        inl = False
                    except Exception as e:
                        gps = ''
                        inl = True
                    wiki.append({'wik':s['wiki'], 'ec':s['editcount'], 'gps':gps, 'inl':inl})
            wiki = sorted(wiki, key = lambda i: i['ec'], reverse=True)
            blkd = ''
            indefd = 0
            for w in dat['merged']:
                if 'blocked' in str(w):
                    try:
                        if w['blocked']['reason'] == '':
                            reas = '<!---No reason provided--->'
                        else:
                            reas = w['blocked']['reason']
                        if blkd == '':
                            blkd = f"**{w['wiki']}** ({w['blocked']['expiry']})\n  *{reas}*"
                        else:
                            blkd = f"{blkd}\n**{w['wiki']}** ({w['blocked']['expiry']})\n  *{reas}*"
                        if w['blocked']['expiry'].lower() == 'infinity':
                            indefd = 1
                    except:
                        print(f"Got blocked but not err for {usr['wnam']}")
            if blkd != '':
                blkd = f"\n<:declined:359850777453264906> **BLOCKED**\n{blkd}"
            i = 1
            embed=discord.Embed(title=f"{usr['wnam']}", description=f"Discord: <@{usr['id']}>\n{t['Registered:']} {dat['registration'].split('T')[0]}\n{t['Home:']} {dat['home']}$
            for s in wiki:
                if i < 11:
                    embed.add_field(name=s['wik'], value=f"{t['Edits:']} {s['ec']:,}\n{s['gps']}", inline=s['inl']) 
                    i += 1
            then = parser.parse(dat['registration'])
            for x in dat['merged']:
                if parser.parse(x['timestamp']) < then:
                    then = parser.parse(x['timestamp'])
            if i > 7:
                embed.set_footer(text=t['max8'])          
            if (datetime.datetime.now(datetime.timezone.utc)-then).days > 6570 and edits > 150000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/1/12/Editor_-_lapis_matter_iv.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 5840 and edits > 132000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Editor_-_lapis_matter_iii.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 5110 and edits > 11400:
                med = 'https://upload.wikimedia.org/wikipedia/commons/6/6e/Editor_-_lapis_matter_ii.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 4380 and edits > 96000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/8/85/Editor_-_lapis_philosophorum_superstar.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 3650 and edits > 78000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/0/00/Editor_-_orichalcum_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 2920 and edits > 60000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Editor_-_bufonite_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 2555 and edits > 51000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/d/dd/Editor_-_platinum_star_II.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 2190 and edits > 42000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/8/86/Editor_-_platinum_star_I.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 1825 and edits > 33000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Editor_-_rhodium_star_III.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 1642 and edits > 28500:
                med = 'https://upload.wikimedia.org/wikipedia/commons/1/1f/Editor_-_rhodium_star_II.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 1460 and edits > 24000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Editor_-_rhodium_star_I.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 1277 and edits > 20000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Editor_-_gold_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 1095 and edits > 16000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/0/06/Editor_-_silver_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 912 and edits > 12000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Editor_-_bronze_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 730 and edits > 8000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/5/53/Editor_-_iron_star.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 547 and edits > 6000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/c/cd/Editor_-_gold_ribbon_-_3_pips.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 365 and edits > 4000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/c/c2/Editor_-_silver_ribbon_-_2_pips.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 182 and edits > 2000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/6/67/Editor_-_bronze_ribbon_-_1_pip.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 91 and edits > 1000:
                med = 'https://upload.wikimedia.org/wikipedia/commons/f/f3/Editor_-_blue_ribbon_-_0_pips.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 30 and edits > 200:
                med = 'https://upload.wikimedia.org/wikipedia/commons/e/e7/Editor_-_white_ribbon_-_0_pips.jpg'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 23 and edits > 150:
                med = 'https://upload.wikimedia.org/wikipedia/commons/7/74/Registered_editor_badge_with_tildes.jpg'    
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 15 and edits > 100:                    
                med = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Registered_Editor_lv2.svg/222px-Registered_Editor_lv2.svg.png'
            elif (datetime.datetime.now(datetime.timezone.utc)-then).days > 8 and edits > 50:
                med = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Registered_Editor_lv3.svg/222px-Registered_Editor_lv3.svg.png'
            else:
                med = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Registered_Editor_lv4.svg/222px-Registered_Editor_lv4.svg.png'
            embed.set_thumbnail(url=med)
            await ctx.send(embed=embed)

@cog_ext.cog_slash(name="auth",
            guild_ids=guild_ids,
            description="Authenticate to your Wikimedia account. (THIS COMMAND IS IN TESTING PHASE, IT WILL NOT ACTUALLY WORK)")
async def auth(self, ctx):
    ctx.respond(eat=True)
    contok = open('tokens/ontok','r').read()
    consec = open('tokens/onsec','r').read()       
    if requests.get('https://wikiauthbot.toolforge.org/test/').text == 'Hello World!':
        consumer_token = ConsumerToken(contok, consec)
        sys.stdout = open(os.devnull, 'w') #TURN OFF CONSOLE PRINT
        handshaker = Handshaker(f"https://{t['lang'].lower()}.wikipedia.org/w/index.php", consumer_token)
        sys.stdout = sys.__stdout__        #TURN ON  CONSOLE PRINT
        redirect, request_token = handshaker.initiate(callback=f'https://wikiauthbot.toolforge.org/wauth/{hex(ctx.author.id)}/') 
    else:
        try:
            await bot.get_channel(695443373292781599).send(f'WikiAuthBot (wiki auth)-slash: Failed to get test result from toolforge. Reverting to pythonanywhere.')
        except:
            pass
        consumer_token = ConsumerToken(open('tokens/contok','r').read(), open('tokens/consec','r').read())
        handshaker = Handshaker(f"https://{t['lang'].lower()}.wikipedia.org/w/index.php", consumer_token)
        redirect, request_token = handshaker.initiate(callback=f'https://1vork.pythonanywhere.com/wauth/{hex(ctx.author.id)}/')                     
    db = TinyDB('Wiki/authd.json')
    Ft = Query()
    rt = pickle.dumps(request_token, 0).decode()
    db.upsert({'id':ctx.author.id, 'request_token':rt, 'wikilang': f"https://{t['lang'].lower()}.wikipedia.org/w/index.php"}, Ft.id==ctx.author.id)        
    await ctx.send("Hi there, to authenticate to your account, please follow this link {rt}\n**Note: Please do not share this link**" ,hidden=True)

bot.run(open('tokens/wiki','r').read())

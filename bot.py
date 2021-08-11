import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import time

import database
import helper

#CHANGE
adminIDs = ["73642971517423616","209294027332386817"]

client = Bot(description="Discord Manager Bot", command_prefix="!", pm_help = True)
dataBase = database.database()

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')

async def watchSubscriptions():
	await client.wait_until_ready()
	while not client.is_closed:
		expiredSubs = dataBase.getExpiredSubs()
		dataBase.removeExpiredSubs()
		for sub in expiredSubs:
			user = discord.utils.get(client.get_all_members(), id=sub[0])
			expiredMessage = helper.expiredMessage()
			if user is not None:
				await client.send_message(user, embed=expiredMessage)
				await helper.removeSubRole(client, user)
				adminMessage = helper.notifyAdminDeactivateMessage(sub[0])
				for adminID in adminIDs:
					user = discord.utils.get(client.get_all_members(), id=adminID)
					await client.send_message(user, embed=adminMessage)
					await asyncio.sleep(.5)

		soonToExpireSubs = dataBase.getSoonToExpireSubs()
		for sub in soonToExpireSubs:
			user = discord.utils.get(client.get_all_members(), id=sub[0])
			twoDayExpireMsg = helper.twoDayNotificationMessage()
			if user is not None:
				await client.send_message(user, embed=twoDayExpireMsg)

		t = time.localtime()
		t = time.mktime(t[:3] + (0,0,0) + t[6:])
		await asyncio.sleep(t + 24*3600 - time.time()) #wait until midnight tomorrow to run again

async def keepDatabaseAlive(): #send random request to avoid timeout
	await client.wait_until_ready()
	await asyncio.sleep(60*5)
	dataBase.conn.ping()

@client.command(pass_context=True)
async def activate(ctx, key: str):
	"""Activate your subscription"""
	id = ctx.message.author.id
	activation = dataBase.activateKey(id, key)
	embed = ""
	if (activation):
		await helper.addSubRole(client, ctx.message.author)
		adminMessage = helper.notifyAdminActivateMessage(id)
		for adminID in adminIDs:
			user = discord.utils.get(client.get_all_members(), id=adminID)
			await client.send_message(user, embed=adminMessage)
			await asyncio.sleep(.5)
		embed = helper.validKeyMessage(activation)  
	else:
		embed = helper.invalidKeyMessage()
	await client.say(embed=embed)

@client.command(pass_context=True)
async def generate(ctx, days: str = 30):
	"""Generate a new key"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return	
	key = dataBase.generateKey(days)

	await client.say(key)

@client.command(pass_context=True)
async def generateMultiple(ctx, days: str = 30, amount: int = 5):
	"""Generate multiple keys"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return	
	message = ""
	for i in range(amount):	
		key = dataBase.generateKey(days)
		message += "{}: {}\n".format(key[0], key[1])
	await client.say(message)

@client.command(pass_context=True)
async def cgenerate(ctx, days: str, customKey: str):
	"""Generate a custom key"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return	
	dataBase.customGenerateKey(days, customKey)
	embed = helper.customGenerateKeyMessage(days, customKey)
	await client.say(embed=embed)

@client.command(pass_context=True)
async def remove(ctx, userID: str):
	"""Removes user from database/role"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	dataBase.removeUser(userID)
	user = discord.utils.get(client.get_all_members(), id=userID)
	await helper.removeSubRole(client, user)
	embed = helper.removeUserMessage(userID)
	await client.say(embed=embed)

@client.command(pass_context=True)
async def check(ctx, userID: str):
	"""Returns specific users subscription information"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	userInfo = dataBase.grabUserInfo(userID)
	await client.say(userInfo)

@client.command(pass_context=True)
async def showKeys(ctx):
	"""Returns list of unused keys"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	keys = dataBase.grabNotUsedKeys()
	n = 30 
	final = [keys[i * n:(i + 1) * n] for i in range((len(keys) + n - 1) // n )]
	for keys in final:
		message = "Quantity: " + str(len(keys)) + "\n"
		for key in keys:
			message += '{}: {}\n'.format(key[0], key[1])
		await client.say(message)
		await asyncio.sleep(.5)

@client.command(pass_context=True)
async def deleteUsedKeys(ctx):
	"""Deletes used keys in database"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	dataBase.deleteUsedKeys()
	embed = helper.deleteAllUsedKeysMessage()
	await client.say(embed=embed)

@client.command(pass_context=True)
async def deleteAllKeys(ctx):
	"""Deletes all keys in database"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	dataBase.deleteAllKeys()
	embed = helper.deleteAllKeysMessage()
	await client.say(embed=embed)

@client.command(pass_context = True)
async def clear(ctx, number=100):
	"""Deletes quanity of last messages, default 100"""
	id = ctx.message.author.id
	if (not helper.isAdmin(id, adminIDs)): return
	mgs = []
	number = int(number)
	async for x in client.logs_from(ctx.message.channel, limit = number):
		mgs.append(x)
	await client.delete_messages(mgs)
	
@client.command(pass_context=True)
async def renew(ctx):
	"""sends renewal link"""
	embed = helper.renewMessage()
	await client.say(embed=embed)

client.loop.create_task(watchSubscriptions())
client.loop.create_task(keepDatabaseAlive())	

client.run('')

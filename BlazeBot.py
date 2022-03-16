import discord
from twss import TWSS
import nltk
from os import environ
from random import random
from discord.ext.commands import Bot
from discord import DeletedReferencedMessage
from re import compile
from string import punctuation
from random import random
from dotenv import load_dotenv


TWSS_CHANCE = 1/int(environ.get("TWSS_CHANCE","10"))



def get_reaction_message(message:str)->list:
	'''
		Convert all the chars in the message to reactable emojis that discord can use.
		NOTE: if the message contains chars that are not in the letters dict or if the same letter is used more times 
		in the message than the number of emojis available for that character, it doesn't fail but just doesn't do anything with it
	'''
	
	# Dictionary of all letters

	letters = {
		"A":["🇦","🅰️"],
		"B":["🇧","🅱️"],
		"C":["🇨"],
		"D":["🇩"],
		"E":["🇪"],
		"F":["🇫"],
		"G":["🇬"],
		"H":["🇭"],
		"I":["🇮","ℹ️"],
		"J":["🇯"],
		"K":["🇰"],
		"L":["🇱"],
		"M":["🇲","Ⓜ️"],
		"N":["🇳"],
		"O":["🇴","🅾️","⭕","0️⃣"],
		"P":["🇵","🅿️"],
		"Q":["🇶"],
		"R":["🇷"],
		"S":["🇸"],
		"T":["🇹"],
		"U":["🇺"],
		"V":["🇻"],
		"W":["🇼"],
		"X":["🇽","❌","❎"],
		"Y":["🇾"],
		"Z":["🇿"]
	}

	output = []
	for char in message:
		emojis = letters.get(char.upper(),None)

		if emojis:
			output.append(emojis.pop(0))
	return output

# Filter out of the duplicate chars in the word without messing up the order
def filter_duplicates(seq:str)->str:
	seen = set()
	seen_add = seen.add
	return "".join([x for x in seq if not (x in seen or seen_add(x))])

# Clean the sentence from all punctuation
def clean_sentence(sentence:str)->str:
	pattern = compile(f"[{punctuation}]")
	sentence = pattern.sub("",sentence)
	return sentence

# Create a bot instance
bot = Bot("&")
client = discord.Client()

@bot.event 
async def on_ready(): 
	global twssBot
	twssBot = TWSS()
	print('We have logged in.')


@bot.event
async def on_message(message : discord.Message):
	if message.content[0]!="&":
		chance =  random()
		print(chance,TWSS_CHANCE)
		if chance< TWSS_CHANCE:
			sentence = clean_sentence(message.content)
			if twssBot(sentence) and message.author != bot.user:
				response = f"> {message.content}\n{message.author.mention} Thats what she said ;D"
				await message.channel.send(response)
	else:
		try:
			await bot.process_commands(message)
		except discord.Forbidden:
				response = f"{message.author.mention} I do not have permission to send and/or react in this channel."
				await message.channel.send(response)


@bot.command(pass_context=True)
async def wr(ctx : discord.ext.commands.Context):

	message =  ctx.message.reference

	# Gets the message to be reacted to
	if not message:
		await ctx.channel.send(f"{ctx.message.author.mention} You forgot to reply to the message you want to react to")
		return
	else:
		word =  ctx.message.clean_content[4:]
		
		if len(word)>20:
			await ctx.message.author.send("Your message was more than 20 characters long. Due to discord limitations, only the first 20 characters will be used for the reaction")

		word =  word[:20]
		
	# word = filter_duplicates(word)

	replied_message = message.resolved

	if(isinstance(replied_message,DeletedReferencedMessage)):
		await ctx.channel.send(f"{ctx.message.author.mention} The message you replied to no longer exists ;-;")
		return

	# Clear all previous reactions
	await replied_message.clear_reactions()

	# get the list of emojis that can be used to form the message
	emoji_list = get_reaction_message(word)

	# React to the message emoji by emoji
	for emoji in emoji_list:
		# Add each emoji as a reaction
		await replied_message.add_reaction(emoji)

	await ctx.message.delete()
	# exit
	return

def install_nlkt_packages():
	nltk.download("punkt")


if __name__ == "__main__":
	load_dotenv()
	install_nlkt_packages()
	bot.run(environ['BLAZE_BOT_TOKEN'])
import discord
from twss import TWSS
from os import environ
from discord.ext.commands import Bot


# Dictionary of all letters
letters = {
	"A":"\U0001F1E6",
	"B":"\U0001F1E7",
	"C":"\U0001F1E8",
	"D":"\U0001F1E9",
	"E":"\U0001F1EA",
	"F":"\U0001F1EB",
	"G":"\U0001F1EC",
	"H":"\U0001F1ED",
	"I":"\U0001F1EE",
	"J":"\U0001F1EF",
	"K":"\U0001F1F0",
	"L":"\U0001F1F1",
	"M":"\U0001F1F2",
	"N":"\U0001F1F3",
	"O":"\U0001F1F4",
	"P":"\U0001F1F5",
	"Q":"\U0001F1F6",
	"R":"\U0001F1F7",
	"S":"\U0001F1F8",
	"T":"\U0001F1F9",
	"U":"\U0001F1FA",
	"V":"\U0001F1FB",
	"W":"\U0001F1FC",
	"X":"\U0001F1FD",
	"Y":"\U0001F1FE",
	"Z":"\U0001F1FF"
}

# Filter out of the duplicate chars in the word without messing up the order
def filter_duplicates(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]

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
		print(twssBot(message.content),message.content)
		if twssBot(message.content) and message.author != bot.user:
			response = f"> {message.content}\n{message.author.mention} Thats what she said ;D"
			await message.channel.send(response)
	else:
		await bot.process_commands(message)

@bot.command(pass_context=True)
async def wr(ctx : discord.ext.commands.Context):

	# Gets the message to be reacted to
	try:
		quoted = ctx.message.content.split("\n")[1]
	except IndexError as err:
		await ctx.channel.send(f"{ctx.message.author.mention} You forgot to quote the message you want to react to")
		return
	# Remove the bit that makes the message quoted
	quoted = quoted.replace("> ","")
	# Get the word to be reacted
	try:
		word = ctx.message.content.split("\n")[2]
	except Exception as e:
		await ctx.channel.send("Enter the text to be reacted")
	word = word.split(" ")
	# Get the author of the original message
	author = word.pop(0)
	# Remove the space and create the word
	word = "".join(word)
	word = filter_duplicates(word)
	# Get all the past 100 messages in the channel
	async for i in ctx.channel.history(limit=100):
		# Check if the quoted text is the same and if its from the same user
		if quoted == i.content and int(author[3:-1]) == i.author.id:
			# Fetch the message if it matches
			message = await ctx.channel.fetch_message(i.id)
			# Clear all previous reactions
			await message.clear_reactions()
			# React to the message char by char
			for char in word:
				# Add each char as a reaction
				await message.add_reaction(letters[char.upper()])
			# exit
			return

bot.run(environ['BLAZE_BOT'])
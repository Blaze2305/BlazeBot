import discord
from os import environ
from discord.ext.commands import Bot

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

def filter_duplicates(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]

bot = Bot("&")

@bot.event
async def on_message(message : discord.Message):
	if message.content[0]!="&":
		print(message.content)
	await bot.process_commands(message)



	
@bot.command(pass_context=True)
async def wordReact(ctx : discord.ext.commands.Context):
	try:
		quoted = ctx.message.content.split("\n")[1]
	except IndexError as err:
		await ctx.channel.send(f"{ctx.message.author.mention} You forgot to quote the message you want to react to")
		return
	async for i in ctx.channel.history(limit=100):
		quoted = quoted.replace("> ","")
		if quoted == i.content:
			message = await ctx.channel.fetch_message(i.id)
			try:
				word = ctx.message.content.split("\n")[2]
			except Exception as e:
				await ctx.channel.send("Enter the text to be reacted")
			word = filter_duplicates(word)
			for char in word:
				await message.add_reaction(letters[char.upper()])
			
bot.run(environ['REACT_BOT_DISCORD'])
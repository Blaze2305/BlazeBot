import discord
from os import environ
from discord.ext.commands import Bot

bot = Bot("&")

@bot.event
async def on_message(message : discord.Message):
	if message.content[0]!="&":
		print(message.content,message.author,message.mentions,message.reference,message.reactions)
	await bot.process_commands(message)



	
@bot.command(pass_context=True)
async def wordReact(ctx : discord.ext.commands.Context):
	try:
		text = ctx.message.content.split("\n")[1]
	except IndexError as err:
		await ctx.channel.send(f"{ctx.message.author.mention} You forgot to quote the message you want to react to")
		return
	async for i in ctx.channel.history(limit=100):
		quoted = text.replace("> ","")
		if quoted == i.content:
			message = await ctx.channel.fetch_message(i.id)
			await message.add_reaction("1F1E6")

bot.run(environ['REACT_BOT_DISCORD'])
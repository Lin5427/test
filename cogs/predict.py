import random
import discord

from discord.ext import commands
from ext.lists import *


class Prediction:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='8ball', description='Robotsu alpha does not do 8balls', no_pm=True)
    async def ball(self, ctx):
        await self.bot.say(f"\u180Erobotsu don't have 8ball, try `{ctx.prefix}prediction`")
        dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
        log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
        user = ctx.message.author
        em = discord.Embed(title=f'{user.display_name}')
        em.colour = (discord.Colour(0xc5465d))
        em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
        em.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_chan, embed=em)

    @commands.command(aliases=['fortune', 'predict', 'astrobotsu'], pass_context=True, name='predicti', no_pm=True,
                 description='Robotsu alpha will include future prediction forecast for your questions')
    async def predicti(self, ctx):
        await self.bot.say("\u180E```Hello there,\nmy Dev XAOS is working hard to bring PREDICTION to you\n "
                           "so you can enjoy asking questions about your future,\nthank you for your patience.```")
        dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
        log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
        user = ctx.message.author
        em = discord.Embed(title=f'{user.display_name}')
        em.colour = (discord.Colour(0xc5465d))
        em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
        em.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_chan, embed=em)

    @commands.command(aliases=["old8ball"], pass_context=True, name="oldball", no_pm=True,
                      description="If you still want the old command, here it is.")
    async def oldball(self, ctx, *, question:str):
        """It's just python random don't take it seriously"""
        message = ctx.message
        if message is None:
            usage = f'\u180EArgunent is missing\nUsage: `{ctx.prefix}{ctx.command.invoked_with} [yes/no question]`'
            await self.bot.say(usage)
            return
        embed = discord.Embed(colour=discord.Colour(0xfff200))
        embed.add_field(name="\u180EDon't take this so seriously", value='Read by: `xaos1502`', inline=True)
        embed.add_field(name='\u180EFor:', value=f'\u180E{ctx.message.author.mention}', inline=True)
        embed.add_field(name='\u180EResponse for you', value=f'{random.choice(magic_conch_shell)}')
        await self.bot.say(embed=embed)
        dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
        log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
        user = ctx.message.author
        em = discord.Embed(title=f'{user.display_name}')
        em.colour = (discord.Colour(0xc5465d))
        em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
        em.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_chan, embed=em)

    @commands.command(aliases=["prediction"], pass_context=True, name="crystalball", no_pm=True)
    async def crystalball(self, ctx, *, question:str):
        """Based on the ancient divination I Ching oracle,
        use it as a guide"""
        message = ctx.message
        if message==None:
            await self.bot.say('\u180EArgument is missing')
            return
        embed = discord.Embed(colour=discord.Colour(0xc5b358))
        embed.set_thumbnail(url="http://i.imgur.com/biEvXBN.png")
        embed.add_field(name="\u180EAncient Oracle's inspiration", value="Read by: `xaos1502`", inline=True)
        embed.add_field(name='\u180EFor:', value=f'**{ctx.message.author.display_name}**', inline=True)
        embed.add_field(name='\u180EMessage:', value=f'{random.choice(magic_coin_oracle)}')
        await self.bot.say(embed=embed)
        dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
        log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
        user = ctx.message.author
        em = discord.Embed(title=f'{user.display_name}')
        em.colour = (discord.Colour(0xc5465d))
        em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
        em.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_chan, embed=em)


def setup(bot):
    bot.add_cog(Prediction(bot))

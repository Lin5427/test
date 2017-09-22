from __future__ import division
import asyncio
import discord
from   discord.ext import commands

from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
                    ZeroOrMore,Forward,nums,alphas,oneOf)
import math
import operator

__author__='Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__='''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__='''
This is a re-wrap of Paul McGuire's fourFn.py as a class, so it can 
be used easily in other places of the code. Most of the work wad done 
by corpnewt, all I did was clean it and create the results in embeds.
Also, the messages are deleted after, except for the correct answer.
'''

class NumericStringParserForPython3(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''
    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )
    def pushUMinus(self, strg, loc, toks ):
        if toks and toks[0]=='-':
            self.exprStack.append( 'unary -' )
    def __init__(self):
        point = Literal( "." )
        e     = CaselessLiteral( "E" )
        fnumber = Combine( Word( "+-"+nums, nums ) +
                        Optional( point + Optional( Word( nums ) ) ) +
                        Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        pi    = CaselessLiteral( "PI" )
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
                ).setParseAction(self.pushUMinus)
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( self.pushFirst ) )
        term = factor + ZeroOrMore( ( multop + factor ).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( ( addop + term ).setParseAction( self.pushFirst ) )
        self.bnf = expr
        epsilon = 1e-12
        self.opn = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = {
                "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}
    def evaluateStack(self, s ):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack( s )
        if op in "+-*/^":
            op2 = self.evaluateStack( s )
            op1 = self.evaluateStack( s )
            return self.opn[op]( op1, op2 )
        elif op == "PI":
            return math.pi
        elif op == "E":
            return math.e
        elif op in self.fn:
            return self.fn[op]( self.evaluateStack( s ) )
        elif op[0].isalpha():
            return 0
        else:
            return float( op )
    def eval(self,num_string,parseAll=True):
        self.exprStack=[]
        results=self.bnf.parseString(num_string,parseAll)
        val=self.evaluateStack( self.exprStack[:] )
        return val

class Calc:

    def __init__(self, bot):
        self.bot = bot
        self.nsp=NumericStringParserForPython3()


    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)


    @commands.command(aliases=['calc', 'maths'], pass_context=True, name="calculate", no_pm=True)
    async def calculate(self, ctx, *, formula = None):
        """ Do some math thanks to Paul McGuire's fourFn.py. """
        person = ctx.message.author
        crunching = await self.bot.send_message(ctx.message.channel, 'Analysing input . . .')

        if formula == None:
            await self.bot.delete_message(crunching)
            msg = '\u200BUse `{}calc [maths formula]`'.format(ctx.prefix)
            embed = discord.Embed(color=discord.Colour(0xc5342f))
            embed.description = f'{msg}'
            result = await self.bot.send_message(ctx.message.channel, embed=embed)
            dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
            log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
            user = ctx.message.author
            em = discord.Embed(title=f'{user.display_name}')
            em.colour = (discord.Colour(0xc5465d))
            em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
            em.set_thumbnail(url=user.avatar_url)
            await self.bot.send_message(log_chan, embed=em)
            await asyncio.sleep(6)
            await self.bot.delete_message(result)
            return

        try:
            answer=self.nsp.eval(formula)
        except:
            await self.bot.delete_message(crunching)
            msg = f'\N{THINKING FACE} **Robotsu** didn\'t understand **" {formula} "** input.\nTry any of these:'
            embed = discord.Embed(color=discord.Colour(0xc5342f))
            embed.description = f'\u200B{msg}'
            embed.add_field(name='multiplication', value="`num` * `num`", inline=True)
            embed.add_field(name='division', value="`num` / `num`", inline=True)
            embed.add_field(name='addition', value="`num` + `num`", inline=True)
            embed.add_field(name='rest', value="`num` - `num`", inline=True)
            embed.add_field(name='exponential', value="`num` ^ `num`")
            embed.add_field(name='integer', value="[`num` + `num` | `num` - `num`] `num` 0 `num`..`num` 9 `num` +")
            result = await self.bot.send_message(ctx.message.channel, embed=embed)
            dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
            log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
            user = ctx.message.author
            em = discord.Embed(title=f'{user.display_name}')
            em.colour = (discord.Colour(0xc5465d))
            em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
            em.set_thumbnail(url=user.avatar_url)
            await self.bot.send_message(log_chan, embed=em)
            await asyncio.sleep(15)
            await self.bot.delete_message(result)
            return

        msg = f'\u200B\N{BLACK HEART} {person.display_name}, {formula} = **`{round(answer, 2)}`**'
        embed = discord.Embed(color=discord.Colour(0xc5342f))
        embed.description = f'{msg}'
        await self.bot.delete_message(crunching)
        # deletes the crunching numbers message
        await self.bot.send_message(ctx.message.channel, embed=embed)
        dan_boru_bako = discord.utils.get(self.bot.servers, id='329814761661399041')
        log_chan = discord.utils.get(dan_boru_bako.channels, id='360683898201571331')
        user = ctx.message.author
        em = discord.Embed(title=f'{user.display_name}')
        em.colour = (discord.Colour(0xc5465d))
        em.description = f'<@!{user.id}> requested {ctx.command.name} using {ctx.command.invoked_with}'
        em.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_chan, embed=em)


def setup(bot):
    bot.add_cog(Calc(bot))

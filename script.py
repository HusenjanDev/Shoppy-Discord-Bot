import discord
from shoppy import shoppy_connection
from mysql_connector import mysql_connection
from discord.ext import commands
from datetime import datetime

# MySQL instance.
connection = mysql_connection(
   'user',
   '3306',
   'root',
   'password'
)

# Creating the database.
connection.create_database('shoppy')

# Creating the table for oders.
connection.create_table('shoppy', 'orders')

# Creating the connection.
shoppy = shoppy_connection('shoppy_api')

# Discord bot instance.
bot = commands.Bot(command_prefix = '.')

# Assist command.
@bot.command(name = 'assist')
@commands.has_role('Administrator')
async def nl_legit(ctx):
    embedVar = discord.embeds.Embed(title = '.assist',
            description = 'Hi, everyone!\n\nTo get access to the configuration you just purchased follow the following steps. Go to your email and then get the order id from the shoppy email you got and if you did not recieve a email from shoppy then get the invoice id from the paypal email and then use the following command.\n\n**Command:**\n.verify *order id or invoice id*', color=0xedc9f4)
        
    await ctx.channel.send(embed = embedVar)

    await ctx.message.delete()

# Remove-order command.
@bot.command(name = 'remove-order')
@commands.has_role('Administrator')
async def remove_order(ctx, *args):
    discord_username = str(ctx.author)
    order_id = str(args[0])

    connection.delete('shoppy', 'orders', order_id)

    embedVar = discord.embeds.Embed(title = '!remove-order',
        description = 'Hi, {0}\n\nThe user is removed from the database the user now can use the order id again.'.format(discord_username), color=0x1BE0E6)
    
    await ctx.channel.send(embed=embedVar, delete_after=8)

    await ctx.message.delete()

# Verify command.
@bot.command(name = 'verify')
async def verify(ctx, *args):
    # Discord username.
    discord_username = ctx.author

    # Discord id.
    discord_id = ctx.author.id

    # Order id.
    order_id = str(args[0])

    # Authorizing the order id.
    if len(order_id) > 0:
        shoppy_auth = shoppy.auth(order_id)
    else:
        embedVar = discord.embeds.Embed(title='ERROR', description="Hi, {0}!\n\nThere was an issue with your order id please contact Bhop#6641.".format(discord_username), color=0xe31010)
        await ctx.channel.send(embed=embedVar, delete_after=8)

    if len(shoppy_auth) == 3:

        if shoppy_auth[2] > "2021-09-19":

            mysql_auth = connection.auth('shoppy', 'orders', discord_username, discord_id, order_id, shoppy_auth[0])

            if mysql_auth == 0:
                
                if shoppy_auth[0] == "AIMWARE CONFIG":
                    role = discord.utils.get(discord_username.guild.roles, name="Aimware")
                    await discord_username.add_roles(role)

                if shoppy_auth[0] == "NEVERLOSE CONFIG":
                    role = discord.utils.get(discord_username.guild.roles, name="Neverlose")
                    await discord_username.add_roles(role)

                if shoppy_auth[0] == "GAMESENSE CONFIG":
                    role = discord.utils.get(discord_username.guild.roles, name="Gamesense")
                    await discord_username.add_roles(role)

                if shoppy_auth[0] == "LUCKYCHARMS CONFIG":
                    role = discord.utils.get(discord_username.guild.roles, name="LuckyCharms")
                    await discord_username.add_roles(role)

                if shoppy_auth[0] == "ONETAP CONFIG":
                    role = discord.utils.get(discord_username.guild.roles, name="Onetap")
                    await discord_username.add_roles(role)
                
                embedVar = discord.embeds.Embed(title=str("ORDER SUCCESFULL"), description="Hi, {0}!\n\nYou successfully got access to {1}'s configs!".format(discord_username, shoppy_auth[0]), color=0x92e310)
                await ctx.channel.send(embed=embedVar, delete_after=8)

                log_channel = bot.get_channel(889099730020347944)

                embedVar = discord.embeds.Embed(title='LOGS', description="The following user received access to the {0}.\n\n**Discord username:** {1}\n\n**Date:** {2}\n\n**Order id:** {3}".format(shoppy_auth[0], discord_username, datetime.now().strftime("%Y-%m-%d"), order_id), color=0x92e310)
                await log_channel.send(embed=embedVar)
            
            else:

                order = connection.get_order_information('shoppy', 'orders', order_id)

                embedVar = discord.embeds.Embed(title=str("ORDER ERROR"), description="Hi, {0}!\n\nYour account {1} already has access to the {2} config.".format(discord_username, str(order[0]), str(order[1])), color=0xe31010)
                
                await ctx.channel.send(embed=embedVar, delete_after=8)

        else:
            embedVar = discord.embeds.Embed(title=str("ORDER EXPIRED"), description="Hi, {0}!\n\nThe order id expired please contact an administrator for more information.".format(discord_username), color=0xe31010)
            
            await ctx.channel.send(embed=embedVar, delete_after=8)

    else:

        embedVar = discord.embeds.Embed(title='INVALID ORDER ID', description="Hi, {0}!\n\nThe purchase was either not successful or there is a issue occuring with the Shoppy API. Please contact Bhop#6641 for more information".format(discord_username), color=0xe31010)
        await ctx.channel.send(embed=embedVar, delete_after=8)
    
    await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command enter an valid command!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please pass all arguments!")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to use the following command!")

bot.run('discord_token')
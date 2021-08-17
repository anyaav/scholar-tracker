from discord.embeds import Embed
from discord.ext import commands
from utility.slicer import slice_mention
from utility.checkaddress import is_valid_address
import sqlscripts
import traceback
import discord

MESSEGE_EXECUTED_SUCCESFULLY="Query executed"
class AdminCommands(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.command(brief= "Add Scholars")
    @commands.has_guild_permissions(administrator=True)
    async def add_scholar(self,ctx,mention,address,cut):
        try:
            user = await self.client.fetch_user(int(slice_mention(mention)))
            if(is_valid_address(address)):
                sqlscripts.add_scholar(str(user),address,float(cut))
            else:
                raise TypeError("Incorrect Address")
            await ctx.send(MESSEGE_EXECUTED_SUCCESFULLY)
        except ValueError:
            await ctx.send("Incorrect format of mention")
        except TypeError:
            await ctx.send("Incorrect input")
  
    @commands.command(brief = "Shows the data of a scholar either by a mention or via an address")
    @commands.has_guild_permissions(administrator=True)
    async def scholar_data(self,ctx,target):
        temp=target
        try:
            user = await self.client.fetch_user(int(slice_mention(target)))
            target=str(user)
        except ValueError:
            target=temp
        sql_scholar_data = sqlscripts.get_scholar_data(target)
        if(len(sql_scholar_data)==0):
            await ctx.send("There is no such record in the database")
            return
        embed_data = discord.Embed(
            title = "Database"
        )
        for x in range(len(sql_scholar_data)):
            embed_data.add_field(name = "Name", value = sql_scholar_data[x][0], inline=True)
            embed_data.add_field(name = "Address", value=sql_scholar_data[x][1],inline=True)
            embed_data.add_field(name = "cut", value=sql_scholar_data[x][2],inline=True)

        await ctx.send(embed=embed_data)

    @commands.command(brief = "Shows all scholar data")
    @commands.has_permissions(administrator=True)
    async def all_scholar_data(self,ctx):
        sql_scholar_data = sqlscripts.get_all_scholar_data()
        if(len(sql_scholar_data)==0):
            await ctx.send("Database empty")
            return
        embed_data = discord.Embed(
            title = "Database"
        )
        for x in range(len(sql_scholar_data)):
            embed_data.add_field(name = "Name", value = sql_scholar_data[x][0], inline=True)
            embed_data.add_field(name = "Address", value=sql_scholar_data[x][1],inline=True)
            embed_data.add_field(name = "cut", value=sql_scholar_data[x][2],inline=True)
            
        await ctx.send(embed=embed_data)
    
    @commands.command(brief = "Delete a scholar via their address")
    @commands.has_permissions(administrator=True)
    async def delete_scholar(self,ctx,address):
        try:
            sqlscripts.delete_scholar(address)
            await ctx.send(MESSEGE_EXECUTED_SUCCESFULLY)
        except sqlscripts.QueryError:
            await ctx.send(MESSEGE_EXECUTED_SUCCESFULLY)
        except Exception:
            traceback.print_exc()

    @commands.command(brief = "Edits the cut percentage of a scholar either by address or a mention")
    @commands.has_permissions(administrator=True)
    async def edit_cut(self,ctx,target,change):
        temp=target
        try:
            user = await self.client.fetch_user(int(slice_mention(target)))
            target=str(user)
        except ValueError:
            target=temp
        except TypeError:
            await ctx.send("Incorrect input")

        try:
            sqlscripts.edit_cut(target,float(change))
            await ctx.send(MESSEGE_EXECUTED_SUCCESFULLY)
        except sqlscripts.QueryError:
            await ctx.send("Query failed")
        except TypeError:
            await ctx.send("Incorrect Input")
        except Exception:
            traceback.print_exc()

    @commands.command(brief = "Edits the name of the scholar via address")
    @commands.has_permissions(administrator=True)
    async def edit_name(self,ctx,address,name):
        try:
            user = await self.client.fetch_user(int(slice_mention(name)))
            name=str(user)
        except ValueError:
            await ctx.send("Name is not a mention")
        try:
            sqlscripts.edit_name(address,name)
            await ctx.send(MESSEGE_EXECUTED_SUCCESFULLY)
        except sqlscripts.QueryError:
            await ctx.send("Query failed")
        except TypeError:
            await ctx.send("Incorrect Input")
        except Exception:
            traceback.print_exc()

def setup(client):
    client.add_cog(AdminCommands(client))
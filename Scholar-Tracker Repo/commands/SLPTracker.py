import traceback
import discord
from utility.getSLPPrice import get_slp_data
from discord.ext import commands
from datetime import datetime

class track_slp(commands.Cog):
    
    def __init__(self,client):
        self.client=client

    @commands.command(brief = "Checks the current price of SLP")
    async def price(self,ctx):
        try:
            data=get_slp_data()
            dt_object = datetime.fromtimestamp(int(data["smooth-love-potion"]['last_updated_at']))
            embeds = discord.Embed(
                title = "Smooth Love Potion",
                description = "CoinGecko Price"
            )
            embeds.add_field(name="PHP",value = "₱"+str(data["smooth-love-potion"]['php']), inline=False)
            embeds.add_field(name="USD",value = "$"+str(data["smooth-love-potion"]['usd']), inline=False)
            embeds.add_field(name="24 hour change",value = str(data["smooth-love-potion"]['php_24h_change'])+"%", inline=False)
            embeds.add_field(name="last updated at:",value = dt_object, inline=False)

            embeds.set_thumbnail(url = 'https://d235dzzkn2ryki.cloudfront.net/smooth-love-potion_large.png')

            await ctx.send(embed=embeds)
        except Exception:
            traceback.print_exc()
def setup(client):
    client.add_cog(track_slp(client))
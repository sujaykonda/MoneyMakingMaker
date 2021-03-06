import sys

import discord
from dask.distributed import Client

from commands.bin import *
from commands.auction import *
from commands.bazaar import *
from commands.farming import *
from commands.bits import *


def ston(string):
    if str(string).endswith("b"):
        return float(str(string)[:-1]) * 1000000000
    elif str(string).endswith("m"):
        return float(str(string)[:-1]) * 1000000
    elif str(string).endswith("k"):
        return float(str(string)[:-1]) * 1000
    else:
        return float(str(string))


def ntos(num):
    if num >= 1000000000:
        return str(round(num / 10000000) / 100) + "b"
    elif num >= 1000000:
        return str(round(num / 10000) / 100) + "m"
    elif num >= 1000:
        return str(round(num / 10) / 100) + "k"
    else:
        return str(round(num * 10) / 10)


class MoneyMakingMaker(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.client = Client(threads_per_worker=2,
                             n_workers=3,
                             memory_limit='2GB')

    async def on_ready(self):
        print('Dask Client Link')
        print(self.client.dashboard_link)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    @staticmethod
    async def dm(author, embed):
        if author.dm_channel is None:
            await author.create_dm()

        await author.dm_channel.send(embed=embed)

    async def on_message(self, message):
        await self.message_handler(message)

    async def message_handler(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        msg = message.content.lower()
        if msg.startswith('m!'):
            ins = msg[2:].split()
            cmd = ins[0]
            if cmd == 'help':
                reply = discord.Embed(color=discord.Color.green())
                reply.add_field(name="m!farming",
                                value="Sends you profits from farming",
                                inline=False)
                reply.add_field(name="m!bzf",
                                value="Finds the highest profiting bazaar flip",
                                inline=False)
                reply.add_field(name="m!bf",
                                value="Finds the top 5 best bin flips",
                                inline=False)
                reply.add_field(name="m!af",
                                value="Finds the top 5 best auctions flips",
                                inline=False)
                await message.reply(embed=reply, mention_author=False)
            if cmd == 'farming':
                print("FARMING CALLED")
                await message.reply("Working on it", mention_author=False)
                farming_level = 0
                if len(ins) >= 2:
                    farming_level = ston(ins[1])
                farming_profits = farming(farming_level)

                reply = discord.Embed(color=discord.Color.green())
                for key in farming_profits.keys():
                    reply.add_field(name=key,
                                    value="Profit Per Hour: " + ntos(farming_profits[key]),
                                    inline=False)

                await MoneyMakingMaker.dm(message.author, reply)
            if cmd == 'bzf':
                print("BAZAAR FLIP CALLED")
                await message.reply("Working on it", mention_author=False)
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])

                flips = bazaar_flip(budget)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(len(flips)):
                    reply.add_field(name="Flip " + str(i + 1),
                                    value="Item: " + str(flips[i][0][0]) +
                                          "\nBuy Price: " + ntos(flips[i][0][1]) +
                                          "\nSell Price: " + ntos(flips[i][0][2]) +
                                          "\nMax Sold Per Min: " + ntos(flips[i][0][3]) +
                                          "\nMax Profit Per Min: " + ntos(flips[i][1]),
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)
            if cmd == 'bf':
                print("BIN FLIP CALLED")
                await message.reply("Working on it", mention_author=False)
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])

                flips = bin_flip(budget)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(15):
                    if len(flips) > i:
                        reply.add_field(name="Flip " + str(i + 1),
                                        value="Item: " + str(flips.iloc[i].name) +
                                              "\nBuying: " + ntos(flips.iloc[i].price) +
                                              "\nSelling: " + ntos(flips.iloc[i].price_next) +
                                              "\nProfit: " + ntos(flips.iloc[i].profit) +
                                              "\n/viewauction " + str(flips.iloc[i].uuid),
                                        inline=False)
                await MoneyMakingMaker.dm(message.author, reply)
                await message.reply("Done", mention_author=False)
            if cmd == 'af':
                print("AUCTION FLIP CALLED")
                await message.reply("Working on it", mention_author=False)
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])
                flips = auction_flip(budget)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(len(flips)):
                    reply.add_field(name="Flip " + str(i + 1),
                                    value="Item: " + str(flips[i][0][0]) +
                                          "\nBuying: " + ntos(flips[i][0][2]) +
                                          "\nSelling: " + ntos(flips[i][0][3]) +
                                          "\nProfit: " + ntos(flips[i][1]) +
                                          "\n/viewauction " + str(flips[i][0][1]),
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)
            if cmd == 'bits':
                await message.reply("Working on it", mention_author=False)
                bits = 50000
                if len(ins) >= 2:
                    bits = ston(ins[1])
                total_profit, best_items = bestbits(bits)
                reply = discord.Embed(color=discord.Color.green())
                reply.add_field(name="Total Profit", value=str(total_profit), inline=False)
                for key in best_items.keys():
                    reply.add_field(name=key,
                                    value="Num Items: " + str(best_items[key]),
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)


if __name__ == '__main__':
    client = MoneyMakingMaker()
    print(sys.argv[1])
    client.run(sys.argv[1])

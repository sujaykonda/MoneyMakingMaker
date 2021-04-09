from dask.distributed import Client, progress
import sys
import discord
from bin import *
from auction import *
from bazaar import *
from farming import *


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
            if cmd == 'farming':
                message.reply("Working on it")
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
                message.reply("Working on it")
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])

                flips = bazaar_flip(budget)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(len(flips)):
                    reply.add_field(name="Flip " + str(i+1),
                                    value="Item: " + str(flips[i][0]) +
                                          "\nProfit Per Min: " + ntos(flips[i][1]),
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)
            if cmd == 'bf':
                message.reply("Working on it")
                item_limit = 20
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])
                if len(ins) >= 3:
                    item_limit = ston(ins[2])

                flips = bin_flip(budget, item_limit)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(len(flips)):
                    reply.add_field(name="Flip " + str(i+1),
                                    value="Item: " + str(flips[i][0][0]) +
                                          "\nProfit: " + ntos(flips[i][0][2]) +
                                          "\n/ah " + requests.get(
                                        "https://api.mojang.com/user/profiles/" + flips[i][0][1] + "/names").json()[-1][
                                              "name"],
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)
            if cmd == 'af':
                message.reply("Working on it")
                item_limit = 20
                budget = 1000000
                if len(ins) >= 2:
                    budget = ston(ins[1])
                if len(ins) >= 3:
                    item_limit = ston(ins[2])
                flips = auction_flip(budget, item_limit)
                reply = discord.Embed(color=discord.Color.green())
                for i in range(len(flips)):
                    reply.add_field(name="Flip " + str(i+1),
                                    value="Item: " + str(flips[i][0][0]) +
                                          "\nProfit: " + ntos(flips[i][0][2]) +
                                          "\n/ah " + requests.get(
                                        "https://api.mojang.com/user/profiles/" + flips[i][0][1] + "/names").json()[-1][
                                              "name"],
                                    inline=False)
                await MoneyMakingMaker.dm(message.author, reply)


if __name__ == '__main__':
    client = MoneyMakingMaker()
    print(sys.argv[1])
    client.run(sys.argv[1])

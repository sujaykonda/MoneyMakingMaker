# Hypixel Skyblock

## What is the Game?
Hypixel Skyblock is a economy based game.  
It uses the auction house for trading small amount of items like weapons, armor, etc.
It also uses the bazaar for trading large amounts of items like ores, crops, enemy drops, etc.
Skyblock is also skill based, meaning fighting enemies, mining ores, farming crops and enchanting items will increases skill levels.  
The goal of the game is too beat all of the mobs in the game and to max out all of your skills.  
This means you want all of the best gear, so you need money to buy the gear or you need to get the gear normally.  
Usually its easier to just buy the gear, so you want a fast method to make money.

# MoneyMakingMaker

### LINK: https://discord.gg/5fbHZFG5u4

## Flipping
Flipping is buying things for low and then selling them for high to make profits.
There are 3 types of flipping in the game,
- Bazaar Flipping - This means putting a buy order for a large amount of items for a low price and then put a sell order of the items for a higher price. Usually flipping one item in the bazaar is useless, since the bazaar is for items that are common meaning they are pretty cheap.  
- Auction Flipping - Auctioning a item is similar to the real world. You can set a minimum price and people can bid on your item that is selling. Sometimes not many people bid on a item and the item is really cheap compared to the normal price, so you can bid on it in hopes of winning the item and you can sell it in BIN (Buy it now) which will be explained in the next flip technique.
- Bin Flipping - Buy It Now or BIN means that someone can directly buy the item for a set price, meaning there is no bidding involved. To bin flip you buy a item that is being sold/binned for the lowest price and then put it up as bin in the second lowest bin price.

## Margins
There are two types of margins. Percentage margins and normal margins. Margins is the difference in price when you flip. For example the normal margins in BIN Flipping is the difference of the lowest bin to the second lowest bin. The normal margins in Bazaar Flipping is the difference between the buy order price and the sell order price. Flipping is all about the margins. Since the margins is essentially how much you will make, people usually care about normal margins. There is also percent margins. This is the percentage of the normal margin to the buy price. This also matters because if you flip alot of the same item which a high percent margin you can essentially multiply your money by the percent margin.

## The Problem: Find Good Flipping Oppurtunities
Good means that you are maximizing the profit per minute. The factors in maximizing the profit per minute is the demand at the sell price and the margin.


## How To Find Flipping Oppurtunities
Instead of looking through it, we used the hypixel api, which is a api in json form that looks like this:  
![image](https://user-images.githubusercontent.com/50930165/114272105-b1d33680-99e2-11eb-94f4-addda9402cba.png)
It may look like garbage at first, but in there we have every single auction and alot of data on said auctions.  
We looped through all of the auctions and put them in groups using the ITEM_ID feature (This is in the weird string called item_bytes which you can decode)  
Next we sorted it by price and found the lowest two items and subtract, getting you the margin of that item.
You find the top margin item, and that is the item you want to flip.
This doesn't seem too difficult, until you realize it takes alot of time to decode these item_bytes AND the profit cannot be the only way you decide flips.  
If you rely on profit only, you may buy obscure items which take extremly long to sell or the second lowest item in the auction house may be way overpriced if you look at history. These problems can be formulated into math, which is used in the bot.
It is similar with bazaar flipping. The margins will be the difference in sell order and buy order. You also want to multiply that with the buy demand, (how many people are buying buy orders). This also has a similar problem. The demand will change because when margins are high, less people will buy the sell orders since the sell orders are overpriced and vice versa.
## Formulating the problem

## Current Features
- Auction Flipping - Snipe an auction for a less price and sell for lowest price bin
- Bin Flipping - Buy the lowest bin and sell for second/new lowest bin
- Bazaar Flipping - Buy order items and then sell order the items
- Farming Profits - Displays all farming profits

## Next Features
1. Optimal Value Function for Bin/Auction Flipping
2. Optimal Way to sell bits
3. Essence Flipping

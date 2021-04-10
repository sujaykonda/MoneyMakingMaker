# Hypixel Skyblock

## What is the Game?
Hypixel Skyblock is a economy based game.  
It uses the auction house for trading small amount of items like weapons, armor, etc.
It also uses the bazaar for trading large amounts of items like ores, crops, enemy drops, etc.
Skyblock is also skill based, meaning fighting enemies, mining ores, farming crops, enchanting items increase levels.  
The goal of the game is too beat all of the mobs in the game and to max out all of your skills.  
This means you want all of the best gear, so you need money to buy the gear or you need to get the gear normally.  
Usually its easier to just buy the gear, you want a fast method to make money, which will be talked about in the next section.

# MoneyMakingMaker

### LINK: https://discord.gg/DYcPtcTc4T  

## The Flipping Problem
Flipping is buying things for low and then selling them for high to make profits.
There are 3 types of flipping,
- Bazaar Flipping - This means buying ordering large amount of items for a low price and then sell ordering the items for a higher price. Usually flipping one item in the bazaar is useless, since the bazaar is for items that are common meaning they are pretty cheap.  
- Auction Flipping - Auctioning a item is similar to the real world. You can set a minimum price and people can bid on your item that is selling. Sometimes not many people bid on the item and the item is really cheap, so you can bid on it in hopes of winning the item and you can sell it in BIN (Buy it now) which will be explained in the next flip
- Bin Flipping - Buy It Now or BIN means that someone can directly buy the item for a set price, meaning there is not bidding involved. To bin flip you buy a item that is being sold/binned for the lowest price and then put it up as bin in the second lowest price.
All of these flips require looking through enourmous amounts of data and picked the best flip out of all of the items. In bazaar flipping, that is relatively possible, due to only have a selection of items that you can sell. Still, it is hard to make decisions without using math to see which is the best flip. In Auction/Bin Flipping, you have to go through the ENTIRE auction house. This includes around 66000 at non peak times. There is no physical way that a human can look through all of these auctions. 

## How We Solved it
Instead of looking through it, we used the hypixel api, which is a api in json form that looks like this:  
![image](https://user-images.githubusercontent.com/50930165/114272105-b1d33680-99e2-11eb-94f4-addda9402cba.png)
It may look like garbage at first, but in there we have every single auction and alot of data on said auctions.  
We looped through all of the auctions and put them in groups using the ITEM_ID feature (This is in the weird string called item_bytes which you can decode)  
Next we sorted it by price and found the lowest two items and subtract, getting you the flips profit.  
This doesn't seem too difficult, until you realize it takes alot of time to decode these item_bytes AND the profit cannot be the only way you decide flips.  
If you rely on profit only, you may buy obscure items which take extremly long to sell or the second lowest item in the auction house may be way overpriced if you look at history.  

## Current Features
- Auction Flipping - Snipe an auction for a less price and sell for lowest price bin
- Bin Flipping - Buy the lowest bin and sell for second/new lowest bin
- Bazaar Flipping - Buy order items and then sell order the items
- Farming Profits - Displays all farming profits

## Next Features
1. Optimal Value Function for Bin/Auction Flipping
2. Optimal Way to sell bits
3. Essence Flipping

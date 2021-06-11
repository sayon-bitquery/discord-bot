import discord 
import os
import requests 
import random

client = discord.Client()
BITQUERY_API_KEY = os.getenv('BITQUERY_API_KEY')

# --------------------- BITQUERY GRAPHQL API -------------------------
def run_query(query):  
    headers = {'X-API-KEY': BITQUERY_API_KEY}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))


# The GraphQL query

query = """
{
  ethereum(network: bsc) {
    dexTrades(
      baseCurrency: {is: "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"}
      quoteCurrency: {is: "0x55d398326f99059ff775485246999027b3197955"}
      options: {desc: ["block.height", "transaction.index"], limit: 1}
    ) {
      block {
        height
        timestamp {
          time(format: "%Y-%m-%d %H:%M:%S")
        }
      }
      transaction {
        index
      }
      baseCurrency {
        symbol
      }
      quoteCurrency {
        symbol
      }
      quotePrice
    }
  }
}
"""

result = run_query(query)  # Execute the query
quotePrice = result.get('data').get('ethereum').get('dexTrades')[0].get('quotePrice') 
# --------------------------------------------------------------------

hello_messages = ['Hi', 'Hello', 'Heyy', 'hey', 'Hey', 'hello', 'heyya', 'hi']

messages = ['BSC','CAKE/USDT', 'Binance', 'price', 'Price', 'prices', 'Prices', 'binance', 'cake', 'usdt', 'bsc', 'Binance Smart Chain Mainnet', 'mainnet']

thank_you = ['Thanks', 'Thnx', 'Thank You', 'Thank you', 'thanks', 'thank you', 'thnx', 'cool', 'great', 'nice', 'ok', 'Thaanks', 'Alright', 'sweet', 'Noice', 'noice', 'awesome', 'good', 'Good']

thank_you_messages = ['It was a pleasure to help you', 'I hope I was able to solve your primary purpose', 'I guess you got what you wanted', 'It was my duty to keep you updated with the prices','The prices for CAKE/USDT on Binance Smart Chain Mainnet (BSC) protocol is up to date', 'I just updated you with the prices for CAKE/USDT on the BSC protocol', 'Thank you for using Bitquery.io']

@client.event
async def on_ready():
  print("Bitquery bot up and running with {0.user} as the user".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return 

  if message.content.startswith('$hello') or message.content.startswith('$hey') or message.content.startswith('$hi'):
    await message.channel.send('Heyy! welcome to Bitquery Updated Coin Price server. I am Bitquery Bot and I am here to provide you with the price updates for CAKE/USDT on Binance Smart Chain Mainnet (BSC) protocol.')

  if any(word in message.content for word in thank_you):
    await message.channel.send(random.choice(thank_you_messages))

  if any(word in message.content for word in messages):
    await message.channel.send("The price is {}".format(quotePrice))

  if any(word in message.content for word in hello_messages):
    await message.channel.send('Heyy! welcome to Bitquery Updated Coin Price server. I am Bitquery Bot and I am here to provide you with the price updates for CAKE/USDT on Binance Smart Chain Mainnet (BSC) protocol.')

client.run(os.getenv('TOKEN'))



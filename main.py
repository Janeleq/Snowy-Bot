from ast import Await
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import random
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')
print(f"Bot started ({TOKEN})") #debugging to check if Token is successfully retrieved

client = discord.Client()
bot = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'({channel}){username}: {user_message}')

    # so that bot does not respond to itself
    if message.author == client.user:
        return

    if user_message.lower() == "snowy":
        await message.channel.send(f"""Here are some of the commands you can use off me :dog:
        **snowy** - list of commands that i can do :smile:
        **hello** - greetings! :wave: 
        **depression** - same. :sob:
        **treats** - give me treats :yum: 
        **attack (name)** - attack that person :knife:
        **snowy pics** - get some picture of me! :frame_photo:""")
        return

    if message.channel.name == 'meow':
        user_message = user_message.lower()
        owner = ["dream", "aloysius"]

        if user_message.lower() == "hello":
            await message.channel.send(f"Hello {username}, I am Aloysius's pet dog :dog: !")
            return

        if user_message.lower() == "depression":
            await message.channel.send(f"nice! @{username}")
            return

        if user_message.lower() == "treats":
            await message.channel.send(f"love me some treats :bacon: :) {username}")
            return

        if "attack" in user_message:
            person_attacked = user_message.split(" ")[1]
            rand_attack = random.randint(5,101)

            if(person_attacked in owner):
                await message.channel.send(f"IT'S YOU {owner}! I recognised that you are my owner. I will not scratch you :(")
            else:
                await message.channel.send(f"I used my puppy claws and scratched {person_attacked}! \n HP - {rand_attack}")

        if user_message.lower() == "snowy pics":
            pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg", "pic5.jpg", "pic6.jpg", "pic7.jpg", "pic8.jpg", "pic9.jpg"]

            random_picture = random.randint(0, len(pictures)-1)
            choosen_picture = pictures[random_picture]

            await message.channel.send("Here is a cute picture of me!", file=discord.File('images/'+ choosen_picture))
            return

    if message.channel.name == 'general':
        if user_message.lower() == "hello":
            await message.channel.send(f"Hello {username}, I am Aloysius's pet dog :dog: !")
            return
        if user_message.lower() == "depression":
            await message.channel.send(f"nice! @{username}")
            return

        if user_message.lower() == "snowy pics":
            pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg", "pic5.jpg", "pic6.jpg", "pic7.jpg", "pic9.jpg"]

            random_picture = random.randint(0, len(pictures)-1)
            choosen_picture = pictures[random_picture]

            await message.channel.send("Here is a cute picture of me!", file=discord.File('images/'+ choosen_picture))
            return

@bot.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    print(user, wallet_amt, bank_amt)
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name ="Bank Balance", value=bank_amt)
    await ctx.send(embed = em)

# give someone pet's closeness
@bot.command()
async def beg(ctx):
    await open_account(ctx.author)  
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(20, 101)
    
    await ctx.send(f"Someone gave you {earnings} closeness!")

    users[str(user.id)]["wallet"] += earnings

    with open("closeness.json", "w") as f:
        json.dump(users, f)

#helper functions 
async def open_account(user):
    users = await get_bank_data()
    
    # if user already have a account
    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("closeness.json", "w") as f:
        json.dump(users, f)

    return True

async def get_bank_data(): 
    with open("closeness.json", "r") as f:
        users = json.load(f)

    return users


client.run(TOKEN)
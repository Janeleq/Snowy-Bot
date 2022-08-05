from fileinput import close
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands, tasks
from itertools import cycle
import asyncio
import random
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')
print(f"Bot started ({TOKEN})") #debugging to check if Token is successfully retrieved

# client = discord.Client()
statuses = cycle(["having fun!", "admiring the sunset :sunglasses:", "sleeping time :zzz:"])

@tasks.loop(hours = 8)
async def status_swap():
    await bot.change_presence(activity=discord.Game(name=next(statuses)))

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    status_swap.start()
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
   # so that bot does not respond to itself
    if message.author == bot.user:
        return

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    #logs
    print(f'({channel}){username}: {user_message}')


    if user_message.lower() == "snowy":
        await message.channel.send(f"""Here are some of the commands you can use off me :dog:
    __General__
    **snowy** - list of commands that i can do :smile:
    **hello** - greetings! :wave: 
    **depression** - same. :sob:
    **attack (name)** - attack that person :knife:
    **snowy pics** - get some picture of me! :frame_photo:\n
    __Commands__
    **!closeness** - check your closeness level with snowy and your amount of treats available (still in the making)
    **!beg** - get some treats from random stranger)
    **!treats** - give me a randomized amount of treats :yum:""")
        return

    if message.channel.name == 'meow' or 'general':
        user_message = user_message.lower()
        owner = ["dream", "aloysius"]

        if user_message.lower() == "hello":
            await message.channel.send(f"Hello {username}, I am Aloysius's pet dog :dog: !")
            return

        if "depression" in user_message:
            await message.channel.send(f"nice! @{username}")
            return

        if user_message.startswith('attack'):
            person_attacked = user_message.split(" ")[1].lower()
            rand_attack = random.randint(10,101)

            if(person_attacked in owner):
                await message.channel.send(f"IT'S YOU {person_attacked}! I recognised that you are my owner. I will not bite you :(")
            else:
                await message.channel.send(f"I used my puppy claws and scratched {person_attacked}! \n HP - {rand_attack}")

        if user_message.lower() == "snowy pics":
            pictures = ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg", "pic5.jpg", "pic6.jpg", "pic7.jpg", "pic8.jpg", "pic9.jpg"]

            random_picture = random.randint(0, len(pictures)-1)
            choosen_picture = pictures[random_picture]

            await message.channel.send("Here is a cute picture of me!", file=discord.File('images/'+ choosen_picture))
            return
        # for bot to process commands
        await bot.process_commands(message)

@bot.command(aliases=['closenesss', 'snowy closeness'])
async def closeness(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    treat_amt = users[str(user.id)]["treats"]
    closeness_amt = users[str(user.id)]["closeness"]

    print(user, treat_amt, closeness_amt)
    em = discord.Embed(title = f"{ctx.author.name}'s balance", color=discord.Color.red())
    em.add_field(name="Treats Balance:bacon:", value=treat_amt)
    em.add_field(name ="Snowy Closeness:dog:", value=closeness_amt)
    await ctx.send(embed = em)

@bot.command()
async def treats(ctx):
    await open_account(ctx.author)  
    username = str(ctx.author).split('#')[0]
    users = await get_bank_data()
    user = ctx.author
    treats_amt = random.randint(20, 120)

    treats_acceptance = [True, False]
    random_status = random.randint(0,2)
    
    choosen_status = treats_acceptance[random_status]
  
    
    # If pet decide to accept the treats,
    if choosen_status:
         users[str(user.id)]["treats"] -= treats_amt
         users[str(user.id)]["closeness"] += treats_amt
         closeness = users[str(user.id)]["closeness"]
         with open("closeness.json", "w") as f:
            json.dump(users, f)

         await ctx.channel.send(f"love me some treats :bacon:, {username} :)\nYou have given Snowy {treats_amt} treats!\nYour closeness with Snowy is now at {closeness}.")

    else:
        #  users[str(user.id)]["treats"] -= treats_amt
         users[str(user.id)]["closeness"] -= treats_amt
         with open("closeness.json", "w") as f:
            json.dump(users, f)

         await ctx.channel.send(f"Snowy has sadly denied your treats :(, {username}\nYour closeness with Snowy has reduced by {treats_amt}.")

    return

# give someone pet's closeness
@bot.command()
async def beg(ctx):
    await open_account(ctx.author)  
    users = await get_bank_data()
    user = ctx.author

    earn_treats = random.randrange(20, 101)
    
    await ctx.send(f"Someone gave you {earn_treats} treats!")

    users[str(user.id)]["treats"] += earn_treats

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
        users[str(user.id)]["treats"] = 0
        users[str(user.id)]["closeness"] = 0

    with open("closeness.json", "w") as f:
        json.dump(users, f)

    return True

async def get_bank_data(): 
    with open("closeness.json", "r") as f:
        users = json.load(f)

    return users

            
# client.run(TOKEN)
bot.run(TOKEN)
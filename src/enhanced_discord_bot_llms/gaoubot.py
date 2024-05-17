#!/usr/bin/env python3

import os
import random

import discord

from asyncio import sleep

from discord.ext import commands, tasks

from enhanced_discord_bot_llms.constants import (
    WORDS_THE_BOT_DONT_LIKE,
    FROWNING_FACE_EMOJI,
)
from enhanced_discord_bot_llms.llm_svc import (
    gen_client,
    usine_de_gaou_creation,
    gen_async_client,
    streaming_usine_de_gaou_creation,
    LLMModel,
    streaming_gaou_formula,
)

intents = discord.Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents)


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    try:
        content = message.content.lower()
        for word in WORDS_THE_BOT_DONT_LIKE:
            if word in content:
                await sleep(10)
                await message.channel.send(
                    f"{message.author.mention} Hey! Do not use that word again {FROWNING_FACE_EMOJI}"
                )
                await message.channel.send(
                    f"{message.author.mention} You called me: {word} and I don't like it. I've deleted your message."
                )
                await sleep(10)
                await message.delete()
    except Exception as e:
        print(f"Error: {e}")

    if message.content == "pingGG":
        await message.channel.send("pongGG")
        return

    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return

    if after.content == "ping":
        await after.channel.send("pong")
        return

    await bot.process_commands(after)


@bot.command()
@commands.guild_only()
async def ping(ctx: commands.Context):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)

    ?ping
    """
    await ctx.reply("pong")


@bot.command()
@commands.guild_only()
async def new_gaou(ctx: commands.Context, parametre: str):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)
    parametre: str (message to send to the model)

    ?new_gaou "I am not a Gaou named Lambert who is 15 years old and is intelligent."
    """
    model = LLMModel.GPT4_Omni
    # model = LLMModel.LLAMA3
    try:
        client = gen_async_client(model=model)
        gueou = await streaming_usine_de_gaou_creation(client, parametre, model=model)
        await ctx.reply(f"""
```json
    
{gueou.model_dump_json(
    indent=4
)}
```
""")
    except Exception as e:
        print(f"Error: {e}")
        await ctx.reply(f"An error occurred: {e}")


@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_messages=True)
async def cleanup(ctx: commands.Context, limit: int):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)
    limit: int (number of messages to delete)

    ?cleanup 10
    """
    await delete_messages(ctx, limit)


@bot.command()
@commands.dm_only()
async def dm_cleanup(ctx: commands.Context, limit: int):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)
    limit: int (number of messages to delete)

    ?dm_cleanup 10
    """
    await delete_messages(ctx, limit)


async def delete_messages(ctx: commands.Context, limit: int):
    print(f"Cleaning up: {limit} messages...")
    async for msg in ctx.channel.history(limit=limit):
        try:
            print(f"Deleting message: {msg.content}")
            await sleep(1)
            await msg.delete()
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply(f"You may not have permission to delete messages.")
            continue


@tasks.loop(minutes=16)
async def my_background_gaou_tasks():
    await bot.change_presence(activity=discord.Game(name="With Gaous"))
    # members = [[member for member in guild.members] for guild in bot.guilds]
    # members = bot.get_all_members()
    channels = bot.get_all_channels()
    for chnl in channels:
        if isinstance(chnl, discord.TextChannel) and chnl.name == "botexperiments":
            await chnl.send(
                f"Who's Gaou anyway? Me Gaou? Think again... {chnl.mention}"
            )
            chnl_members = chnl.members
            for chnl_m in chnl_members:
                if chnl_m.bot:
                    continue
                elif (
                    "african" in chnl_m.name.lower()
                    or "dog" in chnl_m.name.lower()
                    or "lle" in chnl_m.name.lower()
                    or "bru" in chnl_m.name.lower()
                ):
                    await sleep(8)
                    # model = random.choice(
                    #     [model.value for model in LLMModel]
                    # )  # Choose a model at random
                    model = LLMModel.Claude3
                    client = gen_async_client(model=model)
                    gueou_joke = await streaming_gaou_formula(
                        client, chnl_m.display_name, model=model
                    )
                    # message_to_gueou = f"{gueou_joke.friend_gaou_joke} ({gueou_joke.language.name} => {gueou_joke.language.value}) {chnl_m.mention}"
                    message_to_gueou = f"{gueou_joke.friend_gaou_joke} ({gueou_joke.language.value}) {chnl_m.mention}"
                    await chnl.send(message_to_gueou)


@my_background_gaou_tasks.before_loop
async def before_gueou():
    await bot.wait_until_ready()
    print("Ready for Gaous!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    my_background_gaou_tasks.start()


if __name__ == "__main__":
    token = os.environ["DISCORD_BOT_TOKEN"]
    bot.run(token)

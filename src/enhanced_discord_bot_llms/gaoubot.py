#!/usr/bin/env python3

import os
import discord

from asyncio import sleep

from discord.ext import commands

from enhanced_discord_bot_llms.llm_svc import (
    gen_client,
    usine_de_gaou_creation,
    gen_async_client,
    streaming_usine_de_gaou_creation,
    LLMModel,
)

intents = discord.Intents.default()
intents.typing = False
intents.messages = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="?", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


BAD_WORDS = ["slur1", "slur2", "swear1"]


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    content = message.content.lower()
    for word in BAD_WORDS:
        if word in content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} Please do not use that word."
            )

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

    !ping
    """
    await ctx.reply("pong")


@bot.command()
@commands.guild_only()
async def new_gaou(ctx: commands.Context, parametre: str):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)
    parametre: str (message to send to the model)

    !new_gaou "I am not a Gaou named Lambert who is 15 years old and is intelligent."
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

    !cleanup 10
    """
    await delete_messages(ctx, limit)


@bot.command()
@commands.dm_only()
async def dm_cleanup(ctx: commands.Context, limit: int):
    """
    ctx: Context (discord.ext.commands.Context, information about the command)
    limit: int (number of messages to delete)

    !dm_cleanup 10
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


if __name__ == "__main__":
    token = os.environ["DISCORD_BOT_TOKEN"]
    bot.run(token)

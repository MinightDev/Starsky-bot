import discord
from discord.ext import commands
import requests
import urllib.parse
import asyncio
import os
import aiohttp
import random
import base64
import io

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.reactions = True

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

API_URL = 'https://starsky.pro/api/v1/documents'
ACCOUNT_URL = 'https://starsky.pro/api/v1/account'
API_KEY = None

template_list = {
    1: "Freestyle",
    2: "About us",
    3: "Advertisement",
}

document_counter = 1

async def get_user_account():
    global API_KEY 
    if API_KEY:
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Accept': 'application/json'
        }
        response = requests.get(ACCOUNT_URL, headers=headers)
        if response.status_code == 200:
            account_info = response.json().get('data', None)
            return account_info
    return None

@bot.event
async def on_ready():
    print('Starsky is ready!')
    await bot.change_presence(activity=discord.Game(name="✨ Starsky.pro"))

async def fetch_document_details(document_id):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(f'{API_URL}/{document_id}', headers=headers)
    if response.status_code == 200:
        document = response.json()
        return document
    return None

bot.remove_command('help')


user_image_limit = 10 # number img generations per user
user_image_counter = {}

@bot.command()
async def image(ctx, *, prompt):
    user_id = ctx.author.id
    if user_id not in user_image_counter:
        user_image_counter[user_id] = 0

    if user_image_counter[user_id] >= user_image_limit:
        embed = discord.Embed(title="Image Generation Limit Reached", description="You have reached the maximum limit for generated images. Please upgrade by clicking [Here](https://starsky.pro/pricing).", color=discord.Color.brand_red())
        await ctx.send(embed=embed)
        return

    user_image_counter[user_id] += 1

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'prompt': prompt,
        'name': 'Generated Image',
        'description': prompt,
        'resolution': '1024x1024', #the higher the better
    }

    response = requests.post('https://starsky.pro/api/v1/images', headers=headers, data=payload)

    if response.status_code == 201:
        image_id = response.json().get('data', {}).get('id')

        # Fetch image details
        image_details_response = requests.get(f'https://starsky.pro/api/v1/images/{image_id}', headers=headers)
        if image_details_response.status_code == 200:
            image_details = image_details_response.json().get('data', {})

            image_url = image_details.get('url', '')
            image_result = image_details.get('result', '')

            embed = discord.Embed(title="Starsky Bot Image Generator", color=discord.Color.brand_red())
            embed.add_field(name="Prompt:", value=prompt, inline=False)

            if image_url:
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to fetch the generated image.")
        else:
            await ctx.send("Failed to fetch image details.")
    else:
        await ctx.send("Image generation failed. Please try again.")

    if not API_KEY:
        await ctx.send("API key is not valid. Please run `$setup` to provide a valid API key.")


@bot.command()
async def account(ctx):
    account_info = await get_user_account()

    if account_info:
        account_name = account_info.get('name', 'Unknown')
        plan_name = account_info.get('plan', {}).get('name', 'Unknown')
        total_words = account_info.get('plan', {}).get('features', {}).get('words', 0)
        used_words = account_info.get('words_month_count', 0)

        embed = discord.Embed(title="Account Information", color=discord.Color.brand_red())
        embed.add_field(name='**Account Name**', value=account_name, inline=False)
        embed.add_field(name='**Plan Name**', value=plan_name, inline=False)
        embed.add_field(name='**Total Words**', value=total_words, inline=False)
        embed.add_field(name='**Used Words**', value=used_words, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to get user account information. Please make sure to provide a valid API key using $setup.")

@bot.command()
async def templates(ctx, template_id: int = None):
    if template_id is None:
        embed = discord.Embed(title="Available Templates", color=discord.Color.brand_red())
        for template_id, template_name in template_list.items():
            embed.add_field(name=f"**{template_id}. {template_name}**", value="Use `$templates [template_id]` to create a new document with this template.", inline=False)
        await ctx.send(embed=embed)
        return

    if template_id not in template_list:
        await ctx.send("Invalid template ID. Please choose a valid template.")
        return

    template_name = template_list[template_id]

    global document_counter
    document_name = f"Untitled ({document_counter})"
    document_counter += 1

    account_info = await get_user_account()
    if not account_info:
        await ctx.send("Failed to get user account information. Please make sure to provide a valid API key using $setup.")
        return

    total_words = int(account_info.get('plan', {}).get('features', {}).get('words', 0))
    used_words = int(account_info.get('words_month_count', 0))

    if used_words >= total_words:
        subscription_url = 'https://starsky.pro/pricing'
        await ctx.send(f"You have exceeded your plan's word limit. Please upgrade your plan [here]({subscription_url}).")
        return

    await ctx.send(f"Please enter your prompt for the **\"{template_name}\"** document. (You have {total_words - used_words} words left in your plan):")
    prompt = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    if len(prompt.content.split()) > (total_words - used_words):
        await ctx.send(f"You have exceeded your plan's word limit. Please enter a shorter prompt.")
        return

    payload = {
        'name': document_name,
        'prompt': prompt.content,
        'creativity': 0.5,  # Assuming default creativity level
        'template_id': template_id
    }

    encoded_payload = urllib.parse.urlencode(payload).encode('utf-8')

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(API_URL, headers=headers, data=encoded_payload)
    if response.status_code == 201:
        created_document = response.json()
        document_id = created_document.get('data', {}).get('id')

        print("Document successfully created. Fetching document details...")
        fetched_document = await fetch_document_details(document_id)

        if fetched_document:
            result = fetched_document.get('data', {}).get('result', "No result available.")

            embed = discord.Embed(title=f"**Document ID:** {document_id}", color=discord.Color.brand_red())
            embed.add_field(name='**Name**', value=document_name, inline=False)
            embed.add_field(name='**Result**', value=result, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Error fetching document details. Please try again later.")
    else:
        await ctx.send(f"Error storing document. The Starsky API returned an unexpected status code: {response.status_code}.")

@bot.command()
async def setup(ctx):
    await ctx.send("Please enter your Starsky API key:")

    def check_author(m):
        return m.author == ctx.author

    try:
        message = await bot.wait_for('message', check=check_author, timeout=60)
        api_key = message.content.strip()

        # Validate the API key
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        }
        response = requests.get(ACCOUNT_URL, headers=headers)

        if response.status_code == 200:
            global API_KEY
            API_KEY = api_key
            await ctx.send("API key is valid. You can now use the bot.")
        else:
            await ctx.send("Invalid API key. Please make sure to provide a valid API key. If you don't have one, you can get it from https://starsky.pro/api.")
    except asyncio.TimeoutError:
        await ctx.send("Setup timed out. Please run $setup again to provide your API key.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Starsky Bot Help", description="Here are the available commands:", color=discord.Color.brand_red())
    embed.add_field(name="$account", value="Get information about your Starsky account.", inline=False)
    embed.add_field(name="$templates [template_id]", value="Select a template and create a new document.", inline=False)
    embed.add_field(name="$image [prompt]", value="Generate images using starsky ai.", inline=False)
    embed.add_field(name="$setup", value="Set up your Starsky API key.", inline=False)
    await ctx.send(embed=embed)

bot.run('YOUR TOKEN GOES HERE')
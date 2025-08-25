import os
from dotenv import load_dotenv
import discord
from portcheck import check_server
from generatechannel import generate_channel

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

CHANNEL_ID = 1409185592541188312

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    
    status = check_server()
    channel = await client.fetch_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found!")
        await client.close()
        return

    # Generate channel name and normalize
    new_name = generate_channel(status).strip()
    current_name = channel.name.strip()
    
    if current_name != new_name:
        await channel.edit(name=new_name)
        print(f"Channel name changed to {new_name}")
    else:
        print("Channel name already up-to-date, no edit needed.")

    # Prepare embed based on server status
    if "error" not in status:
        players_list = ", ".join(status['online_players']) if status['online_players'] else "No players online"
        embed = discord.Embed(
            title="🎮 Server Status",
            description=f"Server is **online!** :green_circle:",
            color=discord.Color.green()
        )
        embed.add_field(name="Map", value=f"🗺️ {status['map']}", inline=True)
        embed.add_field(name="Players", value=f"👥 {status['players']}", inline=True)
        embed.add_field(name="Online Players", value=players_list, inline=False)
        embed.add_field(name="Game", value=f"🎲 {status['game']}", inline=False)
    else:
        # Offline embed with fun message
        embed = discord.Embed(
            title="🎮 Server Status",
            description=f"Server is **offline!** :red_circle:",
            color=discord.Color.red()
        )
        embed.add_field(name="NOT IDEAL", value="Spam @skantesmoka to fix me!", inline=True)

    # Find pinned status message (async iterator)
    status_message = None
    async for msg in channel.pins():
        if msg.author == client.user:
            status_message = msg
            break

    if status_message:
        # Only edit if embed is different
        if not status_message.embeds or status_message.embeds[0].to_dict() != embed.to_dict():
            await status_message.edit(embed=embed)
            print("Status message updated.")
        else:
            print("Status message already up-to-date, no edit needed.")
    else:
        # Send new pinned message
        status_message = await channel.send(embed=embed)
        await status_message.pin()
        print("Status message sent and pinned.")

    await client.close()

client.run(TOKEN)

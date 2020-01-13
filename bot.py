# bot.py
import os

import discord
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError, Timeout
import json
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
NITRAPI_BASE_URL = os.getenv('NITRAPI_BASE_URL')
NITRAPI_GAMESERVER_DETAILS = os.getenv('NITRAPI_GAMESERVER_DETAILS')

with open('nitrapi_account_config.json') as json_file:
    NITRAPI_ACCOUNT_CONFIG = json.load(json_file)

# Handler for AWS Lambda to run the application
def handler(event, context):
    client = discord.Client()

    @client.event
    async def on_ready():
        guild = discord.utils.get(client.guilds, name=GUILD)
        channel = discord.utils.get(guild.channels, name=CHANNEL)

        status_message = None

        async for message in channel.history(limit=10):
            if message.author == client.user:
                status_message = message

        nitrapi_config = json.loads(NITRAPI_ACCOUNT_CONFIG)

        embed = discord.Embed(title="Valkyrie Server Status", colour=discord.Colour(0xf8e71c), url="https://github.com/sternd/nitrado-ark-status-bot", description="A visualization of the availability status for Valkyrie's Ark Nitrado servers. The status of all servers will be updated every minute.")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/626094990984216586/ceb7d3a814435bc9601276d07f44b9f3.png?size=128")
        embed.set_footer(text="Updated",
                         icon_url="https://cdn.discordapp.com/icons/626094990984216586/ceb7d3a814435bc9601276d07f44b9f3.png?size=128")

        for account in nitrapi_config["nitrado_accounts"]:
            auth_token = account["auth_token"]

            availability_status = 'available'

            for gameserver in account["gameservers"]:
                if gameserver["enabled"] != True:
                    continue

                gameserver_details = getGameserverDetails(auth_token, gameserver["gameserver_id"])

                status = parseGameserverStatus(gameserver_details)

                if availability_status == 'down' or availability_status == 'restarting':
                    availability_status = availability_status
                elif status != 'started' and status != 'restarting':
                    availability_status = 'down'
                elif status == 'restarting':
                    availability_status = 'restarting'

                embed = addRichEmbedField(embed, gameserver["gameserver_name"], status, gameserver_details)

            if availability_status == 'available':
                colour = discord.Colour(0x7ed321)
            elif availability_status == 'restarting':
                colour = discord.Colour(0xf5a623)
            elif availability_status == 'down':
                colour = discord.Color(0xD0021B)
            else:
                colour = discord.Color(0xD0021B)

        embed.__setattr__('timestamp', datetime.utcnow())
        embed.__setattr__('colour', colour)

        if status_message == None:
            await channel.send(embed=embed)
        else:
            await status_message.edit(embed=embed)

        await client.close()

    # Make GET request to NitrAPI for gameserver details
    # Return: Dict | None
    # See for more info: https://doc.nitrado.net/#api-Gameserver-Details
    def getGameserverDetails(token, id):
        # print(f"Getting gameserver details for {id}")
        url = NITRAPI_BASE_URL + NITRAPI_GAMESERVER_DETAILS.replace(':id', id, 1)
        auth_token = f'Bearer {token}'
        try:
            response = requests.get(url, timeout=3, headers={"Authorization": auth_token})
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred for {id}: {http_err}')
        except Timeout as timeout:
            print(f'HTTP timeout occurred for {id}: {timeout}')
        except Exception as err:
            print(f'Other error occurred for {id}: {err}')
        else:
            return response.json()

        return None

    # Extract the gameserver status from the gameserver details API response
    # Return: String | None
    def parseGameserverStatus(gameserver_details):
        try:
            status = gameserver_details['data']['gameserver']['status']
        except Exception as err:
            print(f'Error occurred: {err}')
        else:
            return status

        return None

    # Format the gameserver status with the correct colored circle
    # Return: String
    def formatGameserverStatus(gameserver_status):
        if gameserver_status == "started":
            green_circle = discord.utils.get(client.emojis, name="green_circle")
            return '🟢'
        elif gameserver_status == 'stopped' or gameserver_status == 'stopping' or gameserver_status == 'suspended':
            return '🔴'
        elif gameserver_status == 'restarting':
            return '🟠'
        else:
            return '🔴'

    # Extract the gameserver player count information from the gameserver details API response
    # Return: Dict | None
    def parseGameserverPlayers(gameserver_details):
        try:
            players = {"current_players": gameserver_details['data']['gameserver']['query']['player_current'], "max_players": gameserver_details['data']['gameserver']['query']['player_max']}
        except Exception as err:
            # print(f'Error occurred: {err}')
            return None
        else:
            return players

        return None

    # Formats the message for an individual gameserver and adds it to an existing embed
    # Return: Discord.Embed
    def addRichEmbedField(embed, server_name, status, server_details):
        players = parseGameserverPlayers(server_details)
        formatted_status = formatGameserverStatus(status)

        formatted_server_message = f'*Status:*  {formatted_status}\n'

        if players != None:
            formatted_server_message += f'*Players:*  {players["current_players"]}/{players["max_players"]}'

        embed.add_field(name='**' + server_name + '**', value=formatted_server_message, inline=True)

        return embed

    # Starts the Discord Client connection
    client.run(TOKEN)

    return {
    'message': "Success"
    }

# UNCOMMENT TO RUN LOCALLY
#handler(None, None)
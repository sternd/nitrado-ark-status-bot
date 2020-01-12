# bot.py
import os

import discord
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError, Timeout
import json

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

        output_array = []

        for account in nitrapi_config["nitrado_accounts"]:
            auth_token = account["auth_token"]

            for gameserver in account["gameservers"]:
                if (gameserver["enabled"] != True):
                    continue

                gameserver_details = getGameserverDetails(auth_token, gameserver["gameserver_id"])
                output_array.append(formatGameserverMessage(gameserver["gameserver_name"], gameserver_details))

        formatted_status_message = '\n__**Valkyrie Server Status**__\n\n'

        for gameserver_output in output_array:
            formatted_status_message += gameserver_output + '\n'

        if status_message == None:
            await channel.send(formatted_status_message)
        else:
            await status_message.edit(content=formatted_status_message)

        await client.close()

    # Make GET request to NitrAPI for gameserver details
    # Return: Dict | None
    # See for more info: https://doc.nitrado.net/#api-Gameserver-Details
    def getGameserverDetails(token, id):
        print(f"Getting gameserver details for {id}")
        url = NITRAPI_BASE_URL + NITRAPI_GAMESERVER_DETAILS.replace(':id', id, 1)
        auth_token = f'Bearer {token}'
        try:
            response = requests.get(url, timeout=3, headers={"Authorization": auth_token})
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Timeout as timeout:
            print(f'HTTP timeout occurred: {timeout}')
        except Exception as err:
            print(f'Other error occurred: {err}')
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
            return '🟢 Available'
        elif gameserver_status == 'stopped' or gameserver_status == 'stopping' or gameserver_status == 'suspended':
            return '🔴 Down'
        elif gameserver_status == 'restarting':
            return '🟠 Restarting'
        else:
            return '🔴 Unknown'

    # Extract the gameserver player count information from the gameserver details API response
    # Return: Dict | None
    def parseGameserverPlayers(gameserver_details):
        try:
            players = {"current_players": gameserver_details['data']['gameserver']['query']['player_current'], "max_players": gameserver_details['data']['gameserver']['query']['player_max']}
        except Exception as err:
            print(f'Error occurred: {err}')
        else:
            return players

        return None

    # Formats the message for an individual gameserver for output to Discord
    # Return: String
    def formatGameserverMessage(server_name, server_details):
        status = parseGameserverStatus(server_details)
        players = parseGameserverPlayers(server_details)
        formatted_status = formatGameserverStatus(status)

        formatted_server_message = f'**{server_name}**\n*Status:*  {formatted_status}\n'

        if players != None:
            formatted_server_message += f'*Players:*  {players["current_players"]}/{players["max_players"]}\n'

        return formatted_server_message

    # Starts the Discord Client connection
    client.run(TOKEN)

    return {
    'message': "Success"
    }

# UNCOMMENT TO RUN LOCALLY
handler(None, None)
# bot.py
import os

import discord
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError, Timeout
import json
from datetime import datetime

load_dotenv()
NITRAPI_BASE_URL = os.getenv('NITRAPI_BASE_URL')
NITRAPI_GAMESERVER_DETAILS = os.getenv('NITRAPI_GAMESERVER_DETAILS')

with open('nitrapi_account_config.json') as json_file:
    NITRAPI_ACCOUNT_CONFIG = json.load(json_file)

# Helper class to send Discord API requests
class DiscordHelper:
    TOKEN = os.getenv('DISCORD_TOKEN')
    BOT_CLIENT_ID = os.getenv('BOT_CLIENT_ID')
    CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
    DISCORD_BASE_URL = os.getenv('DISCORD_BASE_URL')
    DISCORD_MESSAGE_HISTORY = os.getenv('DISCORD_MESSAGE_HISTORY')
    DISCORD_CREATE_MESSAGE = os.getenv('DISCORD_CREATE_MESSAGE')
    DISCORD_EDIT_MESSAGE = os.getenv('DISCORD_EDIT_MESSAGE')

    def __init__(self):
        if self.TOKEN is None:
            raise Exception('Missing Discord Token')
        elif self.BOT_CLIENT_ID is None:
            raise Exception('Missing Bot Client ID')
        elif self.CHANNEL_ID is None:
            raise Exception('Missing Discord Channel ID')
        elif self.DISCORD_BASE_URL is None:
            raise Exception('Missing Discord Base URL')
        elif self.DISCORD_MESSAGE_HISTORY is None:
            raise Exception('Missing Discord Message History Path')
        elif self.DISCORD_CREATE_MESSAGE is None:
            raise Exception('Missing Discord Create Message Path')
        elif self.DISCORD_EDIT_MESSAGE is None:
            raise Exception('Missing Discord Edit Message Path')

    # Send a Discord API request
    def sendDiscordRequest(self, action, url, *params):
        # Do request here

        auth_token = f'Bot {self.TOKEN}'

        json_body = None

        if params is not None and params:
            json_body = params[0]

        try:
            if action == 'GET':
                response = requests.get(url, timeout=10, headers={"Authorization": auth_token})
            elif action == 'POST':
                response = requests.post(url, timeout=6, headers={"Authorization": auth_token}, json=json_body)
            elif action == 'PATCH':
                response = requests.patch(url, timeout=6, headers={"Authorization": auth_token}, json=json_body)
            else:
                raise Exception(f'Attempting to send request with unknown action: {action}')

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

    # Get message ID of most recent message sent by bot
    def getLatestMessageID(self):
        # Make request for message history
        # Parse message ID
        url = self.DISCORD_BASE_URL + self.DISCORD_MESSAGE_HISTORY.replace(':channel_id', self.CHANNEL_ID, 1)

        response = self.sendDiscordRequest('GET', url)

        if response is None:
            return None

        for message in response:
            if message["author"]["id"] != self.BOT_CLIENT_ID:
                continue

            return message["id"]

        return None

    # Edit an existing Rich Embed message
    def editMessage(self, message_id, embed):
        # Make request to edit message
        url = self.DISCORD_BASE_URL + self.DISCORD_EDIT_MESSAGE.replace(':channel_id', self.CHANNEL_ID, 1).replace(
            ':message_id', message_id, 1)

        response = self.sendDiscordRequest('PATCH', url, {"embed": embed})

        if response is None:
            return None

        return response

    # Create a new Rich Embed message
    def createMessage(self, embed):
        # Make request to edit message
        url = self.DISCORD_BASE_URL + self.DISCORD_CREATE_MESSAGE.replace(':channel_id', self.CHANNEL_ID, 1)

        response = self.sendDiscordRequest('POST', url, {"embed": embed})

        if response is None:
            return None

        return response


# Handler for AWS Lambda to run the application
def handler(event, context):
    discord_helper = DiscordHelper()

    nitrapi_config = json.loads(NITRAPI_ACCOUNT_CONFIG)

    embed = discord.Embed(title="Valkyrie Server Status", colour=discord.Colour(0xf8e71c),
                          url="https://github.com/sternd/nitrado-ark-status-bot",
                          description="A visualization of the availability status for Valkyrie's Ark Nitrado servers. The status of all servers will be updated every minute.")

    server_icon = os.getenv('SERVER_ICON')

    embed.set_thumbnail(
        url=server_icon)
    embed.set_footer(text="Updated",
                     icon_url=server_icon)

    availability_status = 'available'

    for account in nitrapi_config["nitrado_accounts"]:
        auth_token = account["auth_token"]

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

    dict_embed = embed.to_dict()

    message_id = discord_helper.getLatestMessageID()

    if message_id is None:
        discord_helper.createMessage(dict_embed)
    else:
        discord_helper.editMessage(message_id, dict_embed)

    return {
        'message': "Success"
    }


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
        players = {"current_players": gameserver_details['data']['gameserver']['query']['player_current'],
                   "max_players": gameserver_details['data']['gameserver']['query']['player_max']}
    except Exception as err:
        # print(f'Error occurred: {err}')
        return None
    else:
        return players


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

# UNCOMMENT TO RUN LOCALLY
#handler(None, None)

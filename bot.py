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
NITRAPI_AUTH_TOKEN = os.getenv('NITRAPI_AUTH_TOKEN')
NITRAPI_BASE_URL = os.getenv('NITRAPI_BASE_URL')
NITRAPI_GAMESERVER_DETAILS = os.getenv('NITRAPI_GAMESERVER_DETAILS')
NITRAPI_GAMESERVER_RAGNAROK_ID = os.getenv('NITRAPI_GAMESERVER_RAGNAROK_ID')
NITRAPI_GAMESERVER_VALGUERO_ID = os.getenv('NITRAPI_GAMESERVER_VALGUERO_ID')
NITRAPI_GAMESERVER_EXTINCTION_ID = os.getenv('NITRAPI_GAMESERVER_EXTINCTION_ID')
NITRAPI_GAMESERVER_ABERRATION_ID = os.getenv('NITRAPI_GAMESERVER_ABERRATION_ID')
NITRAPI_GAMESERVER_ISLAND_ID = os.getenv('NITRAPI_GAMESERVER_ISLAND_ID')
NITRAPI_GAME_SERVER_CENTER_ID = os.getenv('NITRAPI_GAME_SERVER_CENTER_ID')

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

        gameserver_ragnarok_details = getGameserverDetails(NITRAPI_GAMESERVER_RAGNAROK_ID)
        gameserver_valguero_details = getGameserverDetails(NITRAPI_GAMESERVER_VALGUERO_ID)
        gameserver_extinction_details = getGameserverDetails(NITRAPI_GAMESERVER_EXTINCTION_ID)
        gameserver_aberration_details = getGameserverDetails(NITRAPI_GAMESERVER_ABERRATION_ID)
        gameserver_island_details = getGameserverDetails(NITRAPI_GAMESERVER_ISLAND_ID)
        gameserver_center_details = getGameserverDetails(NITRAPI_GAME_SERVER_CENTER_ID)

        # EXAMPLE DATA FOR TESTING
        gameserver_ragnarok_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"started\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":15,\"player_max\":20,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")
        gameserver_valguero_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"stopped\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":0,\"player_max\":20,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")
        gameserver_extinction_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"stopping\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":0,\"player_max\":10,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")
        gameserver_aberration_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"restarting\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":0,\"player_max\":10,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")
        gameserver_island_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"started\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":0,\"player_max\":10,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")
        gameserver_center_details = json.loads("{\"status\":\"success\",\"data\":{\"gameserver\":{\"must_be_started\":true,\"status\":\"started\",\"websocket_token\":\"b05ac3d5d71a8858fca3011a8c179f1d9ec5ab41\",\"hostsystems\":{\"linux\":{\"hostname\":\"ms001.nitrado.net\",\"status\":\"online\"}},\"username\":\"ni1_1\",\"managed_root\":false,\"user_id\":1,\"service_id\":1,\"location_id\":2,\"minecraft_mode\":false,\"ip\":\"127.0.0.1\",\"ipv6\":\"2a03:4d41::7f00:1\",\"port\":25565,\"query_port\":25565,\"rcon_port\":25565,\"label\":\"ni\",\"type\":\"Gameserver\",\"memory\":\"Standard\",\"memory_mb\":1024,\"game\":\"mc\",\"game_human\":\"Minecraft Vanilla\",\"game_specific\":{\"path\":\"\/games\/ni1_1\/ftproot\/mcr\/\",\"update_status\":\"up_to_date\",\"last_update\":null,\"path_available\":true,\"features\":{\"has_backups\":true,\"has_application_server\":false,\"has_container_websocket\":false,\"has_rcon\":false,\"has_file_browser\":true,\"has_ftp\":true,\"has_expert_mode\":false,\"has_plugin_system\":false,\"has_restart_message_support\":false,\"has_database\":true},\"log_files\":[],\"config_files\":[]},\"modpacks\":{\"mcrdns\":{\"name\":\"Pixelmon Craft\",\"modpack_version\":\"4.0.6\",\"game_version\":\"1.8.4\"}},\"slots\":4,\"location\":\"DE\",\"credentials\":{\"ftp\":{\"hostname\":\"dev001.nitrado.net\",\"port\":21,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\"},\"mysql\":{\"hostname\":\"dev001.nitrado.net\",\"port\":3306,\"username\":\"ni1_1\",\"password\":\"4x8x15x16x23x42\",\"database\":\"ni1_1_DB\"}},\"settings\":{\"base\":{\"dailyrestart\":\"false\"},\"config\":{\"pvp\":\"true\",\"friendlyfire\":\"false\"}},\"quota\":{\"block_usage\":437656,\"block_softlimit\":10485760,\"block_hardlimit\":15728640,\"file_usage\":456,\"file_softlimit\":1200000,\"file_hardlimit\":2000000},\"query\":{\"server_name\":\"Minecraft Server\",\"connect_ip\":\"127.0.0.1:25565\",\"map\":\"random\",\"version\":\"1.8\",\"player_current\":6,\"player_max\":10,\"players\":[{\"id\":1,\"name\":\"Tyrola\",\"bot\":false,\"score\":0,\"frags\":0,\"deaths\":0,\"time\":31,\"ping\":8}]}}}}")

        ragnarok_message = formatGameserverMessage('Ragnarok', gameserver_ragnarok_details)
        valguero_message = formatGameserverMessage('Valguero', gameserver_valguero_details)
        extinction_message = formatGameserverMessage('Extinction', gameserver_extinction_details)
        aberration_message = formatGameserverMessage('Aberration', gameserver_aberration_details)
        island_message = formatGameserverMessage('Island', gameserver_island_details)
        center_message = formatGameserverMessage('Center', gameserver_center_details)

        formatted_status_message = '\n__**Valkyrie Server Status**__\n\n' + ragnarok_message + '\n' + valguero_message + '\n' + extinction_message + '\n' + aberration_message + '\n' + island_message + '\n' + center_message + '\n'

        if status_message == None:
            status_message = await channel.send(formatted_status_message)
        else:
            status_message = await status_message.edit(content=formatted_status_message)

        await client.close()

    # Make GET request to NitrAPI for gameserver details
    # Return: Dict | None
    # See for more info: https://doc.nitrado.net/#api-Gameserver-Details
    def getGameserverDetails(id):
        url = NITRAPI_BASE_URL + NITRAPI_GAMESERVER_DETAILS.replace(':id', id, 1)
        auth_token = f'Bearer {NITRAPI_AUTH_TOKEN}'
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
            print(response.json())
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
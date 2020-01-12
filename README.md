# Discord Bot for Nitrado Server Status

A simple Discord bot that retrieves the server status for Nitrado gameservers and updates a Discord channel with the status.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt

```bash
pip3 install --target ./package -r requirements.txt
PYTHONPATH="PATH_TO_PACKAGE_FOLDER:$PYTHONPATH"
export PYTHONPATH
```
Replace line #165 of package/discord/client.py:

```python
self.loop = asyncio.get_event_loop() if loop is None else loop
```
With:
```python
self.loop = asyncio.new_event_loop()
```

Create copy of "nitrapi_account_config_template.json" as "nitrapi_account_config.json".
Then add the auth_tokens for each of the Nitrado accounts into the config.

Create a copy of ".env_template" as ".env".
Add the values for: DISCORD_TOKEN, DISCORD_GUILD, and DISCORD_CHANNEL

## Usage
Make sure to uncomment the last line in bot.py to run locally.

```bash
python3 bot.py
```

## Lambda Deployment

```bash
cd project_root
cd ./package
zip -r9 ${OLDPWD}/nitrado-ark-status-bot.zip .
cd ..
zip -g nitrado-ark-status-bot.zip bot.py
zip -g nitrado-ark-status-bot.zip nitrapi_account_config.json
aws lambda update-function-code --function-name nitrado-ark-status-bot --zip-file fileb://nitrado-ark-status-bot.zip
```

## Known Issues
1. Player counts are not always returned by NitrAPI

## Contributing
Pull requests are welcome to the "develop" branch. For major changes, please open an issue first to discuss what you would like to change.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
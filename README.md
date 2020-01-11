# Discord Bot for Nitrado Server Status

A simple Discord bot that retrieves the server status for Nitrado gameservers and updates a Discord channel with the status.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt

```bash
pip3 install --target ./package -r requirements.txt
PYTHONPATH="PATH_TO_PACKAGE_FOLDER:$PYTHONPATH"
export PYTHONPATH
```

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
aws lambda update-function-code --function-name nitrado-ark-status-bot --zip-file fileb://nitrado-ark-status-bot.zip
```

## Contributing
Pull requests are welcome to the "develop" branch. For major changes, please open an issue first to discuss what you would like to change.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
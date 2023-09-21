# telegram_tm_client

TM client that send into telegram you Balance, Items on sale and Sold items that waiting for trade. 

### Installation

Setup requirements into your virtual invironment with:

```
pip install -r requirements.txt
```


### Settings
Setup your setting.py file to allow application to send messages to your chat in telegram.

tg_api - telegram api key can be obtained on BotFather. It's official telegram bot to create your own bot and obtain your bot api key;
tm_api  - you can get your tm api on https://market-old.csgo.com/docs-v2;
request_interval - the interval (in seconds) at which your data will be updated

| KEY | VALUE |
| ------ | ------ |
| tg_api | telegram api key can be obtained on BotFather. It's official telegram bot to create your own bot and obtain your bot api key |
| tm_api | you can get your tm api on https://market-old.csgo.com/docs-v2 |
| request_interval | the interval (in seconds) at which your data will be updated |

## Running

Run client with:

```
python main.py
```

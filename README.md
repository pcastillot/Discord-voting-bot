# Discord-voting-bot
Bot for discord with voting system to kick or mute from voice channel

To install libraries:
pip install -r requirements.txt

Default Available commands:

    -mute @user   --> Mutes user in voice channel he is in
  
    -unmute @user --> Unmutes user in voice channel he is in
  
    -kick @user   --> Kicks user in voice channel he is in

You can change this commands and the prefix by modificating the constants at the beginning of the code.

Also you can change how long the voting is enabled as the minimum percentage needed to valid a request

The one sending the request to the bot, and the mentioned user, must be both in the same voice channel to work, so an unintended use from user not connected won't be possible

Script must be running to work, if not, the bot won't work

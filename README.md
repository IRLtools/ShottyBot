# ShottyBot
<p align="center"> 
  A bot for Twitch + OBS + Discord that easily sends screenshots to discord
</p>

ShottyBot by IRLtools is a super user-friendly approach to increasing your viewer engagement and sharing memories of moments on stream.  With a simple command and less than 3 minutes to set up, your viewers will be sending screenshots, uncluttered with overlays, to your discord.  Please join our discord for updates and feature requests! 


## Installation
Download the latest release from [releases page](https://github.com/IRLTools/ShottyBot/releases/tag/v0.1.0)

## Usage
To use ShottyBot, you must create a twitch app first (the bot) and have a discord webhook url  
  Follow these steps:
1. Head to [Twitch Developers page](https://dev.twitch.tv/console/apps) and register your application.
  - You can set "Category" to chat bot, and oauth redirect uri to "http://localhost"
2. You need a webhook url for the channel that will host the screenshots 
  - Go to integration settings (located in your server settings) and create a new integration
  - Copy the webhook url for the created integration

After that, just open main file (e.g. `main.exe`) and fill in the required info and start the bot!

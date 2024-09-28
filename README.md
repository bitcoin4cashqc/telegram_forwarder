# Telegram Bot for Forwarding Messages

This bot forwards messages from specified channels, groups, or supergroups to other target groups or channels. It also provides the functionality to get the IDs for groups, channels, and topics within supergroups.

## Features
- Automatically forwards messages from allowed users in specified groups or channels.
- Retrieves and displays the group, channel, or topic ID when requested.
- Supports forwarding messages to specific topics within supergroups.

## Requirements
- Python 3.7 or higher
- Install dependencies: pip install -r requirements.txt

## How to Set Up

### 1. Create a Bot using BotFather
1. Open Telegram and search for the @BotFather bot.
2. Send the /newbot command and follow the instructions to create a new bot.
3. BotFather will provide you with an API token for your bot. Save this token, as it will be needed in the code.

### 2. Configure the Bot Token
In the provided Python script, replace the placeholder token with the token received from BotFather.

Edit the line in the script:
`TOKEN = "YOUR_BOT_TOKEN"`

### 3. Get the Group or Channel ID
To get the group or channel ID:
1. Add the bot to the group or channel where you want to forward messages.
2. In the group or channel, send the command: /get_group_id
3. The bot will respond with the group's or channel's ID, which you can then use to update the forwarding logic.

**For channels, you need to forward a message from the channel to the bot directly to retrieve the channel ID.** Once forwarded, the bot will respond with the channel's ID.

### 4. Get the Topic ID (for Supergroups with Topics)
To get the ID of a particular topic within a supergroup:
1. Go to the desired topic within the supergroup.
2. In the topic, send the command: /get_group_id
3. The bot will respond with both the group ID and the Topic ID (message_thread_id). The topic ID will allow the bot to forward messages specifically to this topic.

### 5. Edit the TARGET_GROUPS in the Code
Once you have the group, channel, and topic IDs, edit the TARGET_GROUPS list in the script to include them.

For example:
`TARGET_GROUPS = [ {"chat_id": -1002375678860, "topic_id": None}, {"chat_id": -1002370612441, "topic_id": 40}, {"chat_id": -1002293550563, "topic_id": None} ]`

- chat_id: This is the ID of the group or channel where messages should be forwarded.
- topic_id: This is the ID of the topic within a supergroup. If forwarding to a group or channel without topics, set this value to None.

### 6. Allowed Users
You can specify which users are allowed to trigger message forwarding by editing the ALLOWED_USERS list in the script.

`ALLOWED_USERS = ["SoliditySam"]`

Only users in this list will have their messages forwarded from the groups/channels.

### 7. Run the Bot
Start the bot by running the following command: python main.py

The bot will now listen for messages from the specified groups, channels, or topics and forward them accordingly.

## Commands

### /get_group_id
- This command returns the group or channel ID where the command is run.
- If executed in a supergroup with topics, it will also return the topic ID.

## Example
If you want to forward messages from a private channel to a group and also from one topic in a supergroup to another group, you would first use the /get_group_id command in both the channel and the topic to retrieve their respective IDs. Then, edit the TARGET_GROUPS list as shown above.

## Installation

1. Clone or download the repository.
2. Install the dependencies: pip install -r requirements.txt
3. Configure the bot token and IDs as explained above.
4. Run the bot: python main.py


import requests
import json
import time

def send_discord_message(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(message), headers=headers)
    if response.status_code == 204:
        print("Message sent successfully to Discord")
    else:
        print("Failed to send message to Discord")

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

config = load_config()
webhook_url = config.get('webhook_url')
user_ids = config.get('user_ids', [])

def send_message_for_user(user_id):
    presence_url = f'https://presence.roblox.com/v1/presence/users'
    data = {'userIds': [user_id]}
    response = requests.post(presence_url, json=data)
    if response.status_code == 200:
        response_json = response.json()
        user_presence = response_json['userPresences'][0]
        if user_presence['userPresenceType'] == 2:
            place_id = user_presence['placeId']
            game_id = user_presence['gameId']
            message = {
                "content": None,
                "embeds": [
                    {
                        "title": f"Roblox Profile: https://www.roblox.com/users/{user_id}/profile",
                        "color": None,
                        "fields": [
                            {
                                "name": "**Place ID**",
                                "value": "```{}```".format(place_id),
                                "inline": True
                            },
                            {
                                "name": "**Game ID**",
                                "value": "```{}```".format(game_id),
                                "inline": True
                            },
                            {
                                "name": "**User ID**",
                                "value": "```{}```".format(user_id),
                                "inline": False
                            }
                        ],
                        "author": {
                            "name": "User in-game"
                        }
                    }
                ],
                "attachments": []
            }
            send_discord_message(webhook_url, message)
        else:
            print(f"User {user_id} is not in-game")
    else:
        print(f"Failed to fetch presence information for user {user_id}")

while True:
    for user_id in user_ids:
        send_message_for_user(user_id)
    time.sleep(20)

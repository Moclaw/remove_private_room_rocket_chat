from rocketchat.api import RocketChatAPI
import requests
import argparse
import json

global rocket, url, headers


def get_room(data):
    for rooms in data:
        roomid = rooms['id']
        roomname = rooms['name']
        data.append({"_id": roomid, "name": roomname})
    return data


def change_to_public(list_room):
    for item in list_room:
        payload = json.dumps({
            "rid": item['_id'],
            "roomName": item['name'],
            "roomType": "c"
        })
        response = requests.request(
            "POST", url, headers=headers, data=payload)
        print(response)


def delete():
    for item in list_room:
        print(rocket.delete_public_room(item['id']))


list_room = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete private rooms",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--domain", action="store",
                        help="domain app ex: chat.domain.com")
    parser.add_argument("-u", "--user", action="store",
                        help="user account")
    parser.add_argument("-p", "--password", action="store",
                        help="password")
    config = vars(parser.parse_args())

    domain = config['domain']
    user = config['user']
    password = config['password']

    loginrequets = requests.post(
        "https://"+domain+"/api/v1/login", data={"user": user, "password": password})
    token = loginrequets.json().get("data").get("authToken")
    userid = loginrequets.json().get("data").get("userId")
    rocket = RocketChatAPI(
        settings={'user_id': userid, 'token': token, 'domain': "https://"+domain})
    url = "https://"+domain+"/api/v1/rooms.saveRoomSettings"
    headers = {
        'X-User-Id': userid,
        'X-Auth-Token': token,
        'Content-Type': 'application/json'
    }
    data = rocket.get_private_rooms()
    if (len(list_room) > 0):
        change_to_public(list_room)
    if (len(list_room) == 0):
        print("No private room")
        list_room = rocket.get_public_rooms()
    delete()

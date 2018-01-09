import json
from slackclient import SlackClient
import urllib.request
import os

TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(TOKEN)
print("Token :"+TOKEN)

def get_name_id_mapping():
    group_map = {}
    groups_info = slack_client.api_call("groups.list")
    if groups_info:
        for group in groups_info['groups']:
            group_map[group['name']] = group['id']
    return group_map


def get_user_id_mapping():
    user_map = {}
    users_info = slack_client.api_call("users.list")
    #user_list_request = "https://slack.com/api/users.list?token="+TOKEN+"&pretty=1"
    # users_info = json.loads(urllib.request.urlopen(user_list_request).read())

    if users_info:
        for user in users_info['members']:
            profile = user['profile']
            if 'email' in profile:
                user_map[profile['email']] = user['id']
    return user_map

def get_general_channel_id():
    channel_list = slack_client.api_call("channels.list")
    for channel in channel_list:
        if channel['name']=="general":
            return channel['id']
    return None


def add_users_to_grps():
    # Read students id's into a list
    group_map = get_name_id_mapping()
    user_map = get_user_id_mapping()
    list_file = input("Input path of student list file: ")
    users_list = open(list_file, 'r')
    users = users_list.read().splitlines()
    for user in users:
        user_info = user.split(';')
        print("Adding user: "+user_info[1]+"to team: "+user_info[0])
        if user_info[1] in user_map:
            add_user_to_grp(user_map[user_info[1]], group_map[user_info[0]])
        else:
            print("Error occured:: User "+user_info[1]+" could not be added. Not a member of workspace")
        print("\n")


def add_user_to_grp(user_id, group_id):
    api_results = slack_client.api_call("groups.invite", channel=group_id, user=user_id)
    if[api_results['ok'] == 'true']:
        print("User successfully added")
    else:
        print(str(api_results))
    return None


add_users_to_grps()

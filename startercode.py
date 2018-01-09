import os
from slackclient import SlackClient


SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)

slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

if __name__ == '__main__':

    print "Current status of channels"
    channels = list_channels()
    if channels:
        print("Channels: ")
        for c in channels:
            print(c['name'] + " (" + c['id'] + ")")
    else:
        print("Unable to authenticate.")
    s = raw_input("How many sections? ")

    sections=int(s)

    s = raw_input("How many students per section? ")

    students=int(s)

    s = raw_input("How many students per team? ")

    teamSize=int(s)

    numberOfTeams=students/teamSize
    print "\nThere are " + repr(sections) + " sections, " + repr(students) + " students per section, and " + repr(numberOfTeams) + " students per team.\n"
    print "slack token: " +  SLACK_TOKEN

    for section in range(0,sections):
        for team in range(0,numberOfTeams):

            teamNumber=(section * 10 + team)
            channelName = "team-" + repr(teamNumber)
            print 'setting up section %d team %d on channel %s' % (section, teamNumber, channelName)

            api_results= slack_client.api_call("groups.create", name=channelName)
            if api_results['ok']:
                print 'Success!'
                #send_message(api_results['group', 'id'], "Created channel")
            else:
                print api_results

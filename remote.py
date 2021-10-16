import sys
import getopt
import requests
import json


def main(argv):
    poweropt = ''
    volumeopt = 0
    volumeopt2 = 0
    volumeopt3 = 0
    channelopt = ''
    appopt = ''
    ipopt = ''
    keyopt = ''

    try:
        options, args = getopt.getopt(argv, "hi:k:p:v:c:a:U:D:", ["help", "ip=", "key=", "power=", "volume=", "volumeup=", "volumedown=", "channel=", "app="])
    except getopt.GetoptError:
        print('USAGE: remote.py -i [ip address] -k [pre-shared Key] [option] [option arg]')
        print('-h or --help for options.')
        sys.exit(2)
    for option, arg in options:
        if option == '-h':
            print('USAGE: remote.py -i [ip address] -k [pre-shared Key] [option] [option arg]')
            print('Options:')
            print('-p [on/off] | --power [on/off]')
            print('-v [1-100] | --volume [1-100]')
            print('-U [1-100] | --volumeup [1-100]')
            print('-D [1-100] | --volumedown [1-100]')
            print('-c [hdmi1-hdmi4] | --channel [hdmi1-hdmi4]')
            print('-a [youtube/netflix/twitch/spotify] | --app [youtube/netflix/twitch/spotify]')
            sys.exit()
        elif option in ("-i", "--ip"):
            ipopt = arg
            if ipopt == '':
                print('no ip entered')
        elif option in ("-k", "--key"):
            keyopt = arg
            if keyopt == '':
                print('no key entered')

        elif option in ("-p", "--power"):
            poweropt = arg
            if poweropt == 'on':
                pstatus = True
                pcontrol(ipopt, keyopt, pstatus)
            elif poweropt == 'off':
                pstatus = False
                pcontrol(ipopt, keyopt, pstatus)
            else:
                print('Invalid power option')
                sys.exit()
        elif option in ("-v", "--volume"):
            volumeopt = int(arg)
            if volumeopt in range(0, 101):
                vcontrol(ipopt, keyopt, volumeopt)
            else:
                print('Invalid volume range')
                sys.exit(1)
        elif option in ("-U", "--volumeup"):
            volumeopt2 = int(arg)
            if volumeopt in range(0, 101):
                vcontrol2(ipopt, keyopt, volumeopt2)
            else:
                print('Invalid volume range')
                sys.exit(1)
        elif option in ("-D", "--volumedown"):
            volumeopt3 = int(arg)
            if volumeopt in range(0, 101):
                vcontrol3(ipopt, keyopt, volumeopt3)
            else:
                print('Invalid volume range')
                sys.exit(1)
        elif option in ("-c", "--channel"):
            channelopt = arg
            if channelopt == 'hdmi1':
                channel = 'extInput:hdmi?port=1'
                ccontrol(ipopt, keyopt, channel)
            elif channelopt == 'hdmi2':
                channel = 'extInput:hdmi?port=2'
                ccontrol(ipopt, keyopt, channel)
            elif channelopt == 'hdmi3':
                channel = 'extInput:hdmi?port=3'
                ccontrol(ipopt, keyopt, channel)
            elif channelopt == 'hdmi4':
                channel = 'extInput:hdmi?port=4'
                ccontrol(ipopt, keyopt, channel)
            else:
                print('Invalid channel selection')
                sys.exit(1)
        elif option in ("-a", "--app"):
            appopt = arg
            if appopt == 'spotify':
                app = 'com.sony.dtv.com.spotify.tv.android.com.spotify.tv.android.SpotifyTVActivity'
                acontrol(ipopt, keyopt, app)
            elif appopt == 'youtube':
                app = 'com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity'
                acontrol(ipopt, keyopt, app)
            elif appopt == 'twitch':
                app = 'com.sony.dtv.tv.twitch.android.app.tv.twitch.android.apps.TwitchActivity'
                acontrol(ipopt, keyopt, app)
            elif appopt == 'netflix':
                app = 'com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity'
                acontrol(ipopt, keyopt, app)
            else:
                print('Invalid app selection')
                sys.exit(1)

    print('Power =', poweropt)
    print('Volume =', volumeopt)
    print('Channel =', channelopt)
    print('App =', appopt)


def pcontrol(ipopt, keyopt, pstatus):

    url = f"http://{ipopt}/sony/system"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setPowerStatus",
        "id": 55,
        "params": [{"status": pstatus}],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)

# absolute volume
def vcontrol(ipopt, keyopt, volumeopt):
    url = f"http://{ipopt}/sony/audio"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setAudioVolume",
        "id": 601,
        "params": [{
            "volume": f"{volumeopt}",
            "target": "speaker"
        }],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)

# volume up
def vcontrol2(ipopt, keyopt, volumeopt2):
    url = f"http://{ipopt}/sony/audio"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setAudioVolume",
        "id": 601,
        "params": [{
            "volume": f"+{volumeopt2}",
            "target": "speaker"
        }],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)

# volume down
def vcontrol3(ipopt, keyopt, volumeopt3):
    url = f"http://{ipopt}/sony/audio"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setAudioVolume",
        "id": 601,
        "params": [{
            "volume": f"-{volumeopt3}",
            "target": "speaker"
        }],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)

def ccontrol(ipopt, keyopt, channel):
    url = f"http://{ipopt}/sony/avContent"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setPlayContent",
        "id": 101,
        "params": [{"uri": f"{channel}"}],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)


def acontrol(ipopt, keyopt, app):
    url = f"http://{ipopt}/sony/appControl"
    headers = {
        "X-Auth-PSK": f"{keyopt}"
    }
    data = {
        "method": "setActiveApp",
        "id": 601,
        "params": [{
        "data": "",
        "uri": f"{app}"
        }],
        "version": "1.0"
    }
    req = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(req.status_code)


if __name__ == "__main__":
    main(sys.argv[1:])

import vkauth.vkauth as vkauth
import config
import urllib.parse
import urllib.request
import json
import getpass


def call_api(method, params):
    """Call VK.Api method"""
    url = "https://api.vk.com/method/%s?%s" % (
        method, urllib.parse.urlencode(params))
    return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))['response']


def delete_song(sid, aid, oid):
    params = [('access_token', sid),
              ('aid', aid),
              ('oid', oid)]
    response = call_api('audio.delete', params)
    return response


def get_songs(sid, uid, count=0):
    params = [('access_token', sid),
              ('uid', uid)]
    if count is not 0:
        params.append(('count', count))

    response = call_api('audio.get', params)

    songs_ids = []
    for item in response:
        songs_ids.append(item['aid'])

    return songs_ids


def main():
    api_id = config.authorization_data['api_id']
    api_secret = config.authorization_data['api_secret']
    email = config.authorization_data['email']
    password = config.authorization_data['password']

    if password == '':
        password = getpass.getpass()

    sid, oid = vkauth.auth(email, password, api_id, "audio")

    for aid in get_songs(sid, oid, 1):
        delete_song(sid, aid, oid)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3

from textwrap import fill, indent
from bs4 import BeautifulSoup
import requests
import asyncio
import json

api_url = 'https://api.stackexchange.com/2.2/users/'


def slice_dict(dict, slice):
    s_len = len(slice)
    return {key[s_len:]: value for key,value in dict.items()
                                             if key.startswith(slice)}


def get_user_by_uid(site, uid):
    params = {
        'site': site,
        'filter': '!9YdnSA07B',
    }
    res = requests.get(api_url + str(uid), params=params)
    res = json.loads(res.text)

    return res['items'][0]


def get_users_by_name(site, name=''):
    params = {
        'site': site,
        'inname': name,
        'filter': '!9YdnSA07B',
    }
    res = requests.get(api_url, params=params)
    res = json.loads(res.text)

    return res['items']


def format_url(url):
    return '<{}>'.format(url)


def format_field(key, value=None, indent=1):
    if not value:
        return '{}:: {}\n'.format(' '*indent, key)

    return '{}:: {} {}\n'.format(' '*indent, key, value)


def format_header(header, filler):
    header = str(header)
    header_len = len(header)
    filler_len = 80 - header_len - (3 + 2)

    msg = '{pre_fil} {header} {post_fil}\n'.format(**{
        'pre_fil': filler * 3,
        'header': header,
        'post_fil': filler * filler_len,
    })
    return msg


def format_rep_changes(user):
    changes = slice_dict(user, 'reputation_')
    msg = ''
    if changes['change_day'] > 0:
        msg += format_field('day', '+' + str(changes['change_day']), indent=3)
    if changes['change_quarter'] > 0:
        msg += format_field('quarter', '+' + str(changes['change_quarter']), indent=3)
    if changes['change_year'] > 0:
        msg += format_field('year', '+' + str(changes['change_year']), indent=3)

    if len(msg) > 0:
        msg = format_field('reputation changes') + msg

    return msg


def format_user(user, long_output=True):
    msg = '\n'
    msg += format_header(user['account_id'], '=')
    msg += format_field('uid', user['user_id'])
    msg += format_field('name', user['display_name'])
    msg += format_field('reputation', user['reputation'])
    if 'location' in user:
        msg += format_field('location', user['location'])

    msg += format_field('profile', format_url(user['link']))
    if 'website_url' in user and len(user['website_url']) > 0:
        msg += format_field('website', format_url(user['website_url']))

    msg += format_rep_changes(user)
    msg += '\n'

    if long_output and 'about_me' in user:
        msg += format_header('About User', '-') + '\n'

        soup = BeautifulSoup(user['about_me'])
        text = soup.get_text()

        lines = [ line for line in text.splitlines() if line.strip() ]
        for line in lines:
            msg += indent(fill(line), '  ') + '\n\n'

    return msg


@asyncio.coroutine
def handle_client(reader, writer):
    line = yield from reader.readline()
    line = line.decode('utf-8').strip()

    if '@' not in line:
        writer.write('Error: Username or site missing\n'.encode('utf-8'))
        writer.close()
        return

    user, site = line.split('@')
    if user.startswith('/W'):
        long_output = True
        user = user[3:]
    else:
        long_output = False

    try:
        uid = int(user)
        users = [get_user_by_uid(site, uid)]
    except ValueError:
        users = get_users_by_name(site, user)

    for user in users:
        if user['user_type'] == 'unregistered':
            continue

        msg = format_user(user, long_output)
        writer.write(msg.encode('utf-8'))

    writer.close()


loop = asyncio.get_event_loop()

coro = asyncio.start_server(handle_client, host='0.0.0.0', port=79, loop=loop)
server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

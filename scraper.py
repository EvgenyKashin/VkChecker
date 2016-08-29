# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 14:00:41 2016

@author: EvgenyKashin
"""


import requests
import pandas as pd
import json
from pandas import DataFrame
import time
import os
import private


def get_JSON_data(url):
    d = requests.get(url)
    return json.loads(d.text)


def load_df(vk_method, vk_id):
    data = get_JSON_data('https://api.vk.com/method/' + vk_method +
                         '?uid=' + vk_id + '&fields=first_name,last_name,sex')
    if 'items' in data['response']:
        df = DataFrame(data['response']['items'])
    else:
        df = DataFrame(data['response'])
    if 'deactivated' in df:
        df.drop('deactivated', axis=1, inplace=True)
    if 'hidden' in df:
        df.drop('hidden', axis=1, inplace=True)
    return df


def compare_df(a, b):
    df = pd.concat([a, b], ignore_index=True)
    df_temp = df.drop(['first_name', 'last_name', 'sex'], axis=1)
    try:
        df_temp = df_temp.drop('lists', axis=1)
    except:
        pass
    df_g = df_temp.groupby(list(df_temp.columns))
    idx = [x[0] for x in df_g.groups.values() if len(x) == 1]
    return df.reindex(idx)


def check_friends(vk_id):
    try:
        old_df = pd.read_csv('id' + vk_id + '/old_friends.csv')
    except Exception:
        old_df = load_df('friends.get', vk_id)
        # maximum 3 requests to API methods per second
        time.sleep(0.33)
    new_df = load_df('friends.get', vk_id)
    dif = compare_df(old_df, new_df)

    # update data in storage
    new_df.to_csv('id' + vk_id + '/old_friends.csv', index=None,
                  encoding='utf-8')
    if dif.size == 0:
        return('No new friends')
    result = ''
    for i in dif.index:
        item = dif.ix[i]
        if new_df[new_df.uid == item.uid].size != 0:
            result += str(item) + ' added to friends\n'
        elif old_df[old_df.uid == item.uid].size != 0:
            result += str(item) + ' deleted from friends\n'
        else:
            result += str(item) + ' unknown result\n'
    return result


def check_followers(vk_id):
    try:
        old_df = pd.read_csv('id' + vk_id + '/old_followers.csv')
    except Exception:
        old_df = load_df('users.getFollowers', vk_id)
        # maximum 3 requests to API methods per second
        time.sleep(0.33)
    new_df = load_df('users.getFollowers', vk_id)
    dif = compare_df(old_df, new_df)

    # update data in storage
    new_df.to_csv('id' + vk_id + '/old_followers.csv', index=None,
                  encoding='utf-8')
    if dif.size == 0:
        return('No new followers')
    result = ''
    print(dif)
    for i in dif.index:
        item = dif.ix[i]
        if new_df[new_df.uid == item.uid].size != 0:
            result += str(item) + ' added to followers\n'
        elif old_df[old_df.uid == item.uid].size != 0:
            result += str(item) + ' deleted from followers\n'
        else:
            result += str(item) + ' unknown result\n'
    return result


def check_user(vk_id):
    try:
        os.mkdir('id' + vk_id)
    except:
        pass

    last_result = check_friends(vk_id) + '\n' + check_followers(vk_id)
    with open('id' + vk_id + '/last_result.txt', 'w') as lr:
        lr.write(last_result)
    with open('id' + vk_id + '/log.txt', 'a') as log:
        log.write(time.strftime('%x') + ' ' + time.strftime('%X') + '\n')
        log.write(last_result + '\n\n')


def do_scrape(ids):
    for id in ids:
        check_user(id)


if __name__ == '__main__':
    do_scrape(private.VK_IDS)
    print('Done!')

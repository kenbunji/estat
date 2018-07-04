# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import six

from tqdm import tqdm
from builtins import bytes
from builtins import dict

from estat import e_Stat_API_Adaptor


def download(directory=os.environ['HOME'] + '/estat/'):
    if (directory[-1:] != '/'):
        directory += '/'

    print('Please input the e-Stat appID. You can get the appID from e-Stat website: https://www.e-stat.go.jp/')

    if six.PY2:
        appId = raw_input('appID> ')
    else:
        appId = input('appID> ')

    eStatAPI = e_Stat_API_Adaptor.e_Stat_API_Adaptor({
        # 取得したappId
        'appId': appId
        # データをダウンロード時に一度に取得するデータ件数
        # next_keyに対応するか否か(非対応の場合は上記のlimitで設定した件数のみしかダウンロードされない)
        , 'limit': '10000'
        # 対応時はTrue/非対応時はFalse
        , 'next_key': True
        # 中間アプリの設置ディレクトリ
        , 'directory': directory
        # APIのバージョン
        , 'ver': '2.0'
    })

    # 全ての統計表IDをローカルにダウンロード
    print(eStatAPI.load_all_ids())

    # ダウンロードした統計表IDからインデックスを作成
    print('indexing IDs...')
    rows = eStatAPI.build_statid_index()
    if rows is None:
        print('Error detected. Exit program.')
        return

    # データのダウンロード
    print('getting csv files')
    if six.PY2:
        rows = unicode(rows, 'utf-8')
    for r in tqdm(rows.split('\n')):
        eStatAPI.get_csv('get', r.split('-')[0])
    print('csv files are stored to {}.'.format(eStatAPI.path['csv']))

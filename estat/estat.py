# -*- coding: utf-8 -*-
import os

from tqdm import tqdm

import e_Stat_API_Adaptor


def download(directory=os.environ['HOME'] + '/estat/'):
    if (directory[-1:] != '/'):
        directory += '/'

    print('Please input the e-Stat appID. You can get the appID from e-Stat website: https://www.e-stat.go.jp/')
    appId = raw_input('appID> ')

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
    for r in tqdm(rows.split('\n')):
        eStatAPI.get_csv('get', r.split('-')[0])
    print('csv files are stored to {}.'.format(eStatAPI.path['csv']))

# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#
#  e-Stat API Adaptor rev
#  Arrange
#  Original (c) 2016 National Statistics Center
#  License: MIT
#
# # # # # # # # # # # # # # # # # # # # # # # #

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import csv
import json
import os
import six
import subprocess

from builtins import bytes
from builtins import dict


class e_Stat_API_Adaptor:
    def __init__(self, _):
        # アプリ設定
        self._ = _
        # パス設定
        self.path = {
            # データダウンロード時に使用するディレクトリ
            'tmp': self._['directory'] + 'tmp/',  # indexを作成するパス

            # CSVのディレクトリ
            'csv': self._['directory'] + 'data-cache/',

            # 全ての統計IDを含むJSONファイルのパス
            'statid-json': self._['directory'] + 'dictionary/all.json.dic',
            'dictionary-index': self._['directory'] + 'dictionary/index.list.dic'
        }
        self.url = {
            'host': 'http://api.e-stat.go.jp', 'path': '/'.join([
                'rest', self._['ver'], 'app', 'json', 'getStatsData'
            ])
        }

        self.header = {'Access-Control-Allow-Origin': '*'}
        self.random_str = 'ABCDEFGHIJKLMNOPQRTSUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        self.cache = {}

    # ファイル保存先のディレクトリが無ければ作成する
    def make_dir(self, filename):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            print('make directory ' + path)
            os.makedirs(path)

    # 全ての統計IDをダウンロード

    def load_all_ids(self):
        load_uri = self.build_uri({
            'appId': self._['appId'], 'searchWord': ''
        }).replace('getStatsData', 'getStatsList')
        # 全ての統計ID（json形式）を保存するディレクトリを作成する
        self.make_dir(self.path['statid-json'])
        self.cmd_line(self.build_cmd([
            'curl', '-o', self.path['statid-json'], '"' + load_uri + '"'
        ]))

    # ダウンロードした統計表からインデックスファイルを作成する

    def build_statid_index(self):
        result_jd = self.load_json(self.path['statid-json'])['GET_STATS_LIST']['RESULT']
        print('Tried downloading all ids. Status code: {0} and message : {1}'.format(result_jd['STATUS'],
                                                                                     result_jd['ERROR_MSG']))
        if result_jd['STATUS'] != 0:
            print('Error detected in loading all ids. Check appID.')
            return None

        jd = self.load_json(
            self.path['statid-json'])['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']

        if six.PY2:
            # Python 2
            rows = '\n'.join([
                '-'.join([
                    j['@id'], j['STAT_NAME']['$'], str(j['SURVEY_DATE']), j['GOV_ORG']['$'], j[
                        'MAIN_CATEGORY']['$'], j['SUB_CATEGORY']['$']
                ]) + '.dic'
                for j in jd
            ]).encode('utf-8')
        else:
            # Python 3
            rows = '\n'.join([
                '-'.join([
                    j['@id'], j['STAT_NAME']['$'], str(j['SURVEY_DATE']), j['GOV_ORG']['$'], j[
                        'MAIN_CATEGORY']['$'], j['SUB_CATEGORY']['$']
                ]) + '.dic'
                for j in jd
            ])

        with open(self.path['dictionary-index'], 'w') as f:
            f.write(rows)
        return rows

    def build_uri(self, param):
        return '?'.join([
            '/'.join([self.url['host'], self.url['path']]
                     ), '&'.join([k + '=' + str(v) for k, v in param.items()])
        ])

    def build_cmd(self, cmd_list):
        return ' '.join(cmd_list)

    def cmd_line(self, cmd):
        # try:
        if six.PY2:
            return subprocess.check_output(cmd, shell=True)
        else:
            return subprocess.check_output(cmd, shell=True).decode()
            # except:
            #     return None

    def load_json(self, path):
        try:
            with open(path) as json_data:
                return json.load(json_data)
        except:
            print('File {} is collapsed. Remove the file.'.format(path))
            return None

    def get_all_data(self, statsDataId, next_key):
        print('126 ' + self.path['tmp'] + self._['appId'] + statsDataId)
        print('127', next_key)
        self.cache['tmp'] = self.path['tmp'] + '.'.join([self._['appId'], statsDataId, next_key, 'json'])
        # try:
        if os.path.exists(self.cache['tmp']) == False:
            apiURI = self.build_uri({
                'appId': self._['appId'], 'statsDataId': statsDataId, 'limit': self._['limit'],
                'startPosition': next_key
            })
            self.make_dir(self.cache['tmp'])
            self.cmd_line(self.build_cmd(
                ['curl', '-o', self.cache['tmp'], '"' + apiURI + '"'])).replace('\n', '')
        RESULT_INF = self.load_json(self.cache['tmp'])['GET_STATS_DATA'][
            'STATISTICAL_DATA']['RESULT_INF']
        NEXT_KEY = '-1' if 'NEXT_KEY' not in RESULT_INF.keys() else RESULT_INF[
            'NEXT_KEY']
        return str(NEXT_KEY)
        # except:
        #     # 下記のエラー処理は考える
        #     filepath = self.path[
        #                    'tmp'] + '.'.join([self._['appId'], statsDataId, '*', 'json'])
        #     try:
        #         downloaded_files = self.cmd_line(
        #             self.build_cmd(['ls', filepath]))
        #         if downloaded_files != '':
        #             self.remove_file(filepath)
        #         return None
        #     except:
        #         return None

    def convert_raw_json_to_csv(self, statsDataId):
        try:
            self.cache['csv'] = self.path['csv'] + statsDataId + '.csv'
            dat = {'header': None, 'body': [], 'keys': None}
            ix = [
                {int(f.split('.')[1]): f}
                for f in self.cmd_line(
                    self.build_cmd(
                        ['ls', self.path['tmp'] + '.'.join([self._['appId'], statsDataId, '*', 'json'])])
                ).split('\n')
                if f != ''
            ]
            ix.sort()
            ix = [list(hash.values())[0] for hash in ix]
            for i, json_file in enumerate(ix):
                jd = self.load_json(json_file)
                if i == 0:
                    dat['header'] = [
                        k.replace('@', '')
                        for k in jd['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE'][0].keys()
                    ]
                    dat['keys'] = jd['GET_STATS_DATA'][
                        'STATISTICAL_DATA']['CLASS_INF']
                dat['body'].extend(jd['GET_STATS_DATA'][
                                       'STATISTICAL_DATA']['DATA_INF']['VALUE'])
            _h = {}
            _b = {}
            for o in dat['keys']['CLASS_OBJ']:
                o['CLASS'] = [o['CLASS']] if (
                                                 type(o['CLASS']) is list) is False else o['CLASS']
                if o['@id'] not in _b.keys():
                    _b[o['@id']] = {}
                for oc in o['CLASS']:
                    _b[o['@id']][oc['@code']] = oc['@name']
                _h[o['@id']] = o['@name']
            if six.PY2:
                newCSV = [[r.encode('utf-8') for r in [_h[h] if h in _h.keys() else h for h in dat['header']]]]
            else:
                newCSV = [[r for r in [_h[h] if h in _h.keys() else h for h in dat['header']]]]
            newCSV.append(dat['header'])
            for body in dat['body']:
                newCSV.append(list(body.values()))
            for i, x in enumerate(newCSV):
                if i > 0:
                    for j, d in enumerate(x):
                        if dat['header'][j] in _b.keys() and d in _b[dat['header'][j]].keys():
                            if six.PY2:
                                newCSV[i][j] = _b[dat['header'][j]][d].encode('utf-8')
                            else:
                                newCSV[i][j] = _b[dat['header'][j]][d]
                        else:
                            if six.PY2:
                                newCSV[i][j] = d.encode('utf-8')
                            else:
                                newCSV[i][j] = d
            self.make_dir(self.cache['csv'])
            with open(self.cache['csv'], 'w') as f:
                csv.writer(f, quoting=csv.QUOTE_NONNUMERIC).writerows(newCSV)
            filepath = self.path[
                           'tmp'] + '.'.join([self._['appId'], statsDataId, '*', 'json'])
            self.cmd_line(self.build_cmd(['rm', filepath]))

        except:
            filepath = self.path[
                           'tmp'] + '.'.join([self._['appId'], statsDataId, '*', 'json'])
            if os.path.exists(filepath):
                self.cmd_line(self.build_cmd(['rm', filepath]))

    def remove_file(self, filepath):
        self.cmd_line(self.build_cmd([
            'rm', filepath
        ]))

    def get_csv(self, cmd, statsDataId):
        cmd = 'cat' if cmd == 'get' else cmd
        self.cache['csv'] = self.path['csv'] + statsDataId + '.csv'

        if os.path.exists(self.cache['csv']) == False:
            next_key = '1'
            if self._['next_key'] == True:
                while next_key != '-1':
                    next_key = self.get_all_data(statsDataId, next_key)
            else:
                self.get_all_data(statsDataId, next_key)
            self.convert_raw_json_to_csv(statsDataId)
        txt = self.cmd_line(self.build_cmd([
            cmd, self.cache['csv'], " | awk 'NR != 2 { print $0; }'"
        ])) if cmd == 'cat' or cmd == 'head' else self.cmd_line(self.build_cmd([
            cmd, self.cache['csv']
        ]))
        return txt

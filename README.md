# estat
Download data from Japanese Government Statistics and save it as CSV format files.
各府省等が公表する統計データがまとめられた政府統計の総合窓口（e－Stat）からデータをダウンロードし、CSV形式のファイルに保存します。

# How to use
* First you must get appID from e-Stat site from here (https://www.e-stat.go.jp/).
まずe-Stat (https://www.e-stat.go.jp/)からappIDを取得します。
* Next do the followings.
次に下記のコマンドを実行します。
```
>>> import estat
>>> estat.download()
```
You can find csv format files in $HOME/estat/data-cache.
$HOME/estat/data-cache ディレクトリにCSV形式のデータファイルが生成されます。

If you want to change estat directory from $HOME/estat, do the following.
```
>>> estat.download(directory='/home/hoge/data/estat/')
```
If you cannot download the CSV format files,
check the appID and curl settings in ~/.curlrc or /etc/.curlrc for your proxy server settings.
```
$ cat proxy ~/.curlrc
```

# Author
kenbunji
https://github.com/kenbunji/estat

# License
Licensed under the MIT license.

# Remarks
This program is created referring to this site
https://github.com/e-stat-api/adaptor

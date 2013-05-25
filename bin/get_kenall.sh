#!/bin/sh
rm -f ../db/ken_all.lzh
rm -f ../db/ken_all.csv
rm -f ../db/ken_all_utf8.csv
rm -f ../db/area.csv
rm -f ../db/net.csv

wget --output-document=../db/ken_all.lzh http://www.post.japanpost.jp/zipcode/dl/kogaki/lzh/ken_all.lzh
lha -ew=../db/ ../db/ken_all.lzh
nkf -SwdO ../db/ken_all.csv ../db/ken_all_utf8.csv
python ./make_loaddata.py ../db/ken_all_utf8.csv ../db/area.csv ../db/net.csv
sqlite3 ../db/zip_db < ./zipcode.sql

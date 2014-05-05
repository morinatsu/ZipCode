#!/bin/bash

echo '***** get_kenall.sh *****'
echo "[" `date "+%Y/%m/%d %H/%M"` "]"

homedir=/home/morinatsu/bin/ZipCode/
dbdir=${homedir}/db/
bindir=${homedir}/bin/

echo "homedir: ${homedir}"
echo "dbdir: ${dbdir}"
echo "bindir: ${bindir}"

rm -f ${dbdir}/ken_all.lzh
rm -f ${dbdir}/ken_all.csv
rm -f ${dbdir}/ken_all_utf8.csv
rm -f ${dbdir}/area.csv
rm -f ${dbdir}/net.csv

wget --quiet \
     --output-document=${dbdir}/ken_all.lzh \
     http://www.post.japanpost.jp/zipcode/dl/kogaki/lzh/ken_all.lzh
lha -ew=${dbdir} ${dbdir}/ken_all.lzh
nkf -SwdO ${dbdir}/ken_all.csv ${dbdir}/ken_all_utf8.csv
python ${bindir}/make_loaddata.py \
       ${dbdir}/ken_all_utf8.csv \
       ${dbdir}/area.csv ${dbdir}/net.csv
cd ${bindir}
sqlite3 ${dbdir}/zip_db < ${bindir}/zipcode.sql

exit 0

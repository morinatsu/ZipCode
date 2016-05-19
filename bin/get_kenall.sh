#!/bin/bash -xv

# Download zipcode file and reload

set -e

logdir=/var/log
logfile=${logdir}/$(basename $0).log
exec 2> ${logfile}

logger --stderr --priority user.info '***** get_kenall.sh *****'

homedir=/home/morinatsu/
dbdir=${homedir}/db/
bindir=${homedir}/bin/

rm -f ${dbdir}/ken_all.lzh
rm -f ${dbdir}/ken_all.csv
rm -f ${dbdir}/ken_all_utf8.csv
rm -f ${dbdir}/area.csv
rm -f ${dbdir}/net.csv

wget --quiet \
     --output-document=${dbdir}/ken_all.zip \
     http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip
unzip -L ${dbdir}/ken_all.zip -d ${dbdir}
nkf -SwdO ${dbdir}/ken_all.csv ${dbdir}/ken_all_utf8.csv
python ${bindir}/make_loaddata.py \
       ${dbdir}/ken_all_utf8.csv \
       ${dbdir}/area.csv ${dbdir}/net.csv
cd ${bindir}
sqlite3 ${dbdir}/zip_db < ${bindir}/zipcode.sql

exit 0

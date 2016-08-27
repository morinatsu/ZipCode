#!/bin/bash -xv

# Download zipcode file and reload

set -e

logdir=/var/log
logfile=${logdir}/$(basename $0).log
exec >> "${logfile}"
exec 2>&1

logger --stderr --priority user.info '***** get_kenall.sh begin *****'

homedir=/home/morinatsu/
dbdir=${homedir}/db/
bindir=${homedir}/bin/

rm -f ${dbdir}/ken_all.lzh
rm -f ${dbdir}/ken_all.csv
rm -f ${dbdir}/ken_all_utf8.csv
rm -f ${dbdir}/area.csv
rm -f ${dbdir}/net.csv

logger --stderr --priority user.info 'Downloading ken_all.zip...'
wget --quiet \
     --output-document=${dbdir}/ken_all.zip \
     http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip

logger --stderr --priority user.info 'Unzipping ken_all.zip...'
unzip -L ${dbdir}/ken_all.zip -d ${dbdir}

logger --stderr --priority user.info 'Convert encoding of csv-file...'
nkf -SwdO ${dbdir}/ken_all.csv ${dbdir}/ken_all_utf8.csv

logger --stderr --priority user.info 'Making loaddata...'
python ${bindir}/make_loaddata.py \
       ${dbdir}/ken_all_utf8.csv \
       ${dbdir}/area.csv ${dbdir}/net.csv

logger --stderr --priority user.info 'Loading zipcode data...'
cd ${bindir}
sqlite3 ${dbdir}/zip_db < ${bindir}/zipcode.sql

logger --stderr --priority user.info '***** get_kenall.sh end *****'
exit 0

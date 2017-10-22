#!/bin/bash -xv

# Download zipcode file and reload

set -e

homedir=/home/morinatsu/
dbdir=${homedir}/db/
bindir=${homedir}/bin/
logdir=${homedir}/log/
logfile=${logdir}/get_kenall.log
touch "${logfile}"

echo "***** get_kenall.sh begein at $(date '+%Y-%m-%dT%H:%M:%S') *****" >> "${logfile}" 2>&1

logger --stderr --priority user.info '***** get_kenall.sh begin *****'

rm -f ${dbdir}/ken_all.lzh
rm -f ${dbdir}/ken_all.csv
rm -f ${dbdir}/ken_all_utf8.csv
rm -f ${dbdir}/area.csv
rm -f ${dbdir}/net.csv

{
logger --stderr --priority user.info 'Downloading ken_all.zip...'
wget --quiet \
     --output-document=${dbdir}/ken_all.zip \
     http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip
} >> "${logfile}" 2>&1

{
logger --stderr --priority user.info 'Unzipping ken_all.zip...'
unzip -L ${dbdir}/ken_all.zip -d ${dbdir}
} >> "${logfile}" 2>&1

{
logger --stderr --priority user.info 'Convert encoding of csv-file...'
nkf -SwdO ${dbdir}/ken_all.csv ${dbdir}/ken_all_utf8.csv
}

{
logger --stderr --priority user.info 'Making loaddata...'
python ${bindir}/make_loaddata.py \
       ${dbdir}/ken_all_utf8.csv \
       ${dbdir}/area.csv ${dbdir}/net.csv
} >> "${logfile}" 2>&1

{
logger --stderr --priority user.info 'Loading zipcode data...'
cd ${bindir}
sqlite3 ${dbdir}/zip_db < ${bindir}/zipcode.sql
} >> "${logfile}" 2>&1

logger --stderr --priority user.info '***** get_kenall.sh end *****'
echo "***** get_kenall.sh end at $(date '+%Y-%m-%dT%H:%M:%S') *****" >> "${logfile}" 2>&1
exit 0

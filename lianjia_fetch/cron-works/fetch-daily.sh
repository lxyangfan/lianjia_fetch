#!/bin/sh
PATH=/home/ubuntu/bin:/home/ubuntu/.local/bin:/opt/anaconda2/bin:/usr/lib/jvm/java-8-oracle//bin:/home/ubuntu/anaconda2/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
python /home/ubuntu/Documents/lianjia_fetch/lianjia_fetch/fetch_lianjia.py  2>&1 1 >>  /home/ubuntu/Documents/lianjia_fetch/lianjia_fetch/py-logs.txt
git add .
git commit -m "AWS cron auto fetch"
git push

#!/bin/sh
PATH=/home/ubuntu/bin:/home/ubuntu/.local/bin:/opt/anaconda2/bin:/usr/lib/jvm/java-8-oracle//bin:/home/ubuntu/anaconda2/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin

git add data/
git commit -m "AWS cron auto fetch"
git push origin linuxDev
echo "AWS cron auto fetch and commited..."

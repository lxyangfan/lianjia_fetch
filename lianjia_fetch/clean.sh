#!/bin/bash
echo "Clean logs"
echo "" > logs.txt
echo "" > time.txt
sudo chmod 777 logs.txt time.txt
echo "Restart Cron service"
sudo service cron restart
echo "Restart finished"

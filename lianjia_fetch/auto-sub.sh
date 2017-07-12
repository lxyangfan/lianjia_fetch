echo "Start to commit and push..."
echo 1
git add . 
echo 2
sleep 2
git commit -m "Auto Commit from AWS"
echo 3
sleep 3
git push origin linuxDev
echo 4
sleep 4
echo "Commit and push successfully..."

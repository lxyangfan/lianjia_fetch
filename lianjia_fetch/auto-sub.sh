echo "Start to commit and push..."

git add . 
git commit -m "Auto Commit from AWS"
git push origin linuxDev
sleep 4
echo "Commit and push successfully..."

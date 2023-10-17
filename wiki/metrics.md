sudo apt install -y python3-pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip3 install python-telegram-bot==13.15
pip3 install psutil
pip install aiofiles

pkill -f "python-daemon metrikV2.py"
ps aux | grep metrikV2.py

nohup python metrikV2.py &

nohup python3 metrikV2.py > my.log 2>&1 & echo $! > save_pid.txt

kill -9 `cat save_pid.txt` & rm save_pid.txt

kill -SIGTERM $(ps aux | grep "python3 /home/cat/Documents/GitHubProgerts/lp/metricks/metrikV2.py" | awk '{print $2}')
kill -SIGTERM $(ps aux | grep "python metrikV2.py" | awk '{print $2}')

https://qna.habr.com/q/559461
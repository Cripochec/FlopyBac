#!/bin/bashcd /root/FlopyBac
git pull origin mainsource venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart FlopyBac
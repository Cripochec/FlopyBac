#!/bin/bashcd /root/FlopyBac
cd /root/FlopyBac
git pull origin main
pip install -r requirements.txt
sudo supervisorctl restart FlopyBac
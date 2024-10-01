#!/bin/bash
cd /root/FlopyBac  # Перейти в директорию проекта
git pull origin main  # Обновить код из репозитория
pip install -r requirements.txt  # Установить/обновить зависимости
sudo supervisorctl restart FlopyBac  # Перезапустить приложение через Supervisor

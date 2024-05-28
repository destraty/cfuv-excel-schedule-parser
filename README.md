# Парсер расписаний Крымского Федерального Университета
Это относительно урезанная версия программы для понимания концепции работы, выявления багов и улучшения проекта.

# Установка и запуск
## На Windows
Скачайте и установите ```Python 3.11.7```, если у вас все еще его нет [отсюда](https://www.python.org/downloads/release/python-3117/).

Скачайте и установите ```Java 1.8.0``` по этой [ссылке](https://www.oracle.com/cis/java/technologies/javase/javase8-archive-downloads.html)

Перезагрузите компьютер.

Скачайте файлы из репозитория командой:
```bash
git clone https://github.com/destraty/cfuv-excel-schedule-parser
```
###### P.S. Что такое GIT и как его [установить](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Перейдтие в папку с проектом:
```bash
cd cfuv-excel-schedule-parser
```
Установите все зависимости командой и дождитесь их установки:
```bash
python -m pip install -r ./requirements.txt
```
Запустите проект:
```bash
python server.py
```
Полный запуск может занять до 30 минут.

Перейдите по ссылке ```http://127.0.0.1:5000/docs``` или ознакомьтесь с документацией полученного API 

## На Linux
Установите Python 3.11 из [гайда](https://www.linuxcapable.com/how-to-install-python-3-11-on-ubuntu-linux/)

Установите JDK 1.8.0 
```
sudo apt update
sudo apt-get install openjdk-8-jdk
java -version
```
Не забудьте также установить переменную окружения JAVA_HOME, указав путь к директории установки Java:
```
export JAVA_HOME=/path/to/java/home
```
Добавьте эту строку в файл .bashrc или .profile в вашем домашнем каталоге, чтобы она автоматически выполнялась при входе в систему.

Перезагрузите систему.

Скачайте файлы из репозитория командой:
```bash
git clone https://github.com/destraty/cfuv-excel-schedule-parser
```
###### P.S. Что такое GIT и как его [установить](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Перейдтие в папку с проектом:
```bash
cd cfuv-excel-schedule-parser
```
Установите все зависимости командой и дождитесь их установки:
```bash
python -m pip install -r ./requirements.txt
```
Запустите проект:
```bash
python server.py
```
При необходимости создайте ```.service``` файл. Пример:
```linux
[Unit]
Description=Schedule Service
After=network.target

[Service]
Type=simple
User=ПОЛЬЗОВАТЕЛЬ
WorkingDirectory=/home/ПОЛЬЗОВАТЕЛЬ
ExecStart=/usr/bin/python3.11 ПУТЬ_К_ИСПОЛНЯЕМОМУ_ФАЙЛУ/server.py
Environment=PYTHONPATH=/home/ПОЛЬЗОВАТЕЛЬ/

[Install]
WantedBy=multi-user.target
```

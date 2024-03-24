import json
import keyboard as kb
import os
import csv
from pywinauto import Application, keyboard, mouse
import time 
import pyperclip
import datetime

# chrome_dir = "C:\Program Files\Google\Chrome\Application\chrome.exe"
# chrome = Application(backend='uia')
# chrome.start(chrome_dir + ' --force-renderer-accessibility --start-maximized ' 'https://1xbet.com/allgamesentrance/crash')
# time.sleep(10)
# # открытие devtools
# keyboard.send_keys('{F12}')
# time.sleep(5)
# # Открытие вкладки Сеть
# keyboard.send_keys('^4')
# time.sleep(5)
# # перезагрузка и начало получения статистики
# keyboard.send_keys('{F5}')
# time.sleep(30)
# # сортировка по WS
# mouse.click(button='left', coords=(3642, 171))
# time.sleep(5)
# # переход в окно websocket наименование crash
# mouse.click(button='left', coords=(3201, 331))
# time.sleep(5)
stop_pressed = False  # Переменная, чтобы показать, что стоп клавиша была нажата

def stop_callback(event):
    global stop_pressed
    stop_pressed = True

kb.on_press_key('q', stop_callback)
    
l = -1
f = -1
ts = -1
won = -1
n = -1
d = -1
bid = -1
a = -1
w = -1
last_data = ''
count = 0
count_r = 0
current_datetime = ''
file_name = 'my_file.csv'
# Проверка существования файла
if not os.path.exists(file_name):
    # Создание файла
    with open(file_name, 'w', newline='') as csvfile:
        # Создание объекта writer
        writer = csv.writer(csvfile)
        # Запись заголовков
        writer.writerow(['data','session', 'multiplier', 'session_ls', 'win_amount', 'number', 'death', 'Amount', 'a', 'w'])

while not stop_pressed:

    time.sleep(1)
    mouse.press(button='left', coords=(3373, 377))
    # клик по сообщениям websocket
    time.sleep(1)
    mouse.release(button='left', coords=(3818, 842))
    # keyboard.send_keys('^a')
    # копирование в буфер
    keyboard.send_keys('^c')
    # сброс выделения
    time.sleep(1)
    mouse.press(button='left', coords=(3257, 918))
    # чтение из буфера в переменную
    value = pyperclip.paste()
    # отрезание окончания RS
    value_str = value[:-1]
    value_pr = value.split()
    
    if count >= 3:
        mouse.press(button='left', coords=(3239, 326))
        count_r += 1
        count = 0
    if value_pr == last_data:
        count += 1
        continue
    else:
        count = 0
    if count_r >= 30:
        keyboard.send_keys('{F5}')
        time.sleep(30)
        # сортировка по WS
        mouse.click(button='left', coords=(3057, 82))
        time.sleep(5)
        # переход в окно websocket наименование crash
        mouse.click(button='left', coords=(2078, 216))
        time.sleep(5)
    last_data = value_pr   
    
    for i in range(0,len(value_pr),3):
        list_value = [current_datetime, l, f, ts, won, n, d, bid, a, w]
        value_i = value_pr[i]
        value_str = value_i
        value_json = json.loads(value_str)
        if 'target' in value_json:    
                    
            if value_json['target'] == 'OnCrash':
                l = value_json['arguments'][0]['l']
                f = value_json['arguments'][0]['f']                
                ts = value_json['arguments'][0]['ts']   
                        
            # вытаскиваем значения сессии
            if value_json['target'] == 'OnCashouts':
                l = value_json['arguments'][0]['l']
                won = value_json['arguments'][0]['won']
                n = value_json['arguments'][0]['n']
                d = value_json['arguments'][0]['d']
                        
            if value_json['target'] == 'OnBets':
                l = value_json['arguments'][0]['l']
                bid = value_json['arguments'][0]['bid']
                        
            if value_json['target'] == 'OnStage':
                current_datetime = datetime.datetime.now()
                with open(file_name, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(list_value) 
                    print('list write')  
                    print(list_value)
                l = -1
                f = -1
                ts = -1
                won = -1
                n = -1
                d = -1
                bid = -1
                a = -1
                w = -1
                        
            if value_json['target'] == 'OnBetting':
                a = value_json['arguments'][0]['a']
                w = value_json['arguments'][0]['w']
import cv2
import numpy as np
import pyscreenshot as ps
import pytesseract
from pynput import mouse

# Задайте координаты и размеры области экрана, которую нужно захватить
click_counter = 0
xy1 = []
xy2 = []
def on_mouse_click(x, y, button, pressed):
    global click_counter
    global xy1
    global xy2
    if button == mouse.Button.left and pressed:
        click_counter += 1
        print(f'Нажатие {click_counter}: X:{x} Y:{y}')
        if click_counter in [0,1,2]:
            xy1.append(x)
            xy1.append(y)
        if click_counter in [3,4]:
            xy2.append(x)
            xy2.append(y)
        # Если достигнуто два нажатия, завершаем прослушивание
        print(xy1)
        print(xy2)
        if click_counter >= 4:
            return False

listener = mouse.Listener(on_click=on_mouse_click)
listener.start()
listener.join()

# Установите путь к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preproc(xy):
    # Захватите скриншот указанной области
    screenshot = np.array(ps.grab(bbox=(xy)))
        
    # Преобразуйте изображение в оттенки серого
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Примените адаптивную гистограммную эквализацию
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
        
    # Преобразуйте изображение в текст с помощью Tesseract
    text = pytesseract.image_to_string(contrast_enhanced)
        
    # Выведите распознанный текст
    return text, contrast_enhanced

while True:
    text_2, image_2 = preproc(xy2)
    # Выведите распознанный текст
    print("Распознанный текст:", text_2.split())
    # Отобразите скриншот
    cv2.imshow('Screenshot_2', cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB))
    
    if len(text_2)>=1:
        n1, n2, n3 = -5, -4, -2
        text_1, image_1 = preproc(xy1)
        # Выведите распознанный текст
        print("Распознанный текст:", text_1.split()[n1],text_1.split()[n2],text_1.split()[n3])
    else:
        n1, n2, = -4, -3
        text_1, image_1 = preproc(xy1)
        # Выведите распознанный текст
        print("Распознанный текст:", text_1.split()[n1],text_1.split()[n2],0)
    
    # Отобразите скриншот
    cv2.imshow('Screenshot_1', cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB))
    
    
    
    # Для выхода из цикла нажмите 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закрыть окно после выхода из цикла
cv2.destroyAllWindows()


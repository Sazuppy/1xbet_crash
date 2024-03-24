import streamlit as st
import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
import time
from sklearn.preprocessing import MinMaxScaler
import pickle

st.markdown('# Предсказание множителя игры Crash/1xbet')

with st.expander("Описание проекта:"):
    st.write(
        """Проект представляет собой попытку предсказать множитель в игре crash на площадке 1xbet.
        Данные приходят по websocket после загрузки всех игры на JS. Они формируются с помощью кликера написанного
        на библиотеке для тестирования pywinauto, который полностью автономен, в датасет, который запущен 
        локально на виртуальной машине. Алгоритм при запуске включает браузер,
        ожидает загрузку игры, переходит в режим разработчика и считывает данные. Проект не является работоспособным и будет еще 
        дорабатываться. Не решены проблемы по более быстрой передаче данных в модель, а так же качестве предсказаний. 
        """)

with st.expander("Описание данных на которых была обучена первая модель:"):    
    st.write(""" 
        * data — дата обработки строки данных
        * multiplier — множитель ставки
        * number — количество игроков сделавших ставки
        * Amount — сумма всех ставок игроков
        """
    )
    
with st.expander("Инструкция по запуску на локальной машине"):    
    st.write("""
        Для запуска на локальной машине вам необходимо установить программу для запуска виртуальной машины, 
        я использовал VMware Workstation 17 Pro, установить на виртуальной машине Google Chrome, заранее зайти в режим разработчина 
        и выставить фильтр во вкладке сеть на WS (websocket). В файле кликера prs_new.py выставить точки для кликера для своего разрешения экрана с 
        помощью mouse.py. Для понимания приложены скриншоты. В виртуальной машине выставить общей папкой текущую директорию расположения скриптов и 
        csv файлов, для постоянной записи и считывания. Указать путь к файлам согласно вашего расположения. Запустить файлы prs_new.py и streamlit_info.py   
        """)
    st.image("1.png")
    st.image("2.png")
    st.image("3.png")
    st.image("4.png")
    
    
@st.cache_resource
def get_model():

    model_c = pickle.load(open('model_catboost_prs.pkl', 'rb'))
    model_l = pickle.load(open('model_lgbm_prs.pkl', 'rb'))
    scaler_model = pickle.load(open('scaler_prs.pkl', 'rb'))
    return model_c, model_l, scaler_model

model_c, model_l, scaler_model = get_model()
    
def process_prediction(model_c, model_l, scaler_model):
    while True:
        try:
            data_new = pd.read_csv(r'd:\VM_win10\общая_папка\selenium_crash\my_file_new.csv')

            # for i in range(data_new.shape[0]-11,data_new.shape[0]-1):
            data = pd.read_csv(r'd:\VM_win10\общая_папка\selenium_crash\my_file.csv')
            data = data.replace(-1, np.nan)
            data = data.dropna()
            data = data.drop_duplicates(['session'])
            data = data.drop(['session','session_ls','win_amount', 'death', 'a', 'w'], axis = 1)  
            data_dict = {'data': [data_new.iloc[-1]['data']], 
                        'multiplier': [data.iloc[-1]['multiplier']], 
                        'number': [data_new.iloc[-1]['number']], 
                        'Amount': [data_new.iloc[-1]['Amount']]
                        }
            data_dict = pd.DataFrame(data_dict)
            data = pd.concat([data, data_dict], ignore_index=True)  
            data['data'] = pd.to_datetime(data['data'])
            data = data.set_index('data')
            data = data.tail(100)
            data['second'] = data.index.second
            data['minute'] = data.index.minute
            data['hour'] = data.index.hour
            for lag in range(1, 11):
                data['lag_{}'.format(lag)] = data['multiplier'].shift(lag) 
            data['rolling_mean'] = data['multiplier'].shift().rolling(10).mean()   
            data = data.drop(['multiplier'], axis = 1)
            container_1.write(data.tail(1)) 
            data[['number', 'Amount']] = scaler_model.transform(data[['number', 'Amount']])  
            y_pred_l = model_l.predict(data.tail(1))   
            y_pred_c = model_c.predict(data.tail(1))           
            container_2.write(y_pred_l)     
            container_3.write(y_pred_c)                
            time.sleep(0.1)
        except:
            continue
        
start = st.button("Запуск обработки", type="primary")
stop = st.button("Остановка обработки")
if start:
    st.write('Данные на вход')
    container_1 = st.empty()
    st.write('LGBMRegressor')
    container_2 = st.empty()
    st.write('CatBoostRegressor')
    container_3 = st.empty()
    process_prediction(model_c, model_l, scaler_model)
    
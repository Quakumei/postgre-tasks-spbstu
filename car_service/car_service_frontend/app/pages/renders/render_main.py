import datetime

import pandas as pd
import streamlit as st
from sqlalchemy import text

from pages.renders.render_tables import engine

def get_works_df(engine):
    query = "SELECT masters.id as master_id, masters.name, COUNT(works.id) as works_count FROM masters LEFT JOIN works on masters.id = works.master_id AND works.date_work = CURRENT_DATE GROUP BY masters.id"
    with engine.connect() as conn:
        return conn.execute(text(query))

def get_registered_cars(engine):
    query = "SELECT cars.id, cars.num, cars.color, cars.mark FROM cars"
    with engine.connect() as conn:
        result = conn.execute(text(query))
    return result

def get_masters(engine):
    query = "SELECT id, name FROM masters"
    with engine.connect() as conn:
        result = conn.execute(text(query))
    return result

def get_registered_services(engine):
    query = "SELECT id, name, cost_our, cost_foreign FROM services"
    with engine.connect() as conn:
        result = conn.execute(text(query))
    return result

def add_work(engine, work):
    cols = ', '.join(work.columns)
    values = ', '.join([f"'{k}'" for k in work.iloc[0]])
    query = f"INSERT INTO works ({cols}) VALUES ({values})"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        conn.commit()

def get_last_month_master_works(engine, master_id):
    query = f"SELECT works.id as work_id, works.date_work as date_work, services.name as service_name, services.id as service_id, cars.num as car_num, cars.color as car_color, cars.id as car_id FROM works  LEFT JOIN cars ON cars.id = works.car_id LEFT JOIN services ON services.id = works.service_id WHERE works.master_id = {master_id} AND works.date_work > NOW() - interval '30 day'"
    with engine.connect() as conn:
        result = conn.execute(text(query))
    return pd.DataFrame(result)


def render_main():
    st.markdown(f"## Сегодня - {datetime.datetime.now().strftime('%Y-%m-%d')}")
    st.markdown("### Занятость мастеров сегодня")

    works_query_res = get_works_df(engine)
    business_df = pd.DataFrame(works_query_res).set_index('master_id').sort_values(by=['works_count','master_id'], ascending=False)
    def ap(x):
        return ['background-color: #FFFF0040' for _ in x] if x['works_count'] == 0  else ['background-color: #00ff0040' for _ in x]
    st.dataframe(business_df.style.apply(ap, axis=1))
    with st.expander("Добавить новую работу"):
        st.markdown("Чтобы создать запись о работе, пожалуйста заполните поля")
        
        date_work = None
        car_id = None
        master_id = None
        service_id = None
        
        master = st.selectbox(label="Мастер", options=sorted(get_masters(engine), key=lambda x: x[1]), index=None, format_func=lambda x: f'{x[1]} (id {x[0]})', placeholder='Выберите мастера...')
        car = st.selectbox(label="Машина", options=get_registered_cars(engine), format_func=lambda x: f'{x[1]} - {x[2]} - {x[3]} (id {x[0]})', index=None, placeholder='Выберите машину...')
        service = st.selectbox(label="Услуга", options=sorted(get_registered_services(engine)), index=None, format_func=lambda x: f'{x[1]} - Отеч. {x[2]}р. - Зарубеж. {x[3]}р. (id {x[0]})', placeholder='Выберите услугу...') 
        if master:
            master_id = master[0]
        if car:
            car_id = car[0]
        if service:
            service_id = service[0]
        date_work = st.date_input(label="Дата", value=datetime.datetime.now(), max_value=datetime.datetime.now(), format="YYYY-MM-DD")
        st.markdown("---")
        st.markdown("*Превью добавляемой работы*")
        work_df = pd.DataFrame([
             [date_work, master_id, car_id, service_id],
         ], columns=['date_work', 'master_id', 'car_id', 'service_id'])
        st.dataframe(work_df, hide_index=True)
        add = st.button("Добавить работу", disabled=not (date_work and master_id and car_id and service_id), on_click=add_work, args=(engine, work_df)) 
        
    with st.expander("Посмотреть занятость мастера"):
        master = st.selectbox(label="Мастер",key='master-check-business', options=sorted(get_masters(engine), key=lambda x: x[1]), index=None, format_func=lambda x: f'{x[1]} (id {x[0]})', placeholder='Выберите мастера...')
        if master:
            master_id = master[0]
            last_month_master_works = get_last_month_master_works(engine, master_id)
            def app(x):
                return ['background-color: #00FF0040' for _ in x] if x['date_work'].strftime("%Y-%m-%d") == datetime.datetime.now().strftime('%Y-%m-%d') else ['' for _ in x]
            if last_month_master_works.shape[0] == 0:
                st.markdown("Нет работ за последние 30 дней...")
            else:
                st.markdown("*Прим.: Зелёным отмечена сегодняшняя занятость*")
                st.dataframe(last_month_master_works.set_index('work_id').sort_values(by=['date_work','work_id'], ascending=(False, False)).style.apply(app, axis=1))

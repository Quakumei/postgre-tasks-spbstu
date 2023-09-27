import datetime 

import streamlit as st
import altair as alt

def foreign_domestic_cars_service_cost(conn):
    st.markdown("## Общая стоимость обслуживания отечественных и импортных автомобилей")
    today = datetime.datetime.now()
    month_ago = today - datetime.timedelta(days=364)
    date = st.date_input("Выберите период обслуживания машин", 
                         (month_ago, today + datetime.timedelta(days=1)), max_value=today + datetime.timedelta(days=1),
                         format="YYYY-MM-DD")
    if date and len(date)==2:
        total_service_cost_query = f"""SELECT
            cars.is_foreign,
            SUM(
                CASE WHEN cars.is_foreign THEN
                    services.cost_foreign
                ELSE
                    services.cost_our
                END) AS service_cost
        FROM
            works
            LEFT JOIN cars ON works.car_id = cars.id
            LEFT JOIN services ON works.service_id = services.id
            WHERE date_work >= '{date[0]}' AND date_work <= '{date[1]}'
        GROUP BY
            cars.is_foreign
        ORDER BY
            service_cost DESC;
        """  
        total_service_cost = conn.query(total_service_cost_query)
        c = alt.Chart(total_service_cost).mark_arc(outerRadius=80).encode(theta=alt.Theta("service_cost:Q").stack(True), color=alt.Color("is_foreign:N").legend(None))
        text = c.mark_text(radius=125, size=20).encode(text=alt.condition(alt.datum.is_foreign, alt.value("Импортные"), alt.value("Отечественные")))
        text_val = c.mark_text(radius=100, size=20).encode(text="service_cost:Q")
        c = c + text + text_val
        c = c.properties(title=f'Стоимость обслуживания по "импортности" автомобилей [{date[0]} - {date[1]}] (в RUB)')
        # c = c.configure_title(fontSize=20, anchor='middle')
        st.altair_chart(c, use_container_width=True)
        st.dataframe(total_service_cost)
    else:
        st.markdown("Ожидается ввод периода...")


def best_monthly_workers(conn) -> None:
    date = st.date_input("Выберите месяц работы мастеров", max_value=datetime.datetime.now(), format="YYYY-MM-DD")
    if date:
        d = date.replace(day=1), (date.replace(day=1)+datetime.timedelta(days=30))
        st.markdown(f"## 5 Мастеров, выполнивших наибольшое кол-во работ за {date.strftime('%Y-%m')}")
        best_workers = conn.query(f"SELECT masters.id as master_id, masters.name as master_name, COUNT(1) as works_count FROM works LEFT JOIN masters ON works.master_id = masters.id WHERE works.date_work >= '{d[0]}' AND works.date_work <= '{d[1]}' GROUP BY masters.id ORDER BY COUNT(1) DESC LIMIT 5")
        c = alt.Chart(best_workers).encode(x=alt.X('works_count', title='Кол-во выполненных работ за период'), y=alt.Y('master_name', title=['Имя мастера']), text='works_count').properties(title=f"Топ 5 мастеров по кол-ву работ [{d[0]} - {d[1]}]")
        c = c.mark_bar() + c.mark_text(align='left', dx=2)
        st.altair_chart(c, use_container_width=True)
        st.dataframe(best_workers)
    else:
        st.markdown("Ожидается ввод месяца...")

def render_reports() -> None:
    conn = st.experimental_connection("car_service_db")
    foreign_domestic_cars_service_cost(conn)
    best_monthly_workers(conn)

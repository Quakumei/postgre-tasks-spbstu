import streamlit as st
import datetime

def render_operator_console():
    conn = st.experimental_connection("car_service_db")
    st.title("Operator console")
    st.markdown("## Last year works")
    today_works = conn.query("SELECT works.id as work_id, works.date_work as date, masters.name as master_name, cars.num as car_num, cars.is_foreign as car_is_foreign, services.name as service_name, CASE WHEN cars.is_foreign THEN services.cost_foreign ELSE services.cost_our END AS service_cost FROM works LEFT JOIN masters ON works.master_id = masters.id LEFT JOIN cars ON works.car_id = cars.id LEFT JOIN services ON works.service_id = services.id WHERE works.date_work > (NOW() - interval '1 year')")
    st.dataframe(today_works)
    st.markdown("## Stats")
    d = st.date_input("Period", value=[(datetime.datetime.now() - datetime.timedelta(days=365)), datetime.datetime.now()], format='YYYY-MM-DD')
    if d and len(d) == 2:
        st.markdown(f"### Best 5 masters (by quantity of works) [{d[0]} -- {d[1]}]")
        best_workers = conn.query(f"SELECT masters.id as master_id, masters.name as master_name, COUNT(1) as works_count FROM works LEFT JOIN masters ON works.master_id = masters.id WHERE works.date_work >= '{d[0]}' AND works.date_work <= '{d[1]}' GROUP BY masters.id ORDER BY COUNT(1) DESC LIMIT 5")
        st.dataframe(best_workers)

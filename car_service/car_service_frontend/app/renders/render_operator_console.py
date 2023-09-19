import streamlit as st
import datetime
import altair as alt

def render_operator_console():
    conn = st.experimental_connection("car_service_db")
    st.title("Operator console")
    st.markdown("## Last year works")
    today_works = conn.query("SELECT works.id as work_id, works.date_work as date, masters.name as master_name, cars.num as car_num, cars.is_foreign as car_is_foreign, services.name as service_name, CASE WHEN cars.is_foreign THEN services.cost_foreign ELSE services.cost_our END AS service_cost FROM works LEFT JOIN masters ON works.master_id = masters.id LEFT JOIN cars ON works.car_id = cars.id LEFT JOIN services ON works.service_id = services.id WHERE works.date_work > (NOW() - interval '1 year')")
    st.dataframe(today_works)
    st.markdown("## Stats")
    d = st.date_input("Period", value=[(datetime.datetime.now() - datetime.timedelta(days=365)), datetime.datetime.now()], format='YYYY-MM-DD')
    if d and len(d) == 2:
        st.markdown("### Best 5 masters for the period (based on quantity)")
        best_workers = conn.query(f"SELECT masters.id as master_id, masters.name as master_name, COUNT(1) as works_count FROM works LEFT JOIN masters ON works.master_id = masters.id WHERE works.date_work >= '{d[0]}' AND works.date_work <= '{d[1]}' GROUP BY masters.id ORDER BY COUNT(1) DESC LIMIT 5")
        c = alt.Chart(best_workers).encode(x=alt.X('works_count', title='Works performed in period'), y=alt.Y('master_name', title=['Master\'s name']), text='works_count').properties(title=f"Top 5 Masters [{d[0]} - {d[1]}]")
        c = c.mark_bar() + c.mark_text(align='left', dx=2)
        st.altair_chart(c, use_container_width=True)
        st.dataframe(best_workers)
        st.markdown("### Total service cost for foreign and domestic for the period")
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
    WHERE date_work >= '{d[0]}' AND date_work <= '{d[1]}'
GROUP BY
    cars.is_foreign
ORDER BY
    service_cost DESC;
"""  
        total_service_cost = conn.query(total_service_cost_query)
        c = alt.Chart(total_service_cost).mark_arc(outerRadius=80).encode(theta=alt.Theta("service_cost:Q").stack(True), color=alt.Color("is_foreign:N").legend(None))
        text = c.mark_text(radius=125, size=20).encode(text="is_foreign:N")
        text_val = c.mark_text(radius=100, size=20).encode(text="service_cost:Q")
        c = c + text + text_val
        c = c.properties(title=f'Total service per foreignness [{d[0]} - {d[1]}]')
        # c = c.configure_title(fontSize=20, anchor='middle')
        st.altair_chart(c, use_container_width=True)
        st.dataframe(total_service_cost)
    else:
        st.markdown("waiting for date input...")


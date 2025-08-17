import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

DB_PATH = "D:\\local_food_wastage\\food_wastage.db"  # run from project root: streamlit run app/streamlit_app.py

@st.cache_resource
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_conn()

st.set_page_config(page_title="Local Food Wastage System", layout="wide")
st.title("🍲 Local Food Wastage Management System")

menu = st.sidebar.selectbox("Menu", ["Dashboard", "Queries (15)", "Manage Listings", "Manage Claims", "Providers & Receivers"])
st.sidebar.markdown("---")
st.sidebar.write("DB: " + DB_PATH)

if menu == "Dashboard":
    st.header("Live Dashboard")
    col1, col2, col3 = st.columns(3)
    providers_count = pd.read_sql("SELECT COUNT(*) AS c FROM Providers", conn).iloc[0]['c']
    receivers_count = pd.read_sql("SELECT COUNT(*) AS c FROM Receivers", conn).iloc[0]['c']
    total_qty = pd.read_sql("SELECT COALESCE(SUM(Quantity),0) as total FROM Food_Listings", conn).iloc[0]['total']
    col1.metric("Providers", providers_count)
    col2.metric("Receivers", receivers_count)
    col3.metric("Total Food Quantity", int(total_qty))

    df_types = pd.read_sql("SELECT Food_Type, SUM(Quantity) AS qty FROM Food_Listings GROUP BY Food_Type", conn)
    if not df_types.empty:
        fig1 = px.bar(df_types, x='Food_Type', y='qty', title="Total Quantity by Food Type")
        st.plotly_chart(fig1, use_container_width=True)

    df_claim_status = pd.read_sql("SELECT Status, COUNT(*) AS cnt FROM Claims GROUP BY Status", conn)
    if not df_claim_status.empty:
        fig2 = px.pie(df_claim_status, names='Status', values='cnt', title="Claims by Status")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Items near expiry (next 3 days)")
    near_exp = pd.read_sql("SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location FROM Food_Listings WHERE DATE(Expiry_Date) <= DATE('now', '+3 days') ORDER BY Expiry_Date ASC", conn)
    st.dataframe(near_exp)

elif menu == "Queries (15)":
    st.header("SQL Queries & Results")
    # copy the queries from sql/queries.sql
    q1 = "SELECT City, COUNT(*) AS provider_count FROM Providers GROUP BY City ORDER BY provider_count DESC;"
    st.subheader("1) Providers per City"); st.dataframe(pd.read_sql(q1, conn))
    q2 = "SELECT City, COUNT(*) AS receiver_count FROM Receivers GROUP BY City ORDER BY receiver_count DESC;"
    st.subheader("2) Receivers per City"); st.dataframe(pd.read_sql(q2, conn))
    q3 = ("SELECT p.Type AS provider_type, SUM(f.Quantity) AS total_quantity "
          "FROM Food_Listings f JOIN Providers p ON f.Provider_ID = p.Provider_ID "
          "GROUP BY p.Type ORDER BY total_quantity DESC LIMIT 1;")
    st.subheader("3) Top provider type by total quantity"); st.dataframe(pd.read_sql(q3, conn))

    st.subheader("4) Provider contacts by city")
    city_input = st.text_input("Enter city name (for provider contacts):", "")
    if city_input:
        q4 = "SELECT Provider_ID, Name, Contact, Address FROM Providers WHERE City = ?"
        st.dataframe(pd.read_sql(q4, conn, params=(city_input,)))
    else:
        st.info("Type a city above and press Enter to see provider contacts.")

    q5 = ("SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS num_claims "
          "FROM Claims c JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID "
          "GROUP BY r.Receiver_ID, r.Name ORDER BY num_claims DESC LIMIT 10;")
    st.subheader("5) Receivers with most claims"); st.dataframe(pd.read_sql(q5, conn))

    q6 = "SELECT COALESCE(SUM(Quantity),0) AS total_available_quantity FROM Food_Listings;"
    st.subheader("6) Total quantity available"); st.write(pd.read_sql(q6, conn).to_dict(orient='records'))

    q7 = "SELECT Location AS city, COUNT(*) AS listings_count FROM Food_Listings GROUP BY Location ORDER BY listings_count DESC LIMIT 1;"
    st.subheader("7) City with highest listings"); st.dataframe(pd.read_sql(q7, conn))

    q8 = "SELECT Food_Type, COUNT(*) AS count_listings FROM Food_Listings GROUP BY Food_Type ORDER BY count_listings DESC LIMIT 5;"
    st.subheader("8) Top food types"); st.dataframe(pd.read_sql(q8, conn))

    q9 = ("SELECT f.Food_ID, f.Food_Name, COUNT(c.Claim_ID) AS claim_count "
          "FROM Food_Listings f LEFT JOIN Claims c ON f.Food_ID = c.Food_ID "
          "GROUP BY f.Food_ID, f.Food_Name ORDER BY claim_count DESC;")
    st.subheader("9) Claims per food item"); st.dataframe(pd.read_sql(q9, conn))

    q10 = ("SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS completed_claims "
           "FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID "
           "JOIN Providers p ON f.Provider_ID = p.Provider_ID "
           "WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name ORDER BY completed_claims DESC LIMIT 1;")
    st.subheader("10) Top provider by completed claims"); st.dataframe(pd.read_sql(q10, conn))

    q11 = ("SELECT Status, COUNT(*) AS count_status, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Claims), 2) AS pct_of_total FROM Claims GROUP BY Status;")
    st.subheader("11) Claims % by status"); st.dataframe(pd.read_sql(q11, conn))

    q12 = ("SELECT AVG(qty_claimed) AS avg_quantity_per_receiver FROM ( SELECT c.Receiver_ID, SUM(f.Quantity) AS qty_claimed FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID WHERE c.Status = 'Completed' GROUP BY c.Receiver_ID );")
    st.subheader("12) Average quantity claimed per receiver (completed)"); st.dataframe(pd.read_sql(q12, conn))

    q13 = ("SELECT f.Meal_Type, COUNT(c.Claim_ID) AS claim_count FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID GROUP BY f.Meal_Type ORDER BY claim_count DESC;")
    st.subheader("13) Most claimed meal type"); st.dataframe(pd.read_sql(q13, conn))

    q14 = ("SELECT p.Provider_ID, p.Name, SUM(f.Quantity) AS total_donated_quantity FROM Food_Listings f JOIN Providers p ON f.Provider_ID = p.Provider_ID GROUP BY p.Provider_ID, p.Name ORDER BY total_donated_quantity DESC LIMIT 10;")
    st.subheader("14) Top donors by quantity"); st.dataframe(pd.read_sql(q14, conn))

    q15 = "SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Location FROM Food_Listings WHERE DATE(Expiry_Date) <= DATE('now', '+3 days') ORDER BY Expiry_Date ASC;"
    st.subheader("15) Near-expiry items"); st.dataframe(pd.read_sql(q15, conn))

elif menu == "Manage Listings":
    st.header("Manage Food Listings")
    st.subheader("All Listings")
    st.dataframe(pd.read_sql("SELECT * FROM Food_Listings", conn))

    st.subheader("Add Listing")
    with st.form("add_listing", clear_on_submit=True):
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        expiry = st.date_input("Expiry Date", value=datetime.today())
        provider_id = st.number_input("Provider ID", min_value=1, step=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("Location / City")
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks", "Other"])
        submitted = st.form_submit_button("Add Listing")
        if submitted:
            conn.execute("INSERT INTO Food_Listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (food_name, int(quantity), expiry.isoformat(), int(provider_id), provider_type, location, food_type, meal_type))
            conn.commit()
            st.success("Listing added")
            st.experimental_rerun()

    st.subheader("Edit / Delete Listing")
    sel_id = st.number_input("Food_ID to edit/delete", min_value=1, step=1)
    if sel_id:
        rec = pd.read_sql("SELECT * FROM Food_Listings WHERE Food_ID = ?", conn, params=(sel_id,))
        if rec.empty:
            st.warning("No listing found")
        else:
            st.write(rec)
            if st.button("Delete Listing"):
                conn.execute("DELETE FROM Food_Listings WHERE Food_ID = ?", (sel_id,))
                conn.commit()
                st.success("Deleted")
                st.experimental_rerun()
            with st.form("update_listing"):
                new_name = st.text_input("Food Name", value=rec.iloc[0]['Food_Name'])
                new_qty = st.number_input("Quantity", min_value=1, value=int(rec.iloc[0]['Quantity']))
                new_exp = st.date_input("Expiry Date", value=pd.to_datetime(rec.iloc[0]['Expiry_Date']).date() if rec.iloc[0]['Expiry_Date'] else datetime.today().date())
                new_loc = st.text_input("Location", value=rec.iloc[0]['Location'])
                upd = st.form_submit_button("Update")
                if upd:
                    conn.execute("UPDATE Food_Listings SET Food_Name=?, Quantity=?, Expiry_Date=?, Location=? WHERE Food_ID=?", (new_name, int(new_qty), new_exp.isoformat(), new_loc, sel_id))
                    conn.commit()
                    st.success("Updated")
                    st.experimental_rerun()

elif menu == "Manage Claims":
    st.header("Manage Claims")
    st.subheader("All Claims")
    st.dataframe(pd.read_sql("SELECT * FROM Claims", conn))

    st.subheader("Create Claim")
    with st.form("create_claim"):
        food_id = st.number_input("Food ID", min_value=1)
        receiver_id = st.number_input("Receiver ID", min_value=1)
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        ts = st.date_input("Timestamp", value=datetime.today())
        create_btn = st.form_submit_button("Create Claim")
        if create_btn:
            conn.execute("INSERT INTO Claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?)", (int(food_id), int(receiver_id), status, ts.isoformat()))
            conn.commit()
            st.success("Claim created")
            st.experimental_rerun()

    st.subheader("Update Claim Status")
    claim_to_update = st.number_input("Claim ID to update", min_value=1, step=1)
    if claim_to_update:
        record = pd.read_sql("SELECT * FROM Claims WHERE Claim_ID = ?", conn, params=(claim_to_update,))
        if record.empty:
            st.warning("Claim not found")
        else:
            st.write(record)
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
            if st.button("Update Status"):
                conn.execute("UPDATE Claims SET Status = ? WHERE Claim_ID = ?", (new_status, claim_to_update))
                conn.commit()
                st.success("Status updated")
                st.experimental_rerun()

elif menu == "Providers & Receivers":
    st.header("Providers & Receivers")
    left, right = st.columns(2)
    with left:
        st.subheader("Providers")
        st.dataframe(pd.read_sql("SELECT * FROM Providers", conn))
        st.write("Add Provider")
        with st.form("add_provider"):
            pid = st.number_input("Provider ID", min_value=1)
            pname = st.text_input("Name")
            ptype = st.text_input("Type")
            addr = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            if st.form_submit_button("Add Provider"):
                conn.execute("INSERT INTO Providers (Provider_ID, Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?, ?)", (int(pid), pname, ptype, addr, city, contact))
                conn.commit()
                st.success("Provider added")
                st.experimental_rerun()

    with right:
        st.subheader("Receivers")
        st.dataframe(pd.read_sql("SELECT * FROM Receivers", conn))
        st.write("Add Receiver")
        with st.form("add_receiver"):
            rid = st.number_input("Receiver ID", min_value=1, key='ridkey')
            rname = st.text_input("Name", key='rnamekey')
            rtype = st.text_input("Type", key='rtypekey')
            rcity = st.text_input("City", key='rcitykey')
            rcontact = st.text_input("Contact", key='rcontactkey')
            if st.form_submit_button("Add Receiver"):
                conn.execute("INSERT INTO Receivers (Receiver_ID, Name, Type, City, Contact) VALUES (?, ?, ?, ?, ?)", (int(rid), rname, rtype, rcity, rcontact))
                conn.commit()
                st.success("Receiver added")
                st.experimental_rerun()

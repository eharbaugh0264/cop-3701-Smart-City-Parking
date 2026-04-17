import streamlit as st
import oracledb
import pandas as pd

# needed to initalize the client
try:
    oracledb.init_oracle_client(
        lib_dir=r"C:\FloridaPolyCourseContent\OracleInstantClient\instantclient_23_0"
    )
except Exception as e:
    st.error(f"Oracle client init failed: {e}")

#title
st.title("Smart City Parking")

# ask user for database credentials
user = st.text_input("DB Username")
password = st.text_input("DB Password", type="password")
conn = None
cursor = None

# try trys to connect if user enters info
if user and password:
    try:
        conn = oracledb.connect(
            user=user,
            password=password,
            dsn="db.freesql.com:1521/23ai_34ui2"
        )
        cursor = conn.cursor()
        st.success("Connected to database")
    except Exception as e:
        st.error(str(e))

# if invalid credentials
if cursor is None:
    st.warning("Please enter DB credentials to continue")

# runs if connected to database
if cursor is not None:

    # get location for dropdown
    cursor.execute("SELECT DISTINCT Location FROM parking_spot")
    locations = [row[0] for row in cursor.fetchall()]

    # gets data from the database
    cursor.execute("SELECT DISTINCT Make FROM vehicle")
    makes = [row[0] for row in cursor.fetchall()]

    # the feature selection tool
    feature = st.sidebar.selectbox(
        "Select Feature",
        [
            "Parking Demand",
            "Parking History by Spot",
            "Vehicle Usage by Make",
            "Make vs PermitType",
            "Zone Frequency"
        ]
    )
    #feature 1 Parking demand per spot
    if feature == "Parking Demand":
        location = st.selectbox("Select Location", locations)

        if st.button("Run"):
            query = """
            SELECT ps.Location, COUNT(pe.EventID) AS UsageCount
            FROM parking_spot ps
            LEFT JOIN parking_event pe ON ps.SpotID = pe.SpotID
            WHERE ps.Location = :location
            GROUP BY ps.Location
            """
            cursor.execute(query, {"location": location})
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data, columns=["Location", "Usage Count"]))

    #feat 2 shows how long specific cars have been parked in a spot
    elif feature == "Parking History by Spot":
        location = st.selectbox("Select Location", locations)

        if st.button("Run"):
            query = """
            SELECT 
                pe.VehicleID,
                pe.StartTime,
                pe.EndTime,
                ROUND(
                    (TO_DATE(pe.EndTime, 'YYYY-MM-DD HH24:MI') - 
                     TO_DATE(pe.StartTime, 'YYYY-MM-DD HH24:MI')) * 24,
                    2
                ) AS DurationHours
            FROM parking_event pe
            JOIN parking_spot ps ON pe.SpotID = ps.SpotID
            WHERE ps.Location = :location
            ORDER BY pe.StartTime
            """
            cursor.execute(query, {"location": location})
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data, columns=["VehicleID", "Start", "End", "Hours Parked"]))

    #feat 3 shows how many times a Car make was used in any lot
    elif feature == "Vehicle Usage by Make":
        make = st.selectbox("Select Make", makes)

        if st.button("Run"):
            query = """
            SELECT v.Make, COUNT(pe.EventID) AS UsageCount
            FROM vehicle v
            JOIN parking_event pe ON v.VehicleID = pe.VehicleID
            WHERE v.Make = :make
            GROUP BY v.Make
            """
            cursor.execute(query, {"make": make})
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data, columns=["Make", "Usage Count"]))

    #feat 4s shows what type of permit is assoiciated with make type
    elif feature == "Make vs PermitType":
        make = st.selectbox("Select Make", makes)

        if st.button("Run"):
            query = """
            SELECT v.Make, pp.PermitType, COUNT(*) AS Count
            FROM vehicle v
            JOIN parking_permit pp ON v.VehicleID = pp.VehicleID
            WHERE v.Make = :make
            GROUP BY v.Make, pp.PermitType
            """
            cursor.execute(query, {"make": make})
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data, columns=["Make", "Permit Type", "Count"]))

    #feat 5 shows demand for certian parking zones
    elif feature == "Zone Frequency":

        if st.button("Run"):
            query = """
            SELECT 
                COALESCE(
                    REGEXP_SUBSTR(ps.Location, 'Lot [A-Z]'),
                    'Garage'
                ) AS Zone,
                COUNT(pe.EventID) AS UsageCount
            FROM parking_spot ps
            LEFT JOIN parking_event pe ON ps.SpotID = pe.SpotID
            GROUP BY 
                COALESCE(
                    REGEXP_SUBSTR(ps.Location, 'Lot [A-Z]'),
                    'Garage'
                )
            ORDER BY UsageCount DESC
            """
            cursor.execute(query)
            data = cursor.fetchall()
            st.dataframe(pd.DataFrame(data, columns=["Zone", "Usage Count"]))
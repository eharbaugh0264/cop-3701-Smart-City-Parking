import oracledb
import csv

#  ============================================================================================
#  Bulk Load.docx

# --- SETUP ---

#  list of all the CSV files
#  some kind of loop/function that will take each value and bulk load them
CSVFiles = ['vehicle_data.csv', 'parking_permit_data.csv', 'parking_spot_data.csv', 'parking_event_data.csv', 'parking_sensor_data.csv']
CSVStatements = ["vehicle (VehicleID, LicensePlate, Make, Model, Color) VALUES (:1, :2, :3, :4, :5)",
                 "parking_permit (VehicleID, PermitNumber, ExpirationDate, PermitType) VALUES (:1, :2, :3, :4)",
                 "parking_spot (SpotId, Location) VALUES (:1, :2)",
                 "parking_event (EventID, VehicleID, SpotID, StartTime, EndTime) VALUES (:1, :2, :3, :4, :5)",
                 "sensor (SensorID, SpotID, Status) VALUES (:1, :2, :3)"]

#  The initial create file
CreateFile = 'create_db.sql'

LIB_DIR = r"C:\FloridaPolyCourseContent\OracleInstantClient\instantclient_23_0"

DB_USER = "EHARBAUGH0264_SCHEMA_8X46H" # or your FreeSQL username
DB_PASS = "XA873DVPCPPAM61V2HQPON6!8U4On6" # your password for the dbms user

DB_DSN  = "db.freesql.com" + ":" + "1521" + "/" + "23ai_34ui2"

# Initialize Thick Mode (Required for FreeSQL/Cloud)
oracledb.init_oracle_client(lib_dir=LIB_DIR)


def bulk_load_csv(file_path, insert_statement):
    try:
        # 1. Connect
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        # 2. Read CSV Data into a List
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            data_to_insert = [row for row in reader]

        # 3. Prepare Bulk Insert SQL
        # :1 and :2 correspond to the values in each row of your list
        sql = "INSERT INTO " + insert_statement
        # (name, email) VALUES (:1, :2)"

        # 4. Execute Batch
        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)

        # 5. Commit Changes
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")
    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback()  # Undo changes if an error occurs

    #finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

for path, statement in zip(CSVFiles, CSVStatements):
    print("============", path, "============")
    bulk_load_csv(path, statement)

print("Oracle connection closed.")

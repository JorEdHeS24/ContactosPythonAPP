import mysql.connector

# GET DATA FORM DB

def get_db():
    config = {
        "host": "brt7dgh8sbljdrj8cnbu-mysql.services.clever-cloud.com",
        "port": "3306",
        "database": "brt7dgh8sbljdrj8cnbu",
        "user": "uv34ruwywshxfcee",
        "password": "uI0feGimZGjhV23FuFVD"
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT * FROM users"
    print(query)
    cursor.execute(query)
    contacts = cursor.fetchall()
    # print(contacts)
    return contacts
    # for row in contacts:
    #     print(row)
        
    cursor.close()
    connection.close()


    
# UPDATE DATA TO DB




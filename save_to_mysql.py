import mysql.connector


def init_db():
    """
    Loads environment variables from .env file and
    initialises Database with mysql.connector
    :return:
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()

    return mysql.connector.connect(
        host=os.environ.get("DATABASE_HOST"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        database=os.environ.get("DATABASE_ID")
    )


def get_cursor():
    """
    Get cursor if one doesn't already exist
    :return:
    """
    global db
    try:
        db.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        # reconnect
        db = init_db()
    return db.cursor()


def save(result: list):
    """
    Write final info to mysql database
    :param result:
    :return:
    """
    final_list = []
    for item in result:
        new_tuple = (result.index(item), item["link"], item["forum"], item["forum_id"], " " +
                     item["title"]+" ", item["user"], item["date"], item["official"], item["voting"])
        final_list.append(new_tuple)
    # temp_counter = 0
    # for item in final_list:
    #     if item[3] == "51":
    #         temp_counter += 1
    # print(temp_counter)
    sql = "REPLACE INTO dojo_links (id, link, forum, forum_id, title, user, date, official, voting) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor = get_cursor()
    # cursor.execute("DROP TABLE dojo_links")
    # cursor.execute("CREATE TABLE dojo_links (id INT, link VARCHAR(255) PRIMARY KEY, forum VARCHAR(255), forum_id INT, title VARCHAR(255), user VARCHAR(255), date DATETIME, official INT(1), voting INT(1))")
    print("Database connected")
    cursor.executemany(sql, final_list)
    db.commit()
    print("Saved result to mysql database")


db = init_db()

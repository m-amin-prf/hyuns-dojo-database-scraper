def save(result: list):
    """
    Write final info to a sqlite db
    :param result:
    :return:
    """
    import sqlite3
    con = sqlite3.connect("duel_links.db", check_same_thread=False)
    cursor = con.cursor()

    # Create a temp table
    # If something goes wrong or the process is aborted, the previously scraped data won't be lost.
    #
    # Updating existing entries directly isn't feasible because the IDs are the index within the list,
    # which are subject to change with each scrape. An improvement might be to use the url as the id,
    # which *should* be 1:1 with that specific post.
    cursor.executescript(
        "DROP TABLE IF EXISTS dojo_links_temp;\n"
        "CREATE TABLE dojo_links_temp (\n"
        "  id         INTEGER,\n"
        "  link       TEXT,\n"
        "  forum      TEXT,\n"
        "  forum_id   INTEGER,\n"
        "  title      TEXT,\n"
        "  user       TEXT,\n"
        "  date       TEXT,\n"   # sqlite doesn't have a dedicated date type.
        "  official   INTEGER,\n"
        "  voting     INTEGER);"
    )
    con.commit()

    # Process data for inserting
    final_list = []
    for item in result:
        new_tuple = (result.index(item), item["link"], item["forum"], item["forum_id"], " " +
                     item["title"]+" ", item["user"], item["date"], item["official"], item["voting"])
        final_list.append(new_tuple)

    # Insert the result into the temp table
    sql = ("INSERT INTO dojo_links_temp (id, link, forum, forum_id, title, user, date, official, voting)"
           "  VALUES (?,?,?,?,?,?,?,?,?);")
    cursor.executemany(sql, final_list)
    con.commit()

    # Overwrite the previous links table with the temp table.
    cursor.executescript(
        "DROP TABLE IF EXISTS dojo_links;\n"
        "ALTER TABLE dojo_links_temp RENAME TO dojo_links;"
    )
    con.commit()
    con.close()
    print("Saved result to sqlite db")

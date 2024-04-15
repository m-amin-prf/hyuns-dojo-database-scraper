def save(result: list):
    """
    Write final info to json file
    :param result:
    :return:
    """
    import json
    with open("duels_links.json", "w") as fout:
        json.dump(result, fout)
    print("Saved result to json file")

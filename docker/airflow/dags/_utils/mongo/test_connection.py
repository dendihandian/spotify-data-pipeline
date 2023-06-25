from _utils.mongo.client import mongo

def get_test_database():

    try:
        test_database   = mongo["test_database"]
        test_collection = test_database["test_collection"]
        new_id          = test_collection.insert_one({'key': 'value'}).inserted_id
        print('new_id:', new_id)
    except:
        return False

    return True

if __name__ == '__main__':
    print(get_test_database())

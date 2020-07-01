import time
import argparse

from pymongo import MongoClient

from utils import str2bool, get_sample, print_args, check_connection, get_samples_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments on samples generation')
    parser.add_argument('--nsamples', type=int, default=5000,
                        help='quantity of samples to generate')
    parser.add_argument('--multiple', type=str2bool, default=True,
                        help='bool: True - "insert_many", False - sequential "insert_one"')
    parser.add_argument('--erase', type=str2bool, default=True,
                        help='bool: erase data from db before insertion')
    args = parser.parse_args()

    print_args(__file__, args)

    client = MongoClient(port=27017)
    check_connection(client)

    db = client.business
    database_list = client.list_database_names()
    print("database_list:", database_list)
    print("number of dbs:", len(database_list))
    print("collections in the db:", db.list_collection_names())

    cnt = get_samples_count(db, 'reviews')
    if cnt and args.erase:
        db.reviews.drop()
        print('Database "business" was erased!')
        get_samples_count(db, 'reviews')

    t1 = time.time()
    insertion_list = []
    for _ in range(args.nsamples):
        insertion_list.append(get_sample())

    if args.multiple:
        result = db.reviews.insert_many(insertion_list)
    else:
        for sample in insertion_list:
            result = db.reviews.insert_one(sample)

    insertion_time = time.time() - t1
    print("Insertion took total time of: {}s.".format(round(insertion_time, 4)))

    print(f'Finished creating {args.nsamples} business reviews.')

    get_samples_count(db, 'reviews')
    client.close()

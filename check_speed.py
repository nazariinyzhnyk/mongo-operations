import time
import argparse

from pymongo import MongoClient

from utils import get_sample, print_args


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Speed testing arguments')
    parser.add_argument('--nsamples', type=int, default=5000,
                        help='quantity of samples to generate')

    args = parser.parse_args()
    print_args(__file__, args)

    client = MongoClient(port=27017)
    client.drop_database('business')

    db = client.business
    t1 = time.time()
    for _ in range(args.nsamples):
        result = db.reviews.insert_one(get_sample())
    seq_time = time.time() - t1
    print("Sequential insert time elapsed: {}s.".format(round(seq_time, 4)))

    t1 = time.time()
    insertion_list = []
    for _ in range(args.nsamples):
        insertion_list.append(get_sample())
    result = db.reviews.insert_many(insertion_list)
    mult_time = time.time() - t1
    print("Multiple insert time elapsed  : {}s.".format(round(mult_time, 4)))
    print("Sequential / multiple ratio   : {} times".format(round(seq_time / mult_time, 4)))

    client.close()

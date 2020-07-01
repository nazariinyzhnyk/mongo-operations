import os
from random import randint
import argparse

import pymongo

names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City', 'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich',
         'Lazy', 'Fun']
company_type = ['LLC', 'Inc', 'Company', 'Corporation']
company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']


def get_sample():
    return {'name': names[randint(0, (len(names) - 1))] + ' ' + names[randint(0, (len(names) - 1))] + ' ' +
                    company_type[randint(0, (len(company_type) - 1))],
            'rating': randint(1, 5),
            'cuisine': company_cuisine[randint(0, (len(company_cuisine) - 1))]}


def str2bool(v):
    """

    :param v: value provided by user in command line
    :return: bool
    >>> str2bool('True')
    True
    >>> str2bool('False')
    False
    >>> str2bool('1')
    True
    >>> str2bool('0')
    False
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def print_args(filename, args, fmt='\t - {:8}: {}'):
    print(f'\nRunning {os.path.basename(filename)} with arguments: ')
    for key, value in args.__dict__.items():
        print(fmt.format(key, value))
    print()


def check_connection(client):
    try:
        print(client.server_info())
        print("Connection established successfully!")
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Please check your connection! \n brew services start mongodb-community@4.2")
        print("ERR: " + err)


def get_samples_count(db, collection):
    cursor = db[collection].find({})
    cnt = cursor.count()
    print("# of samples in reviews collection: " + str(cnt))
    return cnt


if __name__ == '__main__':
    import doctest
    doctest.testmod()

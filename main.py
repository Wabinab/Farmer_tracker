"""
Main file where thing goes.
Created on 18 February 2022.
"""
import time

from all import *
import argparse
import logging
import pickle
import json
import yaml
from pyhelpers.store import save_pickle, load_pickle

logging.basicConfig(filename="output/logs.txt", level=logging.INFO)


def pipeline_fetch_data_into_set(account_name):
    name, account = fetch_website_links(account_name)
    account = preprocess_fetch_all_names(account)

    if len(account) == 0:  # try again just in case website haven't finish loading.
        print("Goes into refresh")
        time.sleep(5)
        name, account = fetch_website_links(account_name, read_again=True)
        account = preprocess_fetch_all_names(account)

    if len(account) == 0:  # if still zero, fails.
        printout = f"Cannot find any transfer. Manual checking required: {account_name}"
        print(printout)
        logging.info(printout)
    return name, account


def total_pipeline(list_of_account_names: (list, set)):
    """
    Pass in the list of account names as a list or set, go through them.

    Some current farmers, we'll assume they're parents to some of the whitelisted, and check for more
    interactions. Reason we find farmer first because normal non-farmers are allowed to interact with
    non-farmers as well, so this might be less accurate. This way, we can give a higher confidence to
    the output from this pipeline.

    HOWEVER WE STILL CAN'T DENY THAT THEY MAY NOT ALL BE FARMERS.

    :param list_of_account_names:
    :return: Potential farmers with their ratings. Ratings are counts of occurrences.
    """
    corresponding_names = []
    list_of_acc_output = []

    for name in list_of_account_names:
        _name, acc = pipeline_fetch_data_into_set(name)
        corresponding_names.append(_name)
        list_of_acc_output.append(acc)

    more_occurrences, total = postprocess_counting_total_occurrences_larger_than_once(list_of_acc_output)

    # save more_occurrences
    with open('output/total_count.pkl', 'wb') as f:
        pickle.dump(total, f)

    farmers, whitelisted, perhaps_farmers = finding_farmers(
        corresponding_names, list_of_acc_output, more_occurrences, total)

    curr_farmers = set(farmers.keys())
    potential_farmers = dict()

    dict_name_to_transaction = {k: v for k, v in zip(corresponding_names, list_of_acc_output)}

    save_pickle(dict_name_to_transaction, 'output/transaction_list.pkl')

    for whitelisted_acc in whitelisted.copy():
        compare_to = dict_name_to_transaction.get(whitelisted_acc)
        is_farmer = curr_farmers.intersection(compare_to)

        if len(is_farmer) >= 1:
            potential_farmers[whitelisted_acc] = list(is_farmer)  # not length here.
            whitelisted.remove(whitelisted_acc)

    return farmers, whitelisted, potential_farmers, perhaps_farmers




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('account_file', type=str, help='where all account name located, txt file',
                        default='all_accounts.txt')

    args = parser.parse_args()

    with open(args.account_file, 'r') as f:
        list_of_account_names = f.readlines()

    # new fix, not tested yet.
    list_of_account_names = [name.strip() for name in list_of_account_names]

    farmers, whitelisted, potential_farmers, perhaps_farmers = total_pipeline(list_of_account_names)

    # save to yaml file farmers
    with open('output/current_blacklisted.yaml', "w") as f:
        yaml.dump(farmers, f)

    with open('output/potential_farmers.json', 'w') as f:
        json.dump(potential_farmers, f, indent=4)

    with open('output/perhaps_farmers.yaml', "w") as f:
        yaml.dump(perhaps_farmers, f)

    # whitelisted
    whitelisted = [f"{name}\n" for name in whitelisted]  # add \n to all.
    with open('output/current_whitelisted.txt', 'w') as f:
        f.writelines(whitelisted)


# input("Press anything to exit...")
close_driver_at_end()

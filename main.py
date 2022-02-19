"""
Main file where thing goes.
Created on 18 February 2022.
"""
import time

from all import *
import yaml


def pipeline_fetch_data_into_set(account_name):
    name, account = fetch_website_links(account_name)
    account = preprocess_fetch_all_names(account)

    if len(account) == 0:  # try again just in case website haven't finish loading.
        time.sleep(3)
        name, account = fetch_website_links(account_name, read_again=True)
        account = preprocess_fetch_all_names(account)

    if len(account) == 0:  # if still zero, fails.
        print("Cannot find any transfer. Manual checking required")
    return name, account


def total_pipeline(list_of_account_names: (list, set)):
    """
    Pass in the list of account names as a list or set, go through them.

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

    return finding_farmers(corresponding_names, list_of_acc_output, more_occurrences, total)


if __name__ == '__main__':
    list_of_account_names = "read from text file"
    total_pipeline(list_of_account_names)

    # save to yaml file farmers




input("Press anything to exit...")
close_driver_at_end()

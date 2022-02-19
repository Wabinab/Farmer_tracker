"""
To preprocess or postprocess data.
Created on: 18 February 2022.
"""

import re
from collections import Counter


def preprocess_fetch_all_transactions(TwoD_list):
    """
    Take output from fetch_website_links and pass here to be preprocessed, for all transaction links.
    :param TwoD_list:
    :return:
    """
    flattened = [item for sublist in TwoD_list for item in sublist]
    r = re.compile('https://explorer.mainnet.near.org/transactions/')
    newlist = list(filter(r.match, flattened))

    return newlist


def preprocess_fetch_all_names(TwoD_list):
    """
    Take output from fetch_website_links and pass here to be preprocessed, for all names.
    This assumes that with names, it means transaction happens.
    Automatically removes those that one thought are popular. Note that this DOES NOT REMOVE
    EVERYTHING THAT ARE POPULAR.
    :param TwoD_list:
    :return:
    """

    flattened = [item for sublist in TwoD_list for item in sublist]
    r = re.compile('^[@]')
    newlist = list(filter(r.match, flattened))

    newlist = [_[1:] for _ in newlist]  # remove @ from value.

    # Currently leave here, but for scaling, it requires to move into another file for storage.
    popular_list = {
        'ref-finance.near',
        'wrap.near',
        'learn.near'
    }

    # Remove those in popular_list
    newlist = set(filter(lambda i: i not in popular_list, newlist))

    # Remove subaccounts as they're most probably contract holders.
    newlist = set(filter(lambda i: len(i.split('.')) <= 2, newlist))

    # Remove those containing poolv1.near. This might change into poolv2.near in the future?
    # Hence we counter for that as well.
    # r = re.compile('^(?!.*(.poolv))')
    # newlist = set(filter(r.match, newlist))

    return newlist



def postprocess_transaction_actions(action_text: str):
    """
    Given action text from NEAR explorer, return the transaction amount.

    :param action_text:  Action text from near explorer.
    :return: transaction amount
    """
    assert len(action_text) != 0
    assert re.search('Actions', action_text), "word 'Actions' not in action_text, perhaps not Action?"

    # For transfer not using functions, required word "Transferred"
    output = re.search("Transferred", action_text)

    if output is not None:
        start = output.span()[1]

        # Search for next floating point value
        return float(re.search(r'\d+\.\d+', action_text[start:]).group())

    else: return None


def postprocess_counting_total_occurrences_larger_than_once(list_of_acc_output):
    """
    Given the list of output from all the accounts, make a Counter for multi occurrences counting.
    :param list_of_acc_output:
    :return: Counter object.
    """
    total = Counter()

    for curr_sets in list_of_acc_output:
        total += Counter(curr_sets)

    more_occurrences = {k for k, v in total.items() if v > 1}

    return more_occurrences, total


def finding_farmers(corresponding_names, list_of_acc_output, more_occurrences, total):
    """
    Take output of list_of_acc_output, and the output from
    postprocess_counting_total_occurrences_larger_than_once
    and find farmers.

    :return: Farmers with their corresponding rating score.
    """

    potential_farmers = dict()
    whitelist = set()

    # Check if account appear in more_occurrences.
    for name, acc in zip(corresponding_names, list_of_acc_output):
        farmers = more_occurrences.intersection(acc)

        if len(farmers) == 0:
            whitelist.add(name)
        else:
            potential_farmers[name] = len(farmers)

    return potential_farmers, whitelist

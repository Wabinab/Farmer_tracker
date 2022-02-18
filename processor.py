"""
To preprocess or postprocess data.
Created on: 18 February 2022.
"""

import re


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


def preprocess_fetch_all_names(TwoD_list):  #TODO: Test this function.
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
        'wrap.near'
    }

    # Remove those in popular_list
    newlist = list(filter(lambda i: i not in popular_list, newlist))

    # Remove those containing poolv1.near. This might change into poolv2.near in the future?
    # Hence we counter for that as well.
    r = re.compile('^(?!.*(.poolv))')
    newlist = list(filter(r.match, newlist))

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
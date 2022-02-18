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
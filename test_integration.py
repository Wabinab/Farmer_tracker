"""
Integration tests on sub-parts
Created on: 19 February 2022
"""

import pytest
from all import *

def pipeline_fetch_data(acc_name):
    name1, acc1 = fetch_website_links(acc_name)
    acc1 = preprocess_fetch_all_names(acc1)

    return name1, acc1


def test_finding_farmers_work():
    input_names = ['wabinab.near', 'elon_musk_is.near', 'elon_musk_loves.near']
    corresponding_names = []
    list_of_acc_output = []

    for name in input_names:
        _name, acc = pipeline_fetch_data(name)
        corresponding_names.append(_name)
        list_of_acc_output.append(acc)

    more_occurrences, total = postprocess_counting_total_occurrences_larger_than_once(list_of_acc_output)

    farmers, whitelist = finding_farmers(corresponding_names, list_of_acc_output, more_occurrences, total)

    # expected = {
    #     'elon_musk_is.near': 2,
    #     'elon_musk_loves.near': 2,
    # }

    assert 'elon_musk_is.near' in farmers
    assert 'elon_musk_loves.near' in farmers
    assert 'wabinab.near' not in farmers

    assert 'wabinab.near' in whitelist
    assert 'elon_musk_loves.near' not in whitelist
    assert 'elon_musk_is.near' not in whitelist


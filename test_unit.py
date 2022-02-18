"""
Unit tests.

NOTE:
    If tests fails with `AttributeError: 'NoneType' object has no attribute 'span'`,
    MOST PROBABLY the website is not reachable at the moment. Try again.
"""
import re

from fetch import *
from processor import *
import pytest

links = fetch_website_links('wabinab.near')
fake_links = fetch_website_links('not_even_true')  # don't even have .near


def test_fetch_works_with_expected_data():
    flattened = [item for sublist in links for item in sublist]
    assert 'EXoAkSBTEntbFgQGx625BgnsfRGgeoMA4iPZbMTEdT4t' in flattened, "webpage not fully loaded"  # random hash.


def test_all_contains_word_transaction_in_output():
    output = preprocess_fetch_all_transactions(links)

    assert len(output) > 0, "no transaction when it should have"
    for i in output: assert re.search('transaction', i)


def test_no_transaction_output_with_fake_account():
    output = preprocess_fetch_all_transactions(fake_links)

    assert len(output) == 0, "transaction found when no transaction is expected. Check fake link. "


def test_fetch_explorer_contains_action():
    link = 'https://explorer.mainnet.near.org/transactions/GYPqg5necteQupaJ3kP1WjkwbGfgM4M6X1vik9LWiVeG'

    assert re.search('Actions', fetch_explorer_actions(link))


def test_preprocess_fetch_all_names_with_dummy_as_expected():
    transactions = [
        ['@aurora.poolv1.near', 'withdraw'],
        ['@aurora.poolv1.near', 'stake'],
        ['@another_account.near', 'another account'],
        ['EXoAkSBTEntbFgQGx625BgnsfRGgeoMA4iPZbMTEdT4t', 'some random transaction http link here'],
        ['@ref-finance.near', 'swap'],
        ['@wrap.near', 'unwrap'],
        ['@11244002550bdff129591faabb10e811d910d3f57e0abdc50a5e7dd46b3938ba', 'from Binance'],
        ['@ethan_is_cool.near', 'initial transfer']
    ]

    expected = ['another_account.near',
                '11244002550bdff129591faabb10e811d910d3f57e0abdc50a5e7dd46b3938ba',
                'ethan_is_cool.near']

    assert preprocess_fetch_all_names(transactions) == expected


def test_fetch_explorer_money_is_correct():
    link = 'https://explorer.mainnet.near.org/transactions/GYPqg5necteQupaJ3kP1WjkwbGfgM4M6X1vik9LWiVeG'

    action_output = fetch_explorer_actions(link)

    assert postprocess_transaction_actions(action_output) == 11.003


def test_fetch_explorer_with_functions_cannot_read_is_expected():
    link = 'https://explorer.mainnet.near.org/transactions/2CQ4PnaWHUuBY2CUT1cyomoBvCZ6ojA5AS13iAztHAD4'

    action_output = fetch_explorer_actions(link)

    assert postprocess_transaction_actions(action_output) == None


@pytest.fixture(scope='session')
def close_browser_teardown():
    close_driver_at_end()

def test_dummy_final_to_teardown(close_browser_teardown): pass
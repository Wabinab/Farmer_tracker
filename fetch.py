"""
The fetch functions. Only fetch data, no preprocessing.
Created on 18 February 2022.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import re
import requests
import time

from requests import ConnectionError

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)


def fetch_website_links(account_name="1999.near", read_again=False):
    if not read_again:
        driver.get(f"https://stats.gallery/mainnet/{account_name}/transactions?t=all")

    # When one try to beautify the script, some functionality changes. Make sure you test the
    # functionality with pytest or manual testing that it doesn't change if you plan to beautify
    # the script below.
    script = """
var x = document.querySelectorAll("a");
var myarray = []
for (var i=0; i<x.length; i++){
var nametext = x[i].textContent;
var cleantext = nametext.replace(/\s+/g, ' ').trim();
var cleanlink = x[i].href;
myarray.push([cleantext,cleanlink]);
};
function make_table() {
    var table = '<table><thead><th>Name</th><th>Links</th></thead><tbody>';
   for (var i=0; i<myarray.length; i++) {
            table += '<tr><td>'+ myarray[i][0] + '</td><td>'+myarray[i][1]+'</td></tr>';
    };
 
    
return myarray
}
return make_table()
"""

    time.sleep(3)  #TODO: might need to change how this works?

    return account_name, driver.execute_script(script)


def fetch_explorer_actions(link):
    """
    Given a website, fetch the Action tab information from the NEAR explorer link.

    :param link:
    :return:
    """
    assert re.search('https://explorer.mainnet.near.org', link), """
    Not a valid link: must be explorer.mainnet.near.org type, also testnet and betanet not
    supported"""

    href = requests.get(link)

    if not href.ok: raise ConnectionError("Unable to reach the website. Please try again later.")

    start = re.search('Actions', href.text).span()[0]
    end = re.search('Transaction Execution Plan', href.text).span()[0]

    return href.text[start:end]


def close_driver_at_end():
    driver.close()

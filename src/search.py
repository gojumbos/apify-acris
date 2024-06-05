from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

import local_utils
from local_utils import datetime



def get_doc_id_from_string(db: str):
    """ from individual DET button, get the doc id num"""
    assert type(db) == str
    start = db.find('go_detail') + len('go_detail') + 2
    stop = db[start:].find("\"")
    r = db[start:start+stop]
    assert len(r) == 16
    return r


def get_parcel_info(parcel_table: pd.DataFrame):
    """
    get parcel info from details page
    """
    assert type(parcel_table) == pd.DataFrame
    addr = parcel_table[8][0].__repr__()
    boro = parcel_table[0][0].__repr__()

    sa = addr.find('\n')
    addr = addr[:sa].strip()

    sb = boro.find('\n')
    boro = boro[:sb].strip()
    # boro = boro.replace("/", "")
    """ strip """
    li = ["/", "\'"]
    addr = remove_all(addr, li)  # remove li from addr
    boro = remove_all(boro, li)

    return addr, boro


def get_parties_from_doc(party_table: pd.DataFrame):
    """
    1/14
    type of nan is float, filter this
    use on party 1, then party 2 table
    """
    parties_li = [x for x in party_table if type(x) != float]

    return parties_li


def get_info_detailed_document_html(html: str):
    """
    given html file of document detail page,
    get all address,
    """
    # html FILE -> dataframe
    df_list = pd.read_html(html)
    """ Get parties as lists """
    party1_table, party2_table = df_list[12][0], df_list[15][0]
    parties_1_li, parties_2_li = get_parties_from_doc(party1_table), get_parties_from_doc(party2_table)
    parcel_table = df_list[22]
    addr, boro = get_parcel_info(parcel_table)
    """ Get amount, boro """
    amount_str = df_list[7][1][4]
    return addr, boro, amount_str, parties_1_li, parties_2_li


def remove_all(s: str, li: List):
    """ remove all chars passed to this function from s"""
    assert type(s) == str
    assert type(li) == list

    for c in li:
        s = s.replace(c, "")
    return s

def get_doc_ids_search_page(soup: BeautifulSoup):
    raw_det_buttons = soup.find_all("input", {'name': "DET"})
    det_buttons = [x.__repr__() for x in raw_det_buttons]
    doc_ids = [get_doc_id_from_string(x) for x in det_buttons]
    doc_id_0 = get_doc_id_from_string(det_buttons[0])
    return doc_ids


def result_has_go_next(soup: BeautifulSoup):
    """
    if search results page
    has go_next() embedded, there are
    remaining pages of results
    """
    b = soup.find_all("a", {'href': 'JavaScript:go_next()'})
    return len(b) == 1



import pickle
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import select

import constants
from constants import SLEEP, strip_zero
from time import sleep
import sys

from pyvirtualdisplay import Display

import search

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from apify import Actor

import constants



class Browser:
    def __init__(self, search_type="DEED",
                 date=("02", "28", "2024"),
                 sub_type_search="DEED",
                 url=None,
                 show_head=False,
                 small_test=False,
                 run_local=False,
                 actor_input=None,
                 actor=None):

        if actor:
            self.Actor = actor

        url_doc_type = constants.URL_SEARCH_HOME
        self.small_test = small_test
        self.actor_input = actor_input

        # if run_local:
        #     path = '~/chromedriver_macosx/chromedriver.exe'
        # else:
        #     display = Display(visible=False, size=(800, 800))
        #     display.start()
        #     path = '/usr/bin/chromedriver '
        #     print("Run cloud, pyvd")
        #     chrome_options = webdriver.ChromeOptions()
        #     chrome_options.add_argument("--headless")
        #     chrome_options.add_argument("--disable-gpu")
        #     # chrome_options.add_argument("window-size=1024,768")
        #     chrome_options.add_argument("--no-sandbox")

        Actor.log.info('Launching Chrome WebDriver...')  # new - from Apify
        chrome_options = ChromeOptions()
        # if Actor.config.headless:  # drb
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # # DRB 6/6
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--proxy-server='direct://'")
        # chrome_options.add_argument("--proxy-bypass-list=*")
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        # DRB 6/5:
        self.driver = webdriver.Chrome(options=chrome_options)

        Actor.log.info('line 79 driver run headless')

        # sys.path.append(path) # path not needed??
        # op = webdriver.ChromeOptions()
        # if not show_head:
        #     print("run headless w/ pyvd")
        #     # op.add_argument('headless')
        # self.driver = webdriver.Chrome(options=op)

        if url:
            url_doc_type = url
        # self.driver.get(url_doc_type)

        self.date = date

        """ CONSTANTS: """
        self.search_type = search_type  # doc type
        self.sub_types = []
        self.DROPDOWN_1 = ""  # replace

        if search_type == "DEED":
            self.DROPDOWN_1 = 1
            self.sub_types = ["DEED"]

        elif search_type == "OTHER":
            self.DROPDOWN_1 = 3
            self.sub_types = ["NYC REAL PROPERTY TRANSFER TAX",
                              "NYS REAL ESTATE TRANSFER TAX",
                              "BOTH RPTT AND RETT"]

        elif search_type == "LOAN":
            self.DROPDOWN_1 = 2
            self.sub_types = ["ASSIGNMENT OF LEASES AND RENTS",
                              "MORTGAGE",
                              "AGREEMENT",
                              "ASSIGNMENT, MORTGAGE"]
        else:
            exit("Invalid doc type")

        self.curr_sub_type = self.sub_types[0]  # init to 0, modified externally

    def update_sub_type(self, new_sub_type=None):
        assert new_sub_type is not None
        self.curr_sub_type = new_sub_type


def get_element(driver: webdriver.Chrome, elt_name):
    """ given driver, get specific elt on page BY NAME """
    try:

        sleep(5)
        elt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, elt_name)))
        # elt = driver.find_element(By.NAME, elt_name)
        return elt
    except NoSuchElementException:
        print("no such element ", elt_name)


def get_and_click_dropdown_index(driver: webdriver.Chrome, elt_name: str, index: int):
    """ click drop down element by index """
    try:
        elt = get_element(driver, elt_name)
        sel = select.Select(elt)
        sel.select_by_index(index=index)
    except NoSuchElementException as err:
        print("no such option,", index, err)
    except AttributeError as err:
        print("no attr", err)


def get_and_click_dropdown_value(driver: webdriver.Chrome, elt_name: str, selection: str):
    elt = get_element(driver, elt_name)


    sel = select.Select(elt)
    try:
        sel.select_by_visible_text(text=selection)
    except NoSuchElementException:
        print("no such option,", selection)


def get_and_input_date(driver: webdriver.Chrome, elt_name: str, num_string: str):
    """ input text, do not enter """
    elt = get_element(driver, elt_name)
    elt.send_keys(num_string)
    # elt.send_keys(Keys.RETURN)


def get_and_push_button(driver: webdriver.Chrome, elt_name: str):

    elt = get_element(driver, elt_name)
    elt.click()
    print("clicked ", elt_name)



def enter_date_total(driver: webdriver, date: tuple):
    """ enter date, as [02, 02, 2024] """

    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_fromm", num_string=date[0])
    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_fromd", num_string=date[1])
    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_fromy", num_string=date[2])

    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_tom", num_string=date[0])
    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_tod", num_string=date[1])
    sleep(SLEEP)
    get_and_input_date(driver=driver, elt_name="edt_toy", num_string=date[2])
    return


def get_all_doc_ids_search_res(soup: BeautifulSoup):
    """ use search.py functionality to get all doc ids """
    try:
        s = search.get_doc_ids_search_page(soup=soup)
        return s
    except IndexError as err:
        print("No doc ids found", err)


def visit_doc_page(driver, doc_id):
    try:
        print("DI: ", doc_id)
        # s = f'\"JavaScript:go_detail(\'{doc_id}\')\"'
        # \'JavaScript:go_detail(\"{js_name}\")\'
        driver = get_element_and_onclick_js(driver=driver, js_name=doc_id)

    except IndexError as err:
        print("No doc ids found", err)
    return driver


def get_element_and_onclick_js(driver: webdriver.Chrome, js_name: str):
    """
    get specific javascript button onclick, exact match
    """
    try:
        o = f'input[onclick*=\'{js_name}\'][name=\'DET\']'
        elt = driver.find_element(By.CSS_SELECTOR, o)
        elt.click()
    except NoSuchElementException:
        print("No such element ", js_name)
    return driver


def revert_to_search_res(driver: webdriver):
    try:
        # get_element_js(driver=driver, js_name='javascript:go_result(\'DocumentTypeResult\')')
        # get_and_push_button(driver=driver, elt_name="Submit2")
        # driver.get(url_doc_type)
        driver.back()  # back button
    except NoSuchElementException as e:
        print(e)
    return driver


def enter_search_info(browser: Browser, driver: webdriver, Actor):
    terms = [browser.DROPDOWN_1, browser.curr_sub_type, 2]  # controlled in main.py
    Actor.log.info('url:' + str(driver.current_url))
    sleep(1)
    get_and_click_dropdown_index(driver=driver, elt_name="combox_doc_narrow",
                                 index=terms[0])
    Actor.log('found dropdown 1, line 242')
    sleep(1)
    get_and_click_dropdown_value(driver=driver, elt_name="combox_doc_doctype",
                                 selection=terms[1])
    Actor.log('found dropdown 2')
    sleep(1)
    get_and_click_dropdown_index(driver=driver, elt_name="cmb_date",
                                 index=terms[2])
    Actor.log('found dropdown 3')
    """ DATE """
    enter_date_total(driver=driver, date=browser.date)
    Actor.log('entered date')
    """ SUBMIT """
    sleep(2)
    get_and_push_button(driver=driver, elt_name="Submit2")
    Actor.log('submitted ')


def update_soup(driver: webdriver):
    """ get new soup from driver """
    return BeautifulSoup(driver.page_source, "html.parser")


def go_next_page_search_res(driver: webdriver):
    button = driver.find_element(By.CSS_SELECTOR, 'a[href*=go_next]')
    button.click()
    print("Go next page ")
    return driver


def run_search(browser: Browser,
               driver: webdriver,
               search_data_dict=None,
               search_item_ctr=None,
               ignore_zero_amt=True,
               actor=None
               ):
    """
    >> given browser, driver, retrieve and append scrape results
    to search data list
    >> search_data as dict
    """
    # data_dict: doc id -> [a, b, amt, p1_li, p2_li]
    #

    driver.get(constants.URL_SEARCH_HOME)  # guarantee return home zzz

    enter_search_info(browser=browser, driver=driver, Actor=actor)
    #
    sleep(2)
    search_res_page_ctr = 0
    print("search page ", search_res_page_ctr)
    search_res_soup = update_soup(driver=driver)

    """ INCR MAX ROWS """

    # get_and_click_dropdown_index(driver=driver, elt_name="com_maxrows", index=3)
    # doc_id_list = get_all_doc_ids_search_res(soup=search_res_soup)

    """ NAVIGATE DOCUMENTS """
    curr_page_num = 1
    curr_has_next = search.result_has_go_next(soup=search_res_soup)
    # all_data = []
    search_res_url = driver.current_url

    if "No Records Found" in driver.page_source:
        print("No Records for search")
        # return to search page
        return search_data_dict

    while curr_has_next:
        curr_page_num += 1
        """ UPDATE CURR PAGE """
        sleep(.3)
        search_res_soup = update_soup(driver=driver)
        """ GET ALL DOC DATA """
        doc_id_list = get_all_doc_ids_search_res(soup=search_res_soup)

        """ list is refreshed every step !!! """
        for doc_id in doc_id_list:
            # all_detail_buttons = get_all_detail_buttons(driver=driver)
            sleep(.4)
            Actor.log.info(doc_id, driver.current_url)  # DRB 6/6
            driver = visit_doc_page(driver=driver, doc_id=doc_id)
            doc_html = driver.page_source
            a, b, amt, p1_li, p2_li = search.get_info_detailed_document_html(html=doc_html)
            # search_data.append([a, b, amt]) # now dict
            if int(strip_zero(amt)) == 0 or a in search_data_dict:  # if doc id is duplicated in res, skip
                pass
            else:
                # search_data_dict[search_item_ctr] = [a, b, amt, p1_li, p2_li, doc_id]
                search_data_dict[doc_id] = [a, b, amt, p1_li, p2_li]  # by address
            print(a, b, amt, p1_li, p2_li, doc_id)
            sleep(.4)
            driver = revert_to_search_res(driver=driver)
            search_item_ctr += 1  # increment counter as key
        # tail condition check
        curr_has_next = search.result_has_go_next(soup=search_res_soup)
        print(curr_has_next, curr_page_num)
        if curr_has_next:
            driver = go_next_page_search_res(driver=driver)
        if browser.small_test:
            return search_data_dict

        """ CUT OFF """
        print("DONE")

    return search_data_dict

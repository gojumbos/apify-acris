

import argparse
import flask

# from browser import *
import browser as brows
import em
from datetime import datetime, date, timedelta
from pandas.tseries.offsets import BDay

import constants

import logging

def finalize_data(search_data: dict):
    return list(search_data.values())


def main(show_head=False, style=None, small_test=False,
         run_local=False, Actor=None,
         actor_input=None
         ):
    """
    Begin script
    OTHER == RPTT_RETT, is a subset of DEED
    TO DO:
    split up into 3 scripts
    --
    SOURCE: main.py from _v2 acris
    """

    # logger = logging.getLogger('logger')
    if Actor is None or actor_input is None:
        try:
            pass
        except Exception:
            exit(code=36)

    search_data_dict = {}  # doc_id -> [a, b, amt, p1, p2]
    item_ctr = 0
    # yesterday = datetime.now() - timedelta(days=1)
    # prev_day = datetime.today() - BDay(4)
    today = datetime.today()
    if today.weekday() == 0:
        prev_day = today - timedelta(days=3)
    elif today.weekday() == 6:
        # logger.error('Today is Sunday')
        Actor.log.exception('Line 42', {'Today is Sunday'})
        return
    elif today.weekday() == 5:
        Actor.log.exception('Today is Saturday')
    else:
        prev_day = datetime.now() - timedelta(days=1)
    date = str(prev_day.strftime('%m/%d/%y')).split('/')
    # date = str(datetime.now().strftime('%m/%d/%y')).split('/')
    # date[1] = str(int(date[1]) - 1)  # yesterday
    date = tuple(date)
    """ loop through all doc types """
    # for search_type in ["OTHER",]:  # search type
    if small_test:
        groups = ["DEED"]
        # logger.warning(str(groups))
        Actor.log.info("Line 56", {str(groups)})
    else:
        groups = ["DEED", "OTHER", "LOAN"]
    for search_type in groups:  # search type
        # logger.warning("start search: " + search_type)
        browser = brows.Browser(search_type=search_type, date=date,
                                show_head=show_head,
                                small_test=small_test,
                                run_local=run_local,
                                actor_input=actor_input,
                                actor=Actor
                                )
        driver = browser.driver
        """ loop through all sub types of search type """
        for sub_type in browser.sub_types:
            Actor.log.info("sub-type search: " + sub_type)
            browser.update_sub_type(new_sub_type=sub_type)
            search_data_dict = brows.run_search(browser=browser,
                                                driver=driver,
                                                search_data_dict=search_data_dict,
                                                search_item_ctr=item_ctr,
                                                actor=Actor
                                                )
            """ SEARCH RESULT """
            # driver.close()  # main line 99
    file_path = 'data_temp.txt'

    with open(file_path, 'w') as f:
        for key, value in search_data_dict.items():
            f.write(f"{key}: {value}\n")

    finalize_data(search_data=search_data_dict)

    print("saved")

    print("DONE SCRAPE")

    """ SEND EMAIL """
    data = list(search_data_dict.values())
    emailer = em.EmailInterface(scrape_date=date,
                                actor_input=actor_input)
    emailer.send_all_emails(all_data=data)

    return driver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--show_head", action="store_true")
    parser.add_argument("--run_local", action="store_true")
    args = parser.parse_args()
    main(args.show_head, args.run_local)



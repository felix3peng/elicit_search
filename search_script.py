# -*- coding: utf-8 -*-
"""
Selenium script to scrape search results from elicit.org
Created on Mon Jun 13 15:21:49 2022

@author: Felix
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import itertools
import os
import glob
from config import elicit_user, elicit_pass

global subtopic_count, master_path
master_path = os.getcwd()
subtopic_count = 0


'''define helper functions'''


# collate_terms searches for every term in a set and saves results as csv
def collate_terms(term_list, overwrite=False):
    # iterate which subtopic number it is on
    global subtopic_count
    subtopic_count += 1
    print('-------------------------------------------------------------')
    print('Commencing search for Subtopic ', subtopic_count)
    print(len(term_list), ' terms processing...')
    fcount = 0
    subfolder = 'subtopic' + str(subtopic_count)
    subpath = os.path.join(result_folder, subfolder)
    # check whether directory already exists for the subtopic
    if os.path.isdir(subpath) is False:
        print('Creating new directory')
        os.mkdir(subpath)
    # depending on overwrite flag, may delete existing csv files saved in dir
    if (os.path.isdir(subpath)) & (overwrite is True):
        files = glob.glob(os.path.join(subpath, '*'))
        for f in files:
            os.remove(f)
    elif (os.path.isdir(subpath)) & (overwrite is False):
        pass
    # iterates through each term and checks for existing
    for t in term_list:
        new_name = t.replace(' ', '') + '.csv'
        nterms = len(term_list)
        if os.path.isfile(os.path.join(subpath, new_name)):
            print('file already exists')
            nterms -= 1
            pass
        else:
            # if no previous file, perform search, show 24 results
            #   (click show more twice) and then save as csv
            searchbar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div[1]/div/form/div/div/textarea[1]')
            searchbar.send_keys(Keys.CONTROL + "a")
            searchbar.send_keys(Keys.DELETE)
            searchbar.send_keys(t)
            searchbar.send_keys(Keys.RETURN)
            # find and click the show more button twice
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                show_more = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div/div[3]/button')))
                show_more.click()
            # if sidebar with 'download csv' button hidden, open it
            try:
                expand_sidebar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div[1]/button')
                expand_sidebar.click()
            except:
                pass
            # wait before clicking button (helps with stability)
            time.sleep(3)
            # find and click download button, then wait for 3s and rename it
            csv = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div[2]/div[2]/div[4]/button[2]')
            csv.click()
            new_name = t.replace(' ', '') + '.csv'
            time.sleep(3)
            os.rename(os.path.join(result_folder, orig_name), os.path.join(subpath, new_name))
            fcount += 1
            # print a message for every 10 files to avoid overload
            if fcount % 10 == 0:
                print('File ', fcount, '/', nterms, ' successfully downloaded and renamed!')


'''define search terms'''
# subtopic 1: trustworthiness
prefixes_1 = ['trustworthy', 'trustworthiness', 'trust']
suffixes_1 = ['framework', 'principles', 'factors', 'drivers', 'machines',
              'automation']
# compose search combinations
s1_terms = []
s1_terms.extend(prefixes_1)
s1_terms.extend([x + ' ' + y for x, y
                 in itertools.product(prefixes_1, suffixes_1)])

# subtopic 2: trustworthy AI
prefixes_2 = ['trustworthy', 'trustworthiness', 'trust']
suffixes_21 = ['AI', 'artificial intelligence']
suffixes_22 = ['framework', 'guidelines', 'principles', 'pillars',
               'components']
# compose search combinations
s2_terms = []
s2_terms.extend([x + ' ' + y for x, y
                 in itertools.product(prefixes_2, suffixes_21)])
s2_terms.extend([x + ' ' + y + ' ' + z for x, y, z
                 in itertools.product(prefixes_2, suffixes_21, suffixes_22)])

# subtopic 3: trustworthy AI tools and checklists
prefixes_3 = ['trustworthy', 'trustworthiness', 'trust', 'responsible',
              'ethical', 'fair', 'safe', 'human centered', 'principled']
midterms_3 = ['AI', 'artificial intelligence']
suffixes_3 = ['checklist', 'guide', 'evaluation', 'assessment', 'tools',
              'aids', 'aides']
# compose search combinations
s3_terms = [x + ' ' + y + ' ' + z for x, y, z
            in itertools.product(prefixes_3, midterms_3, suffixes_3)]

'''selenium instance'''
# start up selenium driver and retrieve elicit.org login page
# also set up headless mode (no window opens) and maximized window
# set default download directory to the results folder
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--start-maximized')
result_folder = os.path.join(master_path, 'results')
prefs = {"download.default_directory": result_folder}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
# by default, wait up to 15s for an element to be visible or interactable
driver.implicitly_wait(15)
driver.get('https://elicit.org/login')

# log in to elicit.org
login = driver.find_element(By.XPATH,
                            '//*[@id="auth"]/div/div[1]/form/ul/li[1]/button')
login.click()
email = driver.find_element(By.XPATH,
                            '//*[@id="ui-sign-in-email-input"]')
email.click()
email.send_keys(elicit_user)
email.send_keys(Keys.RETURN)
pwd = driver.find_element(By.XPATH,
                          '//*[@id="ui-sign-in-password-input"]')
pwd.send_keys(elicit_pass)
pwd.send_keys(Keys.RETURN)

# initial search to get to normal search page interface
textarea = driver.find_element(By.XPATH,
                               '//*[@id="__next"]/div/main/div/div/form/div[3]/div/textarea[1]')
textarea.send_keys('test')
textarea.send_keys(Keys.RETURN)

# perform searches
orig_name = 'elicit-results.csv'
collate_terms(s1_terms, overwrite=True)
collate_terms(s2_terms, overwrite=True)
collate_terms(s3_terms, overwrite=True)

# close instance
driver.close()

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

global subtopic_count, master_path
master_path = os.getcwd()
subtopic_count = 0

'''define helper functions'''


def collate_terms(term_list, overwrite=False):
    global subtopic_count
    subtopic_count += 1
    print('-------------------------------------------------------------')
    print('Commencing search for Subtopic ', subtopic_count)
    print(len(term_list), ' terms processing...')
    fcount = 0
    subfolder = 'subtopic' + str(subtopic_count)
    subpath = os.path.join(result_folder, subfolder)
    if os.path.isdir(subpath) is False:
        print('Creating new directory')
        os.mkdir(subpath)
    if (os.path.isdir(subpath)) & (overwrite is True):
        files = glob.glob(os.path.join(subpath, '*'))
        for f in files:
            os.remove(f)
    elif (os.path.isdir(subpath)) & (overwrite is False):
        pass
    for t in term_list:
        new_name = t.replace(' ', '') + '.csv'
        nterms = len(term_list)
        if os.path.isfile(os.path.join(subpath, new_name)):
            print('file already exists')
            nterms -= 1
            pass
        else:
            searchbar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div[1]/div/form/div/div/textarea[1]')
            searchbar.send_keys(Keys.CONTROL + "a")
            searchbar.send_keys(Keys.DELETE)
            searchbar.send_keys(t)
            searchbar.send_keys(Keys.RETURN)
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # show_more = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div/div[3]/button')
                # show_more.click()
                show_more = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div/div[3]/button')))
                show_more.click()
                # driver.execute_script("arguments[0].click();", show_more)
            try:
                expand_sidebar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div[1]/button')
                expand_sidebar.click()
            except:
                pass
            time.sleep(3)
            csv = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div[2]/div[2]/div[4]/button[2]')
            csv.click()
            new_name = t.replace(' ', '') + '.csv'
            time.sleep(3)
            os.rename(os.path.join(result_folder, orig_name), os.path.join(subpath, new_name))
            fcount += 1
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
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--start-maximized')
result_folder = os.path.join(master_path, 'results')
prefs = {"download.default_directory": result_folder}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)
driver.get('https://elicit.org/login')

# log in to elicit.org
login = driver.find_element(By.XPATH,
                            '//*[@id="auth"]/div/div[1]/form/ul/li[1]/button')
login.click()
email = driver.find_element(By.XPATH,
                            '//*[@id="ui-sign-in-email-input"]')
email.click()
email.send_keys('felix.peng@zs.com')
email.send_keys(Keys.RETURN)
pwd = driver.find_element(By.XPATH,
                          '//*[@id="ui-sign-in-password-input"]')
pwd.send_keys('s7an13317')
pwd.send_keys(Keys.RETURN)

# initial search
textarea = driver.find_element(By.XPATH,
                               '//*[@id="__next"]/div/main/div/div/form/div[3]/div/textarea[1]')
textarea.send_keys('test')
textarea.send_keys(Keys.RETURN)

# perform searches
orig_name = 'elicit-results.csv'
collate_terms(s1_terms)
collate_terms(s2_terms)
collate_terms(s3_terms)

# close instance
driver.close()

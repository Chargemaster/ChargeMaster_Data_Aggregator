"""
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
"""
import re
from time import time
import os
import errno
import shutil
import uuid
import json

from urllib.parse import urljoin
from urllib.request import urlretrieve
from urllib3.exceptions import MaxRetryError

import requests


#import numpy as np
from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL, SSLError, ConnectionError

import constant

from selenium.common.exceptions import ElementNotInteractableException, InvalidArgumentException
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

hospital_urls = json.load(open(constant.URLS_PATH))
blacklist = json.load(open(constant.BLACKLIST_PATH))

def load_webdriver():
    return webdriver.Chrome(constant.CHROMEDRIVER_PATH, options=chrome_options)


"""
Didn't foresee that exception handling for just making the HTTP request would be
this difficult to track down. Broke apart the web crawler into two parts, one
for making the request and handling the HTTP status codes and one to parse
the actual HTML returned. 
"""
def get_request(hospital_name=None, url=None):
    if not hospital_name or not url: return
    req = None
    try:
        req = requests.get(url, headers=constant.HEADERS)
    except (InvalidURL, ConnectionError):
        print(f"Invalid URL: {url}, Hospital: {hospital_name}")
        try:
            req = requests.get(url, verify=False, headers=constant.HEADERS)
        except: return
    except (SSLError):
        try:
            req = requests.get(url, verify=False, headers=constant.HEADERS)
        except: return
    """
    Not doing 400s and 500s. Fiddling with headers still won't let me access some sites. 
    400s are usually invalid urls that are outdated. 
    Majority of the urls are still valid and return 200. 
    """
    if req.status_code >= 400: return None 
    return req

# Taken from https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
    except:
        return False
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def is_blacklist(url):
    blist = [site for site in blacklist if (site in url)]
    is_blacklisted = len(blist) > 0 
    return is_blacklisted

def selenium_handle(url, time_diff):
    print(f"Selenium handling: {url}")
    if time_diff > constant.MAX_RUN_TIME: return
    #print("Selenium started", time_diff)
    wd = load_webdriver()
    try:
        wd.get(url)
    except (MaxRetryError, InvalidArgumentException): 
        wd.quit()
        return

    try:
        elems = wd.find_elements(By.XPATH, "//a[@onclick]")
        for elem in elems:
            try:
                #print(f"Found {str(elem)} onclick element")
                elem.click()
            except ElementNotInteractableException: continue
    except: 
        wd.quit()
        return
    wd.quit()

"""
Code to check if any hospital data has been downloaded
Will check the working directory for any new files and move them to the subdirectory given. Moving files across file systems must be an atomic operation meaning that it is the only one run for the given process at a time.

The code for this was taken from https://alexwlchan.net/2019/03/atomic-cross-filesystem-moves-in-python/.
"""

# https://alexwlchan.net/2019/03/atomic-cross-filesystem-moves-in-python/
def safe_move(src, dst):
    """Rename a file from ``src`` to ``dst``.

    *   Moves must be atomic.  ``shutil.move()`` is not atomic.
        Note that multiple threads may try to write to the cache at once,
        so atomicity is required to ensure the serving on one thread doesn't
        pick up a partially saved image from another thread.

    *   Moves must work across filesystems.  Often temp directories and the
        cache directories live on different filesystems.  ``os.rename()`` can
        throw errors if run across filesystems.

    So we try ``os.rename()``, but if we detect a cross-filesystem copy, we
    switch to ``shutil.move()`` with some wrappers to make it atomic.
    """
    try:
        os.rename(src, dst)
    except OSError as err:

        if err.errno == errno.EXDEV:
            # Generate a unique ID, and copy `<src>` to the target directory
            # with a temporary name `<dst>.<ID>.tmp`.  Because we're copying
            # across a filesystem boundary, this initial copy may not be
            # atomic.  We intersperse a random UUID so if different processes
            # are copying into `<dst>`, they don't overlap in their tmp copies.
            copy_id = uuid.uuid4()
            tmp_dst = "%s.%s.tmp" % (dst, copy_id)
            shutil.copyfile(src, tmp_dst)

            # Then do an atomic rename onto the new name, and clean up the
            # source image.
            os.rename(tmp_dst, dst)
            os.unlink(src)
        else:
            raise

"""
ERROR: Cross file system transfers cannot be done with os.rename, os.replace
Try using OS methods but if it doesn't work, use shuttil.move
Needs to be atomic
"""
def check_and_move_files():
    if not constant.SUBDIR_PATH: return
    filenames = os.listdir(".")
    for filename in filenames:
        if filename in constant.IGNORE_LIST: continue
        safe_move(f"./{filename}", f"{constant.SUBDIR_PATH}/{filename}")

"""
Just replace all whitespace in the name with a underscore (_) for file naming conventions.
The names are taken from the WSHA page. We can assume they do not have any
mistakes such as having whitespace in front of the name or behind.

Will return the path of the subdirectory.
"""
def create_subdir(hospital_name):
    hospital_name = hospital_name.strip()
    subdir_name = hospital_name.replace(" ", "_")
    FULL_PATH = f"{constant.SUBDIR_PATH}/{subdir_name}"
    if not os.path.isdir(FULL_PATH): 
        os.mkdir(FULL_PATH)
    return FULL_PATH

def is_within_time(starttime): return time() - starttime < constant.MAX_RUN_TIME

def is_downloadable_link(page):
  content_type = str(page.headers['content-type']).lower()
  if 'text' in content_type or 'html' in content_type: 
    return False
  return True

def format_url(url, href):
    full_url = ""
    if 'http' not in href: # These are strict redirects. 
        if href.startswith("."): return None
        elif url.endswith("/"): full_url = url + href
        else: full_url = f"{url}/{href}"
        full_url = full_url.replace("//", "/")
        if 'https:/' in full_url: full_url = full_url.replace("https:/", "https://")
        else: full_url = full_url.replace("http:/", "http://")
    else: 
        full_url = href
    return full_url

def url_format(url, href):
    full_url = ""
    if 'http' not in href:
        if 'para' in href: print(href)
        if not full_url.endswith("/"): full_url = url + "/" 
        full_url = urljoin(full_url, href)
    else: full_url = href
    return full_url
  

def get_domain(url):
    pattern = '(http[s]?:\/\/([w]{3}\.)?[a-zA-Z1-9]*\.(org|com|net)).*'
    if type(url) != str: return None
    match = re.match(pattern, url)
    if match: return match.group(1)
    return match

def check_download(full_url, page):
  if is_downloadable_link(page):
    filename = full_url.split("/")[-1]
    print(f"{filename} is downloadable")
    try:
      urlretrieve(full_url, f"./{filename}") # download with unique 
    except: pass

def check_selenium(soup, url, starttime):
    soup_html = str(soup)
    if 'onclick' in soup_html:
        selenium_handle(url, time() - starttime)


# Don't need this
def check_for_csv_xlsx_files(hospital_name, hrefs, url, starttime, levels):
    full_url = ""
    for href in hrefs:
        if not href: continue
        if href.endswith("csv") or href.endswith("xlsx"):
            if 'http' not in href: # These are strict redirects. 
                if href.startswith("."): return None
                elif url.endswith("/"): full_url = url + href
                else: full_url = f"{url}/{href}"
            else: 
                full_url = href
            print(f"Found file: {href}")
            domain_link = get_domain(f"{hospital_urls[hospital_name]['hospital_url']}")
            alternative_link=f"{domain_link}/{href}"
            try:
                filename = href.split("/")[-1]
                urlretrieve(alternative_link, f"./{filename}")
            except:
                pass
            try:
                filename = href.split("/")[-1]
                urlretrieve(href, f"./{filename}")
            except:
                pass
            crawl_and_scrape(hospital_name, alternative_link, starttime, 1, [], []) 
            crawl_and_scrape(hospital_name, full_url, starttime, 1, [],[]) # terminate there.
      
def check_apx(hospital_name, url, starttime, visited_urls, visited_hrefs):
    if 'apps.para' in url: 
        crawl_and_scrape(hospital_name=hospital_name,
            url=url,
            starttime=starttime,
            levels=3, # Refresh levels to keep this call going longer. 
            visited_urls=visited_urls,
            visited_hrefs=visited_hrefs
        )


def crawl_and_scrape(hospital_name, url, starttime, levels, visited_urls, visited_hrefs):
    if levels == 0: return
    if not is_within_time(starttime): return
    if url in visited_urls: return
    if is_blacklist(url): return

    print(f"Crawling & Scraping for {hospital_name}, on current URL: {url}, {levels} levels deep.")
    try: # malformed url sometimes
        page = get_request(hospital_name, url)
    except requests.exceptions.InvalidSchema: return
    if not page: return
    visited_urls.append(url) # Add to visited webpage list
    soup = BeautifulSoup(page.content)
    check_download(url, page)
    # Check Selenium
    check_selenium(soup, url, starttime)
    for a_href in soup.findAll('a'):
        if not is_within_time(starttime): break
        href = a_href.get('href')
        if href in visited_hrefs: continue
        visited_hrefs.append(href)
        if not href: continue # No href links so 'url' will be NoneType
        if href.endswith(".pdf"): continue
        full_url = url_format(url, href)
        #check_for_csv_xlsx(url, href)
        check_apx(hospital_name, full_url, starttime, visited_urls, visited_hrefs)
    
        if not full_url: continue
    # If website is on our blacklist, skip
        if is_blacklist(full_url): continue
        crawl_and_scrape(hospital_name=hospital_name, 
            url=full_url, 
            starttime=starttime, 
            levels=levels-1, 
            visited_urls=[], 
            visited_hrefs=[]
        )
        
        
        # Check to see if we can download the file

def scrape_hospitals():
    for hospital_name, hospital_data in hospital_urls.items():
        hospital_url = hospital_data['hospital_url']
        if not hospital_url: continue # Some fields may not have a hospital url
        if 'cdm_missing' in hospital_data.keys() and hospital_data['cdm_missing']:
            continue
        if hospital_data['scraped_cdm']: continue # already have the cdm
        print("============================================================================")
        print(f"Scraping the current hospital: {hospital_name}")
        crawl_and_scrape(hospital_name=hospital_name, 
            url=hospital_url, 
            starttime=time(), 
            levels=10, 
            visited_urls=[], 
            visited_hrefs=[]
        )
        check_and_move_files()
        # Update to show we checked this hospital already and save to json.
        hospital_data['scraped_cdm'] = True
        hospital_urls[hospital_name] = hospital_data
        with open(constant.URLS_PATH, 'w') as outfile:
            json.dump(hospital_urls, outfile)

if __name__ == '__main__':
    # Load json containing the URLs about the hospitals
    hospital_urls = json.load(open(constant.URLS_PATH))

    # Load json containing blacklisted websites
    blacklist = json.load(open(constant.BLACKLIST_PATH))
    scrape_hospitals()
    
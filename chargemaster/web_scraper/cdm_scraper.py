"""
Author: Ji KAng
December 13, 2021

This Python program is an implementation of a web scraper. It is designed to
scrape chargemaster (CDM) information from WSHA associated hospitals given
a JSON file with all associated hospital's corresponding URLs. It will
recursively examine each web page. It is restricted and changed through
constant.py which holds static values for the scraper to follow.

An example is the subdirectory path in which to save the data
(see constant.SUBDIR_PATH). Modifying these values inherently change
how the web scraper functions. It will save any scraped files under
'data/scraped_files/{hospital_name}'
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

from bs4 import BeautifulSoup
from requests.exceptions import InvalidURL, SSLError

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
    """Loads a chrome web driver with given options. Returns it."""
    return webdriver.Chrome(constant.CHROMEDRIVER_PATH, options=chrome_options)

def get_request(hospital_name=None, url=None):
    """
    Function gets a hospital name for information only. Given a url,
    the function will make a request to the URL with given
    headers (see constant.py). From there, it will return
    the request object or None if unsucessful.

        Parameters:
            hospital_name (string): Name of hospital for debugging output
            url (string): URL of webpage

        Returns:
            req (Request): Request object of webpage
    """
    if not hospital_name or not url:
        return None
    req = None
    try:
        req = requests.get(url, headers=constant.HEADERS)
    except (InvalidURL, ConnectionError):
        print(f"Invalid URL: {url}, Hospital: {hospital_name}")
        try:
            req = requests.get(url, verify=False, headers=constant.HEADERS)
        except:
            return None
    except SSLError:
        try:
            req = requests.get(url, verify=False, headers=constant.HEADERS)
        except:
            return None
    if req.status_code >= 400:
        return None
    return req


def is_downloadable(url):
    """
    Tests for if the URL contains a downloadable resource. E.g. One that isn't HTML.
    Code attributed to:
    https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un
    Function will make a HEAD http request to the URL. Examine its content-type,
    and evaluate if it is not HTML or text. Returns true if neither of them,
    false otherwise.

        Parameters:
            url (string): URL of webpage

        Returns:
            is_downloadable (boolean): If given URL is downloadable
    """
    try:
        headers = requests.head(url, allow_redirects=True)
    except:
        return False
    header = headers.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def is_blacklist(url):
    """
    Function checks if the given url contains any identifiers that are in the blacklist.
    For example, the scraper will stay away from domains such as facebook, linkedin,
    tiktok, youtube, yahoo, and so on.

        Parameters:
            url (string): URL of webpage

        Returns:
            is_blacklisted (boolean): True if blacklisted, False otherwise.
    """
    blist = [site for site in blacklist if site in url]
    is_blacklisted = len(blist) > 0
    return is_blacklisted

def selenium_handle(url, time_diff):
    """
    Function sends any urls containing javascript elements to the webdriver to handle.
    Checks if the given time limit has expired. If not, will get the webpage
    using Selenium's built-in "get", find all elements containing 'onclick' using
    an XPATH, then iterate through and click them all.

        Parameters:
            url (string): URL of webpage
            time_diff (int): Time elapsed since the scraper began for the hospital

    """
    print(f"Selenium handling: {url}")
    if time_diff > constant.MAX_RUN_TIME:
        return
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
                elem.click()
            except ElementNotInteractableException:
                continue
    except:
        wd.quit()
        return
    wd.quit()


def safe_move(src, dst):
    """
    Code to check if any hospital data has been downloaded. Will check the working directory
    for any new files and move them to the subdirectory given.
    Moving files across file systems must be an atomic operation meaning that
    it is the only one run for the given process at a time.

    The code for this was taken from
    https://alexwlchan.net/2019/03/atomic-cross-filesystem-moves-in-python/.
    The documentation for the code snippet, from alexwlchan is below:
    Rename a file from ``src`` to ``dst``.

    *   Moves must be atomic.  ``shutil.move()`` is not atomic.
        Note that multiple threads may try to write to the cache at once,
        so atomicity is required to ensure the serving on one thread doesn't
        pick up a partially saved image from another thread.

    *   Moves must work across filesystems.  Often temp directories and the
        cache directories live on different filesystems.  ``os.rename()`` can
        throw errors if run across filesystems.

        So we try ``os.rename()``, but if we detect a cross-filesystem copy, we
        switch to ``shutil.move()`` with some wrappers to make it atomic.

        Parameters:
            src (string): Source directory path
            dest (int): Destination directory path
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

def check_and_move_files(subdir_path=None):
    """
    Function will check the current directory for any new files.
    Compare all files to a ignore list and if they're not on the ignore
    list, will move them to the "subdir_path" provided.

        Parameters:
            subdir_path (string): Relative path to destination

    """
    if not constant.SUBDIR_PATH:
        return
    filenames = os.listdir(".")
    for filename in filenames:
        if filename in constant.IGNORE_LIST:
            continue
        safe_move(f"./{filename}", f"{subdir_path}/{filename}")

def create_subdir(hospital_name):
    """
    Given a hospital name, will check if a subdirectory for that
    hospital already exists under the scraped_files directory.
    If not, creates, and returns the path to this subdirectory.

        Parameters:
            hospital_name (string): Name of hospital

        Returns:
            full_path (string): Filepath of created subdirectory
    """
    hospital_name = hospital_name.strip()
    subdir_name = hospital_name.replace(" ", "_")
    full_path = f"{constant.SUBDIR_PATH}/{subdir_name}"
    if not os.path.isdir(full_path):
        os.mkdir(full_path)
    return full_path

def is_within_time(starttime):
    """
    Given a starttime, returns True if time elapsed is
    within the time limit, False otherwise
    """
    return time() - starttime < constant.MAX_RUN_TIME

def is_downloadable_link(page):
    """
    Given a page, checks its content-type for text or html.
    Returns true if neither are found, false otherwise.

        Parameters:
            page (Request): Request page object

        Returns:
            is_downloadable (boolean): If given page is downloadable or not
    """
    content_type = str(page.headers['content-type']).lower()
    if 'text' in content_type or 'html' in content_type:
        return False
    return True

def format_url(url, href):
    full_url = ""
    if 'http' not in href: # These are strict redirects.
        if href.startswith("."):
            return None
        if url.endswith("/"):
            full_url = url + href
        else:
            full_url = f"{url}/{href}"
        full_url = full_url.replace("//", "/")

        if 'https:/' in full_url:
            full_url = full_url.replace("https:/", "https://")
        else:
            full_url = full_url.replace("http:/", "http://")
    else:
        full_url = href
    return full_url

def url_format(url, href):
    full_url = ""
    if 'http' not in href:
        if 'para' in href: print(href)
        if not full_url.endswith("/"):
            full_url = url + "/"
        full_url = urljoin(full_url, href)
    else: full_url = href
    return full_url


def get_domain(url):
    pattern = r'(http[s]?:\/\/([w]{3}\.)?[a-zA-Z1-9]*\.(org|com|net)).*'
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
    except:
        pass

def check_selenium(soup, url, starttime):
    soup_html = str(soup)
    if 'onclick' in soup_html:
        selenium_handle(url, time() - starttime)


# Don't need this
def check_for_csv_xlsx_files(hospital_name, hrefs, url, starttime, levels):
    full_url = ""
    for href in hrefs:
        if not href:
            continue
        if href.endswith("csv") or href.endswith("xlsx"):
            if 'http' not in href: # These are strict redirects.
                if href.startswith("."):
                    return None
                if url.endswith("/"):
                    full_url = url + href
                else:
                    full_url = f"{url}/{href}"
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


def validate_args(url, starttime, levels, visited_urls):
    if levels == 0:
        return False
    if not is_within_time(starttime):
        return False
    if url in visited_urls:
        return False
    if is_blacklist(url):
        return False

def crawl_and_scrape(hospital_name, url, starttime, levels, visited_urls, visited_hrefs):
    if not validate_args(url, starttime, levels, visited_urls):
        return

    print(f"Crawling & Scraping for {hospital_name}, on current URL: {url}, {levels} levels deep.")
    try: # malformed url sometimes
        page = get_request(hospital_name, url)
    except requests.exceptions.InvalidSchema:
        return
    if not page:
        return
    visited_urls.append(url) # Add to visited webpage list
    soup = BeautifulSoup(page.content)
    check_download(url, page)
    # Check Selenium
    check_selenium(soup, url, starttime)
    for a_href in soup.findAll('a'):
        if not is_within_time(starttime):
            break
        href = a_href.get('href')
        if href in visited_hrefs:
            continue
        visited_hrefs.append(href)
        if not href:
            continue # No href links so 'url' will be NoneType
        if href.endswith(".pdf"):
            continue
        full_url = url_format(url, href)
        #check_for_csv_xlsx(url, href)
        check_apx(hospital_name, full_url, starttime, visited_urls, visited_hrefs)

        if not full_url:
            continue
    # If website is on our blacklist, skip
        if is_blacklist(full_url):
            continue
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
        if not hospital_url:
            continue # Some fields may not have a hospital url
        if 'cdm_missing' in hospital_data.keys() and hospital_data['cdm_missing']:
            continue
        if hospital_data['scraped_cdm']:
            continue # already have the cdm
        print("============================================================================")
        print(f"Scraping the current hospital: {hospital_name}")
        crawl_and_scrape(hospital_name=hospital_name,
            url=hospital_url,
            starttime=time(),
            levels=10,
            visited_urls=[],
            visited_hrefs=[]
        )
        subdir_path = create_subdir(hospital_name)
        check_and_move_files(subdir_path)
        # Update to show we checked this hospital already and save to json.
        hospital_data['scraped_cdm'] = True
        hospital_urls[hospital_name] = hospital_data
        with open(constant.URLS_PATH, 'w') as outfile:
            json.dump(hospital_urls, outfile, indent=4)

if __name__ == '__main__':
    # Load json containing the URLs about the hospitals
    hospital_urls = json.load(open(constant.URLS_PATH))

    # Load json containing blacklisted websites
    blacklist = json.load(open(constant.BLACKLIST_PATH))
    scrape_hospitals()
    
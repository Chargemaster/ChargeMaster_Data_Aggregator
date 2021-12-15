"""
Author: Ji Kang
December 12, 2021
Tests for web scraping module that scrapes chargemaster data from WSHA affiliated hospitals. 
Using the unittest module, there're multiple unit tests
that'll go over the various different functionality associated with the webscraper.
Please look to the function level documentation for more details on each test.
"""

import unittest
import sys
import requests
import os
import datetime as dt
from bs4 import BeautifulSoup

# Need to append path to access the knn file.
sys.path.insert(0, './chargemaster/web_scraper')

import constant
import cdm_scraper

class TestCDMScraper(unittest.TestCase):
    """
    Smoke test to make sure the "knn_regression" function runs. This utilizes
    the sample data given to us.
    """

    def test_smoke(self):
        """
        Smoke test to make sure the file is accessible
        """
        module_name = cdm_scraper.__name__
        assert module_name is not None

    def test_get_request_valid(self):
        """
        Tests that the get_request function can properly handle various URLS
        that are valid. Knowingly returning 200 status codes. 
        """
        valid_urls = [
                    'https://www.fairfaxhospital.com/',
                    'http://www.fcphd.org',
                    'http://www.forkshospital.org'
                    ]
        for url in valid_urls:
            continue # remove
            req = cdm_scraper.get_request(hospital_name="test", url=url)
            assert req is not None

    def test_is_downloadable(self):
        """
        Tests that, if given a valid URL, returns True or False based on
        whether or not that given resource is downloadable. 
        E.g. If there is 'text' in its content type. 
        """
        non_downloadable_urls = [
            'https://uwseds.github.io/',
            'https://google.com',
            'https://yahoo.com',
            'https://stackoverflow.com'
        ]
        for url in non_downloadable_urls:
            assert cdm_scraper.is_downloadable(url) is False
        
        downloadable_urls = [
            ''
        ]

    def test_blacklist_checker(self):
        """
        Tests if the function can properly discern a blacklisted
        website or not. 
        """
        blacklist_urls = [
            'facebook',
            'linkedin',
            'javascript',
            'tiktok'
            ]

        for url in blacklist_urls:
            result = cdm_scraper.is_blacklist(url)
            assert result is True
        
        valid_urls = [
            'notblacklisted',
            'somehospitalname',
            'uwseds.github.io'
        ]

        for url in valid_urls:
            result = cdm_scraper.is_blacklist(url)
            assert result is False

    def test_selenium_handler(self):
        """
        Unit test to test whether the selenium handler can properly
        interact with a known onclick web element to download
        its associated chargemaster file.
        """

        # Load web driver object and check that it's valid
        wd = cdm_scraper.load_webdriver()
        assert wd is not None

        # Load web instance
        wd.get('https://apps.para-hcfs.com/PTT/FinalLinks/ArborHealth_V3.aspx')
        
        # Find all onclick web elements by xpath
        elems = wd.find_elements(cdm_scraper.By.XPATH, "//*[@onclick]")
        
        # Get files in the directory already
        old_files = os.listdir("./")
        # Known truth that the resource exists. 
        assert elems is not None
        for elem in elems:
            try:
                elem.click()
            except:
                continue
        for file in os.listdir("./"):
            if file in old_files:
                continue
            assert "Arbor Health" in file
            os.remove(file)
        

        # Clean up files
        

        # Close web driver instance
        wd.quit()



    def test_get_request_invalid(self):
        """
        WIP
        Unit test that tests the get_request function. Checks that it can properly handle
        invalid/malformed URLs.
        """
        assert True
        invalid_urls = [
            'https://qoieogihqoigq.com',
            #'https://.com',
            #'thisisnotevenanurl'
        ]
        for url in invalid_urls:
            continue
            req = cdm_scraper.get_request(hospital_name="test", url=url)
            assert req is None

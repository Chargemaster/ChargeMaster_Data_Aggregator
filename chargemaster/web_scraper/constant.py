# Constant definitions
MAX_RUN_TIME=480 # 480seconds = 8 minutes max runtime per hospital
URLS_PATH = "./data/hospital_urls.json"
BLACKLIST_PATH = "./chargemaster/web_scraper/blacklist.json"
CHROMEDRIVER_PATH = "./chargemaster/web_scraper/chromedriver"

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}
IGNORE_LIST = ['.config', 'drive', '.ipynb_checkpoints'] # Google Colab or Jupyter Notebook related files. Unrelated to scraped data

SUBDIR_PATH = 'data/scraped_data'


APX_KEYWORD = 'apps.para'
import requests, argparse, re, json
from bs4 import BeautifulSoup
from os.path import exists

"""
Looking at the WSHA webpage, it will return a 403 (Forbidden) HTTP status code with
requests without any headers. It understands it is a GET but refuses to service it. 
Adding the user-agent which let's the server know what kind of application is requesting
the information. The USER_AGENT field listed is what I found locally. 
"""
# URL for Washington State Hospital Association
WSHA_URL = 'https://www.wsha.org/?p=61'
# May need to update user agent. Look in Chrome Developer Tools > Network > Headers
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}
parser = argparse.ArgumentParser(description="Scrape hospital URLS, CDM from hospital URLS, etc. WIP")
parser.add_argument('--scrape_urls', nargs='?', const=True, default=True, type=bool)
parser.add_argument('--scrape_cdms', nargs='?', const=True, default=True, type=bool)
args = parser.parse_args()
scrape_urls, scrape_cdms = args.scrape_urls, args.scrape_cdms

"""
Getting a wsha link, it will return the hospital URL if there is one. 
"""
def get_hospital_data(wsha_link):
    hospital_json = {
        'hospital_url': None, 
        'congressional_district': None,
        'legislative_district': None
    }
    page = requests.get(wsha_link, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = str(soup.find_all("div", class_="col-sm-5")[0])
    #hospital_url_pattern = 'Fax:.*<br\/>\n<a href=\".*\">(.*)<\/a>'
    hospital_url_pattern = '<a href=\".*\">(http[^\s]*)<\/a>'
    congressional_pattern = 'Congressional District: <strong>(\d+)*<\/strong>'
    legislative_pattern = 'Legislative District: <strong>(.*)<\/strong>'
    hospital_url = re.search(hospital_url_pattern, soup)
    if not hospital_url: return hospital_json 
    hospital_json['hospital_url'] = hospital_url.group(1)

    try:
        hospital_json['congressional_district'] = re.search(congressional_pattern, soup).group(1)
        hospital_json['legislative_district'] = re.search(legislative_pattern, soup).group(1)
    except AttributeError:
        print("No district information found")
        return hospital_json
    print(f"{hospital_json['hospital_url']}, Congressional: {hospital_json['congressional_district']}, Legislative: {hospital_json['legislative_district']}")
    return hospital_json

def scrape_hospital_data(): # For now, hospitals that are a member of the WSHA
    page = requests.get(WSHA_URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    members_json = {}
    hospital_list_members = soup.find_all("table", class_="table table-striped tablesorter", id="find-hospital-list")
    #hospital_list_nonmembers = soup.find_all("table", class_="table table-striped tablesorter", id="find-hospital-list-non-member")
    
    # Now we need to get rows with only <td> </td> tags which holds what we need. 
    hospital_members_data = []
    td_elements = hospital_list_members[0].find_all("td")
    for td_element in td_elements:
        td_element = str(td_element)
        if td_element != "<td></td>": # Empty tags
            hospital_members_data.append(td_element)
    
    """
    Some hospitals don't have a county and/or number of beds listed. Need to check each entry. 
    """
    td_pattern = '<td>(.*)</td>'
    url_pattern = 'href=\"(.*)\">(.*)<'
    hospital_name, wsha_url = None, None
    for hospital_data in hospital_members_data:
        hospital_data = re.search(td_pattern, hospital_data).group(1) # Removed <td> </td> and gets whatevers inbetween. 
        if "href" in hospital_data: # If it is a link
            result = re.search(url_pattern, hospital_data)
            wsha_url, hospital_name = f"https://www.wsha.org{result.group(1)}", result.group(2)
            hospital_json = get_hospital_data(wsha_url)
            members_json[hospital_name] = {'wsha_url': wsha_url,
                                            'hospital_url': hospital_json['hospital_url'],
                                            'county': None,
                                            'nbeds': -1,
                                            'congressional_district': hospital_json['congressional_district'], 
                                            'legislative_district': hospital_json['legislative_district']
                                        }
        else:
            if hospital_data.isnumeric(): members_json[hospital_name]['nbeds'] = int(hospital_data)
            else: members_json[hospital_name]['county'] = hospital_data
        #if not hospital_name or not wsha_link: continue
    with open('./data/hospital_urls.json', 'w') as fp:
        json.dump(members_json, fp, indent=4)

if __name__ == '__main__':
    if scrape_urls: 
        print("Scraping WSHA for hospital URLS...")
        scrape_hospital_data()
    if scrape_cdms:
        print("Scraping hospital webpages for CDM files.")

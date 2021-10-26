import waybackpy
import pandas
import requests
import urllib
import requests
import lxml
import bs4
import datetime as dt
from datetime import date, timedelta
import calendar
import selenium
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from selenium import webdriver
import monthdelta
import re
import pandas as pd

from selenium.webdriver.chrome.options import Options



def export_html_full(html):
    """ generates final index html file"""

    html_head = '<!DOCTYPE html>\n<html>\n<head>\n'
    style = '<link rel=¨stylesheet¨ type=¨text/css¨ href=¨style.css¨>\n'
    end_of_head = '</head>\n<body>\n'
    script = '\n <script src="script.js" type="text/javascript"></script>\n'
    html_tail = '</body>\n</html>'
    full_text_html = html_head + style + end_of_head + html + script + html_tail
    with open(f'index.html',
              mode='w') as html_file:
        html_file.write(full_text_html)

def archive_urls(url_list):
    user_agent = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36"  # determined the user-agent.
    archived_urls =[]
    for url in url_list:
        # url =  # determined the URL to be saved.
        wayback = waybackpy.Url(url, user_agent)  # created the waybackpy instance.
        archive = wayback.save()  # saved the link to the internet archive
        print(archive.archive_url)  # printed the URL.
        archived_urls.append(archive.archive_url)
    return archived_urls


def create_csv_df():
    # check adam ni website
    hdr = {'User-Agent': 'Safari/419.3'}
    req = Request('http://adamni.com/neican/digest/ocd/', headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    articles = soup.findAll("a")
    articles = [a for a in articles if 'OCD_' in a.text]
    list_of_df = []
    for article in articles:
        link = 'http://adamni.com' + article.get('href')
        list_of_df.append(pd.read_csv(link))
    df = pd.concat(list_of_df)
    return df


def generate_html(df):
    all_keywords = []
    for index, row in df.iterrows():
        all_keywords.append(row['Keywords'])
    keywords = sorted(set(','.join(all_keywords).split(',')))
    years = []
    not_years = []
    for k in keywords:
        try:
            years.append(str(int(k)))
        except ValueError:
            not_years.append(k)
    print('keywords:'+ str(not_years))

    institutions = ['Politburo','OrganizationDepartment']
    document_types = ['GroupStudySessions', 'Documents' ]

    if len(not_years) != len(institutions+document_types):
        print('please check keywords!')

    html_string ='\n <div class="filterInputs"> <label><input type="radio" name="year" value="" checked><i></i>All years</label> \n '
    for year in years:
        html_string += f'<label><input type="radio" name="year" value={year}><i></i>{year}</label>\n'

    html_string += '\n</div><div class="filterInputs"> <label><input type="radio" name="institution" value="" checked><i></i>All institutions</label>\n'
    for institution in institutions:
        html_string += f'<label><input type="radio" name="institution" value={institution.strip()}><i></i>{institution.strip()}</label>\n'

    html_string += '\n</div><div class="filterInputs"> <label><input type="radio" name="document_type" value="" checked><i></i>All document types</label>\n'
    for document_type in document_types:
        html_string += f'<label><input type="radio" name="document_type" value={document_type.strip()}><i></i>{document_type.strip()}</label>\n'
    html_string += '</div><table>\n'

    for index, row in df.iterrows():
        if 'http' in row["Archive Link"]:
            html_string += f'<div data-filterable="{row["Keywords"].replace(", ", " ")}"><tr><td>{row["Date"]}</td><td>{row["Title"]}</td><td>{row["Institution"]}</td><td>{row["Document Type"]}</td><td><a href={row["Link"]}>Link1</a>, <a href={row["Archive Link"]}>Link1</a></td></tr><tr><td></td><td colspan="4" >{row["Title english (machine translated)"]}</td></tr></div>\n'
        else:
            html_string += f'<div data-filterable="{row["Keywords"].replace(", ", " ")}"><tr><td>{row["Date"]}</td><td>{row["Title"]}</td><td>{row["Institution"]}</td><td>{row["Document Type"]}</td><td><a href={row["Link"]}>Link1</a></td></tr><tr><td></td><td colspan="4" >{row["Title english (machine translated)"]}</td></tr></div>\n'

    html_string +="</table>"
    return html_string


if __name__ == "__main__":
    df = create_csv_df()
    html = generate_html(df)
    export_html_full(html)





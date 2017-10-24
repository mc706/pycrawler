import os
from datetime import datetime

import yaml
import requests
from urllib.parse import urlparse
from splinter import Browser
from bs4 import BeautifulSoup as BS


def get_sites():
    """
    Get Sites from sites folder
    """
    return os.listdir('sites')


def get_site_config(site):
    """
    Get Config from the
    """
    with open(os.path.join('sites', site, 'config.yml'), 'r') as config:
        return yaml.load(config)


def take_screenshot(url, dir):
    """
    Take screenshot of url
    """
    result_path = (dir + '/screen_' + str(urlparse(url).path).replace('/', '_')).rstrip('_') + '.png'
    with Browser('phantomjs') as browser:
        browser.visit(url)
        browser.driver.save_screenshot(result_path)
    return None


def check_url(config, url):
    """
    Check url
    """
    print("Checking: {}".format(url))
    result = {}
    urls = []
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BS(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        parsed_uri = urlparse(href)
        domain = "{parsed_uri.scheme}://{parsed_uri.netloc}".format(parsed_uri=parsed_uri)
        if domain == config['domain']:
            urls.append(link.get('href'))
    res = take_screenshot(url, config['dir'])
    result['status_code'] = response.status_code
    result['timing'] = response.elapsed
    print('Result: {} in {}. Found {} links'.format(result['status_code'], result['timing'], len(urls)))
    return result, urls


def run(site):
    """
    Run the tests for a site
    """
    time = str(datetime.now()).replace(" ", "_")
    run_name = "crawl_{}".format(time)
    config = get_site_config(site)
    print("Running: {}".format(config['name']))
    config['run'] = run_name
    config['dir'] = "sites/{}/{}".format(site, run_name)
    os.mkdir(config['dir'])
    context = {
        'urls': config['entry_points'],
        'seen': [],
        'results': {}
    }
    while len(context['urls']):
        url = context['urls'].pop()
        context['seen'].append(url)
        result, found_urls = check_url(config, url)
        context['results'][url] = result
        for new_url in found_urls:
            if new_url not in context['seen'] and new_url not in context['urls']:
                context['urls'].append(new_url)
        print("Unique Links Left: ", len(context['urls']), "Links Checked", len(context['seen']))
    with open(os.path.join(config['dir'], 'report.yml'), 'w') as report:
        yml = yaml.dump(context['results'], default_flow_style=False)
        report.write(yml)


def run_suite(suites=None):
    if not suites:
        suites = get_sites()
    for suite in suites:
        try:
            run(suite)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    import sys

    run_suite(sys.argv[1:])

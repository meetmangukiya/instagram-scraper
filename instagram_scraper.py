import argparse
import csv
import os
import re
import sys
import threading
from typing import Callable, List

import requests
from requests_html import HTMLSession



# Source: http://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
REGEXES = {
    'hashtag': re.compile('(?:#)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'),
    'username': re.compile('(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'),
}


def scrape_instagram_tag(tag: str, total_count: int=50):
    """
    Scrape and yield recently tagged instagram photos.
    """
    url = f'https://www.instagram.com/explore/tags/{tag}'
    session = HTMLSession()
    req = session.get(url)

    count = 0
    page = 0

    while count <= total_count:
        req.html.render(scrolldown=page)
        images = req.html.xpath('//img[@alt]')
        page += 1
        for image in images:
            if count > total_count:
                break
            try:
                url, caption = image.attrs['src'], image.attrs['alt']
            except:
                pass
            else:
                hashtags = set(REGEXES['hashtag'].findall(caption))
                mentions = set(REGEXES['username'].findall(caption))
                count += 1
                yield url, caption, hashtags, mentions


def scrape_instagram(tags: List[str], total_count: int=50):
    """
    :param tags:
        List of tags that need to be scraped.
    :param total_count:
        Total number of images to be scraped.
    """
    for tag in tags:
        yield from scrape_instagram_tag(tag, total_count)

def main(tags, total_count):
    def _single_tag_processing(tag, total_count):
        os.makedirs(f'data/{tag}', exist_ok=True)
        with open(f'data/{tag}/data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for count, (url, caption, hashtags, mentions) in enumerate(scrape_instagram_tag(
                tag, total_count)):

                try:
                    req = requests.get(url)
                    with open(f'data/{tag}/{count}.jpg', 'wb') as img:
                        img.write(req.content)
                except:
                    print(f'An error occured while downloading {url}')
                else:
                    writer.writerow([
                        f'{count}.jpg',
                        url,
                        caption,
                        ', '.join(hashtags),
                        ', '.join(mentions)
                    ])
                    print(f'[{tag}] downloaded {url} as {count}.jpg in data/{tag}')

    for tag in tags:
        _single_tag_processing(tag, total_count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags', '-t', nargs='+',
                        help='Tags to scrape images from')
    parser.add_argument('--count', '-c', type=int, default=50,
                        help='Total number of images to scrape for each given '
                             'tag.')
    args = parser.parse_args()
    assert args.tags, "Enter tags to scrape! Use --tags option, see help."
    assert args.count, "Enter total number of images to scrape using --count option, see help."
    main(args.tags, args.count)

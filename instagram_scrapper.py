import argparse
import csv
import os

import requests
from requests_html import HTMLSession

session = HTMLSession()


def scrape(tags, total_count):
    for tag in tags:
        try:
            os.mkdir(tag)
        except FileExistsError:
            pass

        url = 'https://www.instagram.com/explore/tags/' + tag
        req = session.get(url)

        count = 0
        page = 0
        with open(os.path.join(tag, 'data.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

            while count <= total_count:
                req.html.render(scrolldown=page)
                images = req.html.xpath('//img[@alt]')
                page += 1
                for image in images:
                    try:
                        url, caption = image.attrs['src'], image.attrs['alt'].replace('\n', '\\n')

                        with open(os.path.join(tag, str(count) + '.jpg'), 'wb') as img:
                            img.write(requests.get(url).content)

                        writer.writerow([count, caption])
                        print('[{}]'.format(tag), 'downloaded image ' + str(count), url)
                        count += 1
                        if count >= total_count:
                            break
                    except:
                        print('!!one image failed!!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags', '-t', nargs='+',
                        help='Tags to scrape images from')
    parser.add_argument('--count', '-c', type=int,
                        help='Total number of images to scrape for each given '
                             'tag.')
    args = parser.parse_args()
    assert args.tags, "Enter tags to scrape! Use --tags option, see help."
    assert args.count, "Enter total number of images to scrape using --count option, see help."
    scrape(args.tags, args.count)

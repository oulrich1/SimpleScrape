from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import re
import requests
import codecs

from BeautifulSoup import BeautifulSoup as BS

#
# #
# # #
#
#  P U R P O S E
#
#  - to scrape sites for caching and references if/when things change.
#
#  - does not provide an interface to extract data from pages.
#
#  - only provides a quick and dirty way to save information from pages to local drive.
#
# # #
# #
#

# # Global Constants # #
# NONE

# # Global Settings # #
# NONE



def make_get_request(url):
    html = ""
    try:
        page = requests.get(url)
        if page.status_code != 200:
            raise Exception
        if page:
            html = page.text
            url = page.url
    except requests.exceptions.MissingSchema:
        print("Failed to GET page: " + url)
    return html

# Returns html text in list
def scrape_pages(urls):
    return [make_get_request(url) for url in urls]

# ie: given: "hey/there/buddy.php"
#     returns "buddy.html"
def get_filename(url, extension=".html"):
    s = url.split('/')
    for i in range(1, len(s)+1):
        end = s[-i]
        if len(end) > 0:
            return end.split('.')[0] + extension
    return "index" + extension

def get_filenames(urls):
    return [get_filename(url) for url in urls]

# given: "hey/there/buddy.php"
# returns: "hey/there"
def get_baseurl(url):
    return "/".join(url.split("/")[0:-1])

def get_baseurls(urls):
    return [get_baseurl(url) for url in urls]


def write_pages_to_files(pages, filenames, path="./"):
    for idx, filename in enumerate(filenames):
        make_dir_if_not_exists(path)
        with codecs.open(path + filename, "w", "utf-8-sig") as f:
            f.write(pages[idx])

def is_media(url):
    media=[".jpg", ".jpeg", ".png"]
    for m in media:
        if re.search(".*" + m, url):
            return True
    return False

# takes an html page string..
# uses beautiful soup to extract element attributes
# returns a list of image urls..
def get_img_urls(html):
    soup = BS(html)
    imgEls = soup.findAll('img')
    img_urls = []
    for el in imgEls:
        if el.get("src"):
            img_url = el["src"]
            if is_media(img_url):
                img_urls.append(img_url)
    return img_urls


# takes a list of html pages as strings
# returns a list of lists of image urls, see get_img_urls(page)
def get_img_urls_ll(pages):
    return [get_img_urls(html) for html in pages]

def make_dir_if_not_exists(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except:
        print("  Failed to check or create path '" + path + "' directory.")


# downloads image at url 'link' and stores in local "download_path"
# uses 'requests' lib to make a get request through a stream.
# does not throw, fails silently, prints to console on error or success.
def download_image(link, download_path):
    # Check or create download path
    make_dir_if_not_exists(download_path)

    # Download the image by making a get request through a stream
    try:
        img_response = None
        try:
            img_response = requests.request(
                'get', link, stream=True)
            if img_response.status_code != 200:
                raise Exception()
        except:
            # print("  (Request Error)")
            raise Exception()

        # If all is still well then read the response context
        img_content = img_response.content
        with open(os.path.join(download_path,  link.split('/')[-1]), 'wb') as f:
            byte_image = bytes(img_content)
            f.write(byte_image)
            print("  Download Complete: " + link)
    except:
        print("    Failed to download: " + link)



def download_images(links, download_path):
    for link in links:
        download_image(link, download_path)



# # # # # # # #
#             #
#   M A I N   #
#             #
# # # # # # # #
def main():

    urls = [
       "http://techcrunch.com/2015/10/11/microsofts-hardware-push-and-the-falling-pc-market/"
    ]

    # scraping takes a while..
    pages = scrape_pages(urls)

    # # # Save the HTML pages # # #

    # get filenames to make files to write pages to..
    filenames = get_filenames(urls)
    write_pages_to_files(pages, filenames, path="./news/microsoft/")


    # # # Get Important Page Resources # # #

    # get base url and image urls which will be combined to
    # form the full image url, which will be downloaded to
    # build the resources for the website being scraped.
    baseurls = get_baseurls(urls)
    img_urls_ll = get_img_urls_ll(pages) # returned as list of lists of img urls

    # append img url "filenames" to the base url to get FULL image urls
    img_urls = [base + "/" + filename
                for idx, base in enumerate(baseurls)
                for filename in img_urls_ll[idx]]

    # download each image and store it local to the files
    download_images(img_urls, download_path="./news/microsoft/img")
    print("Done.")


if __name__ == "__main__":
    main()
    exit()

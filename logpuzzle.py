#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import argparse
import os
import re
import sys
if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    puzzle_urls = []
    with open(filename, "r") as f:
        log_lists = f.read().split("\n")
        log_lists = list(filter(lambda x: "/puzzle/" in x, log_lists))
        for url in log_lists:
            url_result = re.findall(r'GET (\S+) HTTP', url)
            puzzle_urls.append(url_result[0])
    url_list = create_urls(puzzle_urls)
    url_list = list(set(url_list))
    sorted_urls = sorted(url_list, key=return_last_word)

    def extract_host_name(url):
        """Returning the host names from url"""
        host = re.findall(r'GET (\S+) HTTP', url)
    return sorted_urls


def create_urls(urls):
    front = "http://code.google.com"
    url_return = [front + url for url in urls]
    return url_return


def return_last_word(url):
    return re.findall(r'-(....).jpg', url)


def add_prefixes(filename, host_lists):
    """ Adds server prfixes to urls in host list """
    server_name = "https://" + re.findall(r'\S+\_(\S+)', filename)[0]
    completed_url_list = [server_name + host for host in host_lists]
    return completed_url_list


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print("dir made")
    index_html = "<html><body>"
    for index, url in enumerate(img_urls):
        image_name = "img" + str(index)
        print(f"retrieving {url}")
        urlretrieve(url, dest_dir + "/" + image_name)
        index_html += f"<img src={image_name}></img>"
    index_html += "</body></html>"
    with open(dest_dir + "/index.html", "w") as write_index:
        write_index.write(index_html)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

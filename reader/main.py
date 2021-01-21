import csv
import sys

import requests
from lxml import html
from readability import Document as ReaderDocument


def get_url_object(url):
    """
    Makes a get request to a url and checks the response code is 200 (OK),
    if so returns the given response object.

    If not unceremoniously borks.

    :param url: a url address to attempt to collect a response from, ideally a webpage
    :return: requests response object
    """
    response = requests.get(url)
    assert response.status_code == 200, f"http status is {response.status_code}"
    return response


def get_readable_article(response_object):
    """
    Uses the readability library to produce a suspected summary
    of the article context that is 'readable'

    This currently is not aware that the summary() function can fail

    :param response_object: a requests response object
    :return: a string that is hopefully html friendly
    """
    reader_document = ReaderDocument(response_object.text)
    html_string_object = reader_document.summary()

    return html_string_object


def make_nice_html(string):
    """
    Takes a string and hopes that it is parseable as html then
    tidies it up using some default functionality,
    gives it back as as hopefully tidyier string
    :param string: ideally a html object as a string
    :return: ideally a nicer version of the given string
    """
    html_object = html.fromstring(string)
    clean_html_object = html.clean.clean_html(html_object)
    cleaner_string = clean_html_object.text_content()
    return cleaner_string


def get_simple_article_text(passed_url):
    """
    Takes a url and tries to find an article in it
    Does no error handling at all, we will need to make it handle errors

    :param passed_url: a string that is an url
    :return: a string that is the article at the url given
    """

    response_object = get_url_object(passed_url)
    readable_article = get_readable_article(response_object)
    extracted_text = make_nice_html(readable_article)

    # TODO: This is some nasty cleaning stuff I need to replace
    extracted_text = extracted_text.replace("\n", " ")
    extracted_text = " ".join(extracted_text.split())

    return extracted_text


def main(*args):
    with open("urls.txt") as open_file:
        urls = [line.rstrip() for line in open_file]

    results = []
    for url in urls:
        print(f"url: '{url}'")
        article_text = get_simple_article_text(url)
        results.append([url, article_text])

    with open("results.csv", "w", newline="") as csvfile:
        writer_object = csv.writer(csvfile)
        writer_object.writerows(results)


if __name__ == "__main__":
    main(sys.argv[1:])

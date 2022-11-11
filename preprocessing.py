from bs4 import BeautifulSoup
import argparse
import os
import json
import html


def filter_html(soup: BeautifulSoup):
    """
    Filters tags and their contents from html
    :param soup: Parsed html
    :return: Filtered html
    """
    scripts = soup.find_all("script")
    for tag in scripts:
        tag.decompose()

    iframes = soup.find_all("iframe")
    for tag in iframes:
        tag.decompose()

    link_tags = soup.find_all("link")
    for tag in link_tags:
        tag.decompose()

    metas = soup.find_all("meta")
    for tag in metas:
        tag.decompose()

    styles = soup.find_all("style")
    for tag in styles:
        tag.decompose()

    return soup


def get_paragraphs_string(soup: BeautifulSoup):
    paragraphs = soup.find_all("p")
    result_string_plaintext = ""
    result_string_html = ""

    for paragraph in paragraphs:
        text = paragraph.get_text().strip()
        if text != "":
            result_string_plaintext += f'<p>{text}</p>\n'

        result_string_html += f'{paragraph.decode()}\n'

    return result_string_plaintext, result_string_html


def main(args: dict):
    files = os.listdir(args['input_dir'])
    output_file_plain = open(f"{args['output_file']}_plain.jsonl", 'w+', encoding='utf-8')
    output_file_html = open(f"{args['output_file']}_html.jsonl", 'w+', encoding='utf-8')

    i = 0
    for file in files:
        with open(os.path.join(args['input_dir'], file), 'r', encoding='utf-8') as f:
            text = f.read()

        soup = BeautifulSoup(text)
        soup = filter_html(soup)
        plain, _html = get_paragraphs_string(soup)
        output_file_plain.write(json.dumps({'text': plain, 'label': args['label']}) + '\n')
        output_file_html.write(json.dumps({'text': _html, 'label': args['label']}) + '\n')

        if i % 1000 == 0:
            print(f'{i / len(files) * 100}%')
        i += 1

    output_file_plain.close()
    output_file_html.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, type=str)
    parser.add_argument('--output_file', required=True, type=str, help='jsonl format')
    parser.add_argument('--label', required=True, type=int)
    args = vars(parser.parse_args())
    main(args)




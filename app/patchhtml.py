import re
import html
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

from config import ProxyConfig
from consts import BS_SKIP_TAGS


def patch_html_regex(res: bytes, word_cnt: int,
                     add_str: str, target_url: str) -> bytes:
    """ HTML patcher based on regex expressions with by char html parsing """
    res = res.decode('utf-8')
    result = ''
    st_s = 0
    st_c = 0
    res_len = len(res)
    target_url_len = len(target_url)

    while st_c != res_len:
        if res[st_c] == '>':
            st_res = res[st_s:st_c]
            # change anchors links if exists
            if st_c - st_s > target_url_len:
                st_res = html.unescape(st_res[1:])
                st_res = re.sub("href=\"{}".format(target_url[:-1])
                                + "[/]{0,1}",
                                "href=\"/",
                                st_res)
                st_res = '<'+st_res
            result = result + st_res + '>'
            st_s = st_c+1
        elif res[st_c] == '<':
            if st_c != st_s:
                st_res = res[st_s:st_c+1]
                # replace slash html encoding to str slash
                st_res = html.unescape(st_res)

                #  (?<!/|-) remove matching preceeding word of 6
                #    elements by / or - symbol
                #  this symbols may use in link or - word annotations
                #  \\b[a-zA-Z]{6}\\b - start word (\\b) word with
                #    only 6 symbols and (\\b) end world
                #  (?!<) - test for after world no < symbol - start next
                #    tag used for correct "parent" matching

                tr = re.sub("(?<!/|-)\\b[a-zA-Z]{"
                            + str(word_cnt)
                            + "}\\b(?!<)",
                            "\g<0>" + add_str,
                            st_res)
                tr = html.escape(tr[:-1])
                result = result + tr
                st_s = st_c

        st_c = st_c + 1

    return result.encode("utf-8")


def patch_tag_bs4(tag: Tag, config: ProxyConfig):
    """ Patch single tag """
    for child in tag.children:
        if not isinstance(child, NavigableString):
            continue
        if child.parent != tag:
            continue

        text = re.sub("(?<!/|-)\\b[a-zA-Z]{"
                      + str(config.word_len)
                      + "}\\b(?!<)",
                      "\g<0>" + config.word_app,
                      str(child.string))
        child.string.replace_with(NavigableString(text))


def patch_html_bs4(res: str, config: ProxyConfig) -> str:
    """ HTML patcher based on BeatifulSoup module"""
    html = BeautifulSoup(res.decode('utf-8'), "html.parser")
    for tag in html.find_all(name=True):
        if tag.name not in BS_SKIP_TAGS:
            patch_tag_bs4(tag, config)

    for tag in html.find_all('a'):
        st_res = re.sub("{}".format(config.target_url[:-1]) + "[/]{0,1}",
                        "/", str(tag['href']))
        tag['href'] = st_res

    return html.encode("utf-8")


def patch_html(res: bytes, config: ProxyConfig) -> bytes:
    """ HTML patcher instance """
    if config.regex_patcher:
        return patch_html_regex(res, config.word_len,
                                config.word_app, config.target_url)
    else:
        return patch_html_bs4(res, config)

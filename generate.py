#!/usr/bin/python
# -*- coding:gb18030 -*-

"""Documentation"""

import shutil
import os
import codecs
import shelve
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
import pypinyin


# ��̬�ļ�·����Ĭ��Ϊ`/static/`
# ��ʾʹ��flask������վʱ��`http://ip:port/static/`Ŀ¼
# Ҳ��ָ��Ϊ�̶���ַ�ľ�̬�ļ�url�����磺"http://192.168.62.47:5000/static/"
# ע�⣬ʹ�����������ľ�̬�ļ�ʱ�п��������������
STATIC_ROOT = "/static/"

# Markdown�ļ���ȡĿ¼
INPUT_CONTENT = "./in/"

# �����ļ�
INDEX_DAT = "./static/out/index.dat"

# html�������Ŀ¼
OUTPUT_CONTENT = "./static/out/"

env = Environment(
    loader=FileSystemLoader("templates")
)


# ��ǩ��������
TAG_INVERTED_INDEX = {}
# ���ߵ�������
AUTHOR_INVERTED_INDEX = {}

# ��������
ARTICLE_INDEX = {}
ARTICLE_RANK = {}

_MD_FILES = []

_current_file_index = None
_pinyin_names = set()

TAG_HTML_TEMPLATE = u"<a href='/tag/{tag}/' class='tag-index'>{tag}</a>"
AUTHOR_HTML_TEMPLATE = u"<a href='' class='tag-index'>{author}</a>"
TITLE_HTML_TEMPLATE = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>����</h5><p>{title_str}</p></div>"


def _reload_global():
    global TAG_INVERTED_INDEX, AUTHOR_INVERTED_INDEX, ARTICLE_INDEX,\
        _MD_FILES, _current_file_index, _pinyin_names

    TAG_INVERTED_INDEX = {}
    AUTHOR_INVERTED_INDEX = {}
    ARTICLE_INDEX = {}
    _MD_FILES = []
    _current_file_index = None
    _pinyin_names = set()


def clean():
    """��������ļ���
    """
    if os.path.exists(OUTPUT_CONTENT):
        shutil.rmtree(OUTPUT_CONTENT)


def parse_time(timestamp, pattern="%Y-%m-%d %H:%M:%S"):
    """����ʱ��
    """
    return datetime.fromtimestamp(timestamp).strftime(pattern)


def str2pinyin(hans, style=pypinyin.FIRST_LETTER):
    """�ַ���תƴ����Ĭ��ֻ��ȡ����ĸ
    """
    pinyin_str = pypinyin.slug(hans, style=style, separator="")
    num = 2
    while pinyin_str in _pinyin_names:
        pinyin_str += str(num)
        num += 1
    return pinyin_str


def dump_index():
    """�־û�������Ϣ
    """
    dat = shelve.open(INDEX_DAT)
    dat["article_index"] = ARTICLE_INDEX
    dat["article_rank"] = ARTICLE_RANK
    dat["tag_inverted_index"] = TAG_INVERTED_INDEX
    dat["author_inverted_index"] = AUTHOR_INVERTED_INDEX
    dat.close()


def index_tags(tags, fid):
    """Ϊ��ǩ����������ӱ�ǩ
    """
    for tag in tags:
        if tag in TAG_INVERTED_INDEX:
            TAG_INVERTED_INDEX[tag].append(fid)
        else:
            TAG_INVERTED_INDEX[tag] = [fid]


def index_rank(rank, fid):
    rank = int(rank[0])
    ARTICLE_RANK[fid] = rank
    
def index_authors(authors, fid):
    """Ϊ���ߵ��������������
    """
    for author in authors:
        if author in AUTHOR_INVERTED_INDEX:
            AUTHOR_INVERTED_INDEX[author].append(fid)
        else:
            AUTHOR_INVERTED_INDEX[author] = [fid]


def create_index(filename, meta):
    """����������Ϣ
    :param filename: �ļ���INPUT_CONTENT��ʼ��ȫ·��
    :param meta:
    :type meta: dict
    :return:
    """

    filename = codecs.decode(filename, "gb2312")

    index_tags(meta.get("tags", []), _current_file_index)
    index_authors(meta.get("authors", []), _current_file_index)
    index_rank(meta.get("rank", [0]), _current_file_index)

    title = meta.get("title", [""])[0]
    if title == "":
        title = os.path.splitext(os.path.basename(filename))[0]

    publish_dates = meta.get("publish_date", [])
    if len(publish_dates) == 0:
        publish_date = parse_time(os.path.getctime(filename), "%Y-%m-%d")
    else:
        publish_date = publish_dates[0]

    ARTICLE_INDEX[_current_file_index] = {
        "filename": filename,
        "modify_time": parse_time(os.path.getmtime(filename)),
        "title": title,
        "summary": meta.get("summary", [u""])[0],
        "authors": meta.get("authors", [u"����"]),
        "publish_date": publish_date,
        "tags": meta.get("tags", []),
        "rank": meta.get("rank", 0)
    }


def get_out_dir(md_file):
    """��ȡmd�ļ������·��
    :param md_file:
    :return:
    """

    return os.path.join(OUTPUT_CONTENT, _current_file_index + ".html")


def save_html(out_path, html):
    """����html���ļ�
    :param out_path:
    :param html:
    :return:
    """
    base_folder = os.path.dirname(out_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    with codecs.open(out_path, "w+", "utf-8") as f:
        f.write(html)


def render_tags_html(tags):
    """��Ⱦtags��html
    """
    tags_html = ""
    for tag in tags:
        tags_html += TAG_HTML_TEMPLATE.format(tag=tag)
    return tags_html


def render_authors_html(authors):
    """��Ⱦ����html
    """
    authors_html = ""
    for author in authors:
        authors_html += AUTHOR_HTML_TEMPLATE.format(author=author)
    return authors_html


def render_title_html(title):
    """��Ⱦ����html
    """
    title_html = ""
    if title.strip() != "":
        title_html = TITLE_HTML_TEMPLATE.format(title_str=title)
    return title_html


def render(md_file):
    """��Ⱦhtmlҳ��
    :param md_file:
    :return:
    """
    with codecs.open(md_file, "r", "utf-8") as f:
        text = f.read()
        md = Markdown(
            extensions=[
                #"fenced_code",
                "pymdownx.details",     # �����ص�ģ��
                "pymdownx.mark",        # ����
                "pymdownx.b64",         # ʹ�ñ���ͼƬ
                "pymdownx.superfences", # ����ͼ��ʱ��ͼ
                "codehilite(css_class=highlight,linenums=None)",
                "meta",
                "admonition",
                "tables",
                "toc(baselevel=1,title=Catalogue)",
                "wikilinks",
            ],
        )
        html = md.convert(text)
        meta = md.Meta if hasattr(md, "Meta") else {}
        toc = md.toc if hasattr(md, "toc") else ""
        create_index(md_file, meta)

        template = env.get_template("base_article.html")
        text = template.render(
            blog_content=html,
            static_root=STATIC_ROOT,
            title=ARTICLE_INDEX[_current_file_index].get("title"),
            title_html=render_title_html(ARTICLE_INDEX[_current_file_index].get("title")),
            summary=ARTICLE_INDEX[_current_file_index].get("summary", ""),
            authors=render_authors_html(ARTICLE_INDEX[_current_file_index].get("authors")),
            tags=render_tags_html(ARTICLE_INDEX[_current_file_index].get("tags")),
            toc=toc,
            rank=ARTICLE_INDEX[_current_file_index].get("rank"),
        )

    return text


def gen(md_file_path):
    """��markdown����html�ļ�
    :param md_file_path:
    """
    out_path = get_out_dir(md_file_path)
    html = render(md_file_path)
    save_html(out_path, html)


def scan_md():
    """ɨ��md�ļ�
    """
    global _current_file_index
    for f in _MD_FILES:
        file_base_name = os.path.splitext(os.path.basename(f))[0]
        _current_file_index = str2pinyin(
            codecs.decode(file_base_name, "gb18030", "ignore")
        )
        _pinyin_names.add(_current_file_index)
        gen(f)


def load_md_files(folder):
    """��ָ���ļ�������Markdown�ļ�
    """
    global _MD_FILES
    for root, dirs, files in os.walk(folder):
        for f in files:
            if os.path.splitext(f)[1].lower() == ".md":
                _MD_FILES.append(os.path.join(root, f))


def generate():
    _reload_global()
    clean()

    load_md_files(INPUT_CONTENT)
    scan_md()
    dump_index()
    pass


if __name__ == "__main__":
    generate()
    pass

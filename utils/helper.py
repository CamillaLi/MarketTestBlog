#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""
import shelve

from settings import INDEX_DAT


class IndexData(object):
    """索引数据类
    """

    _data = {}

    @classmethod
    def _load_data(cls):
        """载入数据
        """
        dat = shelve.open(INDEX_DAT)
        for k in dat:
            cls._data[k] = dat[k]
        return cls._data

    @classmethod
    def get_index_data(cls):
        """获取索引信息
        """
        if len(cls._data) == 0:
            cls._load_data()
        return cls._data

    @classmethod
    def reload_index_data(cls):
        """重载数据信息
        """
        cls._load_data()
        
    @classmethod
    def get_top_article(cls):
        all_articles_rank = IndexData.get_index_data().get("article_rank")
        top_articles_index = []
        for (index, rank) in all_articles_rank.items():
            if rank == 999:
                top_articles_index.append(index)
        ret = {}
        all_articles = IndexData.get_index_data().get("article_index")
        for index in top_articles_index:
            ret[index] = all_articles[index]
        return ret

if __name__ == "__main__":
    pass

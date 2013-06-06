#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import __builtin__ 
from StringIO import StringIO
import unittest
from mock import Mock, patch, MagicMock, mock_open

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), 
                                               '../') ))
import make_loaddata

class TestMakeLoaddata(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal(self):
        # そのまま
        args = MagicMock(source='normal.csv')
        output = make_loaddata.merge_separated_line(args).next()
        self.assertEqual(output,
                         [u"01101", u"060  ", u"0600041", u"ホッカイドウ",
                          u"サッポロシチュウオウク", u"オオドオリヒガシ",
                          u"北海道", u"札幌市中央区", u"大通東",
                          u"0", u"0", u"1", u"0", u"0", u"0"])

    def test_dup(self):
        # 連結
        args = MagicMock(source='dup.csv')
        output = make_loaddata.merge_separated_line(args).next()
        self.assertEqual(output,
                         [u"01230", u"059  ", u"0590005", u"ホッカイドウ",
                          u"ノボリベツシ", 
                          u"サツナイチョウ(5、9、11-12、36、42-2、62、80、95、184、231、389-2、499、500バンチ)",
                          u"北海道", u"登別市", 
                          u"札内町（５、９、１１−１２、３６、４２−２、６２、８０、９５、１８４、２３１、３８９−２、４９９、５００番地）",
                          u"1", u"0", u"0", u"0", u"0", u"0"])

# ○○町、○○町、○○町


# ○○町１丁目、２丁目、３丁目


    def test_series(self):
        # ○○町１〜３丁目
        args = MagicMock(source='series.csv')
        output = make_loaddata.merge_separated_line(args).next()
        self.assertEqual(output,
                         [[u"03366", u"02955", u"0295521", u"イワテケン",
                           u"ワガグンニシワガマチ", u"コツナギザワ54チワリ", 
                           u"岩手県", u"和賀郡西和賀町", u"小繋沢５４地割",
                           u"0", u"0", u"0", u"1", u"0", u"0"],
                          [u"03366", u"02955", u"0295521", u"イワテケン",
                           u"ワガグンニシワガマチ", u"コツナギザワ55チワリ", 
                           u"岩手県", u"和賀郡西和賀町", u"小繋沢５５地割",
                           u"0", u"0", u"0", u"1", u"0", u"0"],
                          [u"03366", u"02955", u"0295521", u"イワテケン",
                           u"ワガグンニシワガマチ", u"コツナギザワ56チワリ", 
                           u"岩手県", u"和賀郡西和賀町", u"小繋沢５６地割",
                           u"0", u"0", u"0", u"1", u"0", u"0"]])

    def test_parentheses(self):
        # ○○町（○○、○○）
        args = MagicMock(source='series.csv')
        output = make_loaddata.merge_separated_line(args).next()
        self.assertEqual(output,
                         [[u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマイイボシ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山飯干", 
                           u"1", u"0", u"0", u"0", u"0", u"0"],
                          [u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマオバライ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山小原井", 
                           u"1", u"0", u"0", u"0", u"0", u"0"],
                          [u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマカワウチ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山川内", 
                           u"1", u"0", u"0", u"0", u"0", u"0"],
                          [u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマタテイワ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山立岩", 
                           u"1", u"0", u"0", u"0", u"0", u"0"],
                          [u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマハエノヒラ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山八重の平", 
                           u"1", u"0", u"0", u"0", u"0", u"0"],
                          [u"45429", u"88314", u"8831402", u"ミヤザキケン",
                           u"ヒガシウスキグンモロツカソン", u"ナナツヤマホンムラ",
                           u"宮崎県", u"東臼杵郡諸塚村", u"七ツ山本村", 
                           u"1", u"0", u"0", u"0", u"0", u"0"]])

if __name__ == '__main__':
    unittest.main()


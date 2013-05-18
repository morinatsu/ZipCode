#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
zipcode : returns Japanese zipcode or address

"""
import re
import json
import logging
import webapp2
from zip_models import AreaCode, NetCode
from gaejson import GaeJson


class FromZip(webapp2.RequestHandler):
    """ return zipcode data from zipcode. """

    def get(self):
        def validate_zipcode(code):
            validated_code = re.match(r'^\d{3}-?\d{4}$', code)
            return validated_code.group(0)

        def is_net(code):
            if code[3:] == '0000':
                return True
            else:
                return False

        self.response.headers['content-type'] = \
            'application/json;charset=UTF-8'
        zipcode = validate_zipcode(self.request.get("code"))
        if zipcode:
            if is_net(zipcode):
                netcode = NetCode()
                query = netcode.gql("WHERE zipcode = :zipcode",
                                    zipcode=zipcode)
            else:
                areacode = AreaCode()
                query = areacode.gql("WHERE zipcode = :zipcode",
                                     zipcode=zipcode)
            json.dump(query, self.response.out,
                      ensure_ascii=False, cls=GaeJson)


class FromAdr(webapp2.RequestHandler):
    """ return zipcode data from address. """

    def get(self):
        def like_filter(query, street):
            for entity in query:
                logging.DEBUG('%s == %s' % (entity.street, street)
                if entity.street == street[:len(entity.street)]:
                    yield entity

        self.response.headers['content-type'] = \
            'application/json;charset=UTF-8'
        prefecture = self.request.get("pref")
        municipality = self.request.get("muni")
        street = self.request.get("street")
        areacode = AreaCode()
        query = areacode.gql(
            """WHERE prefecture__kanji = :prefecture
                 AND municipality_kanji = :municipality""",
            prefecture=prefecture, municipality=municipality)
        if query:
            json.dump(like_filter(query, street), self.response.out,
                      ensure_ascii=False, cls=GaeJson)
            return
        netcode = NetCode()
        query = netcode.gql(
            """WHERE prefecture__kanji = :prefecture
                 AND municipality_kanji = :municipality""",
            prefecture=prefecture, municipality=municipality)
        if query:
            json.dump(like_filter(query, street), self.response.out,
                      ensure_ascii=False, cls=GaeJson)


class MkDummy(webapp2.RequestHandler):
    """ return zipcode data from address. """

    def get(self):
        area = AreaCode()
        area.local_government_code = u"01101"
        area.old_zipcode = u"060  "
        area.zipcode = u"9999999"
        area.prefecture_kana = u"ホッカイドウ"
        area.municipality_kana = u"サッポロシチュウオウク"
        area.street_kana = u"イカニケイサイガナイバアイ"
        area.prefecture_kanji = u"北海道"
        area.municipality_kanji = u"札幌市中央区"
        area.street_kanji = u"以下に掲載がない場合"
        area.street_has_plural_code = u"0"
        area.street_has_code_by_section = u"0"
        area.has_chome = u"0"
        area.zipcode_shared_by_plural_street = u"0"
        area.is_modified = u"0"
        area.reason_of_modify = u"0"
        area.put()


app = webapp2.WSGIApplication(
    [("/fromzip.*", FromZip), ("/fromadr.*", FromAdr), ("/test.*", MkDummy)],
    debug=True)

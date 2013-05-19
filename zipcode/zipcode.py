#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
zipcode : returns Japanese zipcode or address

"""
import re
from flask import Flask, request, json, g, Response, abort
import sqlite3

app = Flask(__name__)
app.config.from_object('config')


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/zip2adr')
def zip2adr():
    """ return zipcode data from zipcode. """

    def validate_zipcode(code):
        validated_code = re.match(r'^(\d{3})-?(\d{4})$', code)
        if validated_code is None:
            app.logger.error('invalid zipcode: %s', code)
            abort(400)
        app.logger.info('valid zipcode: %s', code)
        return validated_code.group(1) + validated_code.group(2)

    def is_net(code):
        if code[5:] == '00':
            return True
        else:
            return False

    zipcode = validate_zipcode(request.args.get('code', ''))
    if zipcode:
        if is_net(zipcode):
            cur = g.db.execute('select * from netcode where zipcode=?',
                               (zipcode, ))
        else:
            cur = g.db.execute('select * from areacode where zipcode=?',
                               (zipcode, ))
        entries = [dict(row) for row in cur.fetchall()]
    else:
        entries = []
    return Response(json.dumps(entries, ensure_ascii=False),
                    mimetype='application/json; charset=utf-8')


@app.route('/adr2zip')
def adr2zip():
    """ return zipcode data from address. """

    def like_filter(entries, street):
        for entry in entries:
            compare_length = min(len(street), len(entry['street_kanji']))
            app.logger.info('compare: %s == %s',
                            street[:compare_length],
                            entry['street_kanji'][:compare_length])
            if (street[:compare_length] ==
                    entry['street_kanji'][:compare_length]):
                yield entry

    prefecture = request.args.get('pref', '')
    municipality = request.args.get('muni', '')
    street = request.args.get('street', '')
    if prefecture == '' or municipality == '' or street == '':
        abort(400)
    cur = g.db.execute(
        '''select *
             from areacode
            where prefecture_kanji = ?
              and municipality_kanji = ?''',
        (prefecture, municipality))
    entries = [dict(row) for row in cur.fetchall()]
    matched_entries = list(like_filter(entries, street))
    if len(matched_entries) > 0:
        return Response(json.dumps(
            matched_entries,
            ensure_ascii=False),
            mimetype='application/json; charset=utf-8')
    cur = g.db.execute(
        '''select *
             from netcode
            where prefecture_kanji = ?
              and municipality_kanji = ?''',
        (prefecture, municipality))
    entries = [dict(row) for row in cur.fetchall()]
    return Response(json.dumps(
        entries,
        ensure_ascii=False),
        mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run()

#!/usr/bin/env python3

import sys
import json
from urllib.request import Request, urlopen
from pathlib import Path
from configparser import ConfigParser

def dadata_cli():
    '''
    Parses arguments, passes them to a relevant class,
    calls fine_print method of a class to provide output
    '''
    query = ""
    if len(sys.argv) > 3:
        for arg in sys.argv[3:]:
            query = query + arg + " "
        if sys.argv[1] == "suggest":
            if sys.argv[2] == "address":
                ob = Address(query)
                ob.fine_print()
            elif sys.argv[2] == "party":
                ob = Party(query)
                ob.fine_print()
            elif sys.argv[2] == "bank":
                ob = Bank(query)
                ob.fine_print()
            elif sys.argv[2] == "fio":
                ob = Fio(query)
                ob.fine_print()
            elif sys.argv[2] == "email":
                ob = Email(query)
                ob.fine_print()
            elif sys.argv[2] == "fias":
                ob = Fias(query)
                ob.fine_print()
            elif sys.argv[2] == "fms-unit":
                ob = FmsUnit(query)
                ob.fine_print()
            elif sys.argv[2] == "postal-unit":
                ob = PostalUnit(query)
                ob.fine_print()
            elif sys.argv[2] == "fns-unit":
                ob = FnsUnit(query)
                ob.fine_print()
            elif sys.argv[2] == "region-court":
                ob = RegionCourt(query)
                ob.fine_print()
            elif sys.argv[2] == "metro":
                ob = Metro(query)
                ob.fine_print()
            elif sys.argv[2] == "country":
                ob = Country(query)
                ob.fine_print()
            elif sys.argv[2] == "currency":
                ob = Currency(query)
                ob.fine_print()
            elif sys.argv[2] == "okved2":
                ob = Okved2(query)
                ob.fine_print()
            else:
                Dadata.usage()
        else:
            Dadata.usage()
    else:
        Dadata.usage()

class Dadata():
    '''
    Parent class, contains common variables and functions
    '''
    config_path = "".join( ( str(Path(__file__).parent), "/config" ) )
    config = ConfigParser()
    config.read(config_path)
    key = config.get("common", "key")
    headers = {"Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token {}".format(key)}
    root_url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/"

    def validate(dict, *args):
        try:
            if len(args) == 1:
                return dict[args[0]]
            if len(args) == 2:
                return dict[args[0]][args[1]]
            if len(args) == 3:
                return dict[args[0]][args[1]][args[2]]
        except AttributeError:
            return None
        except TypeError:
            return None
        except KeyError:
            return None

    def usage():
        print('''
    Usage:
    ./dadata.py suggest {}api_method query_text{}
    API methods are found at: https://dadata.ru/api/suggest/
    Note: for best usability, underscore in API method names is replaced with dash ( '-' ) in dadata-cli (see Examples)
    Query text is passed to API as is
    '''.format("\x1b[3m","\x1b[0m"),
    '''
    Examples:
    ./dadata.py suggest address Ленина 29
    ./dadata.py suggest party Гугл Москва
    ./dadata.py suggest postal-unit Ленина 29
        ''')

class Suggestions(Dadata):
    '''
    Parent class, contains common variables and functions
    .getdata returns a dictionary on success, string on failure
    '''
    base_url = Dadata.root_url + "suggest/"

    def __init__(self, query):
        self.query = query
        self.data = '{ "query": "'+query+'", "count": 20 }'

    def getdata(self, api_url):
        request = Request(api_url, self.data.encode("utf-8"),
            super().headers)
        try:
            reply = json.loads(urlopen(request).read().decode())
            return reply
        except OSError as e:
            return str(e)
        except json.decoder.JSONDecodeError as e:
            return "JSONDecodeError, probably HTTP error"

class Address(Suggestions):
    api_url = Suggestions.base_url + "address"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}"
                    .format(Dadata.validate(value["data"], "country"),
                    Dadata.validate(value["data"], "postal_code"),
                    value["value"]))
        except TypeError:
            print(super().getdata(self.api_url))

class Party(Suggestions):
    api_url = Suggestions.base_url + "party"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}    {!s:}    {!s:}"
                    .format(Dadata.validate(value["data"], "inn"),
                    Dadata.validate(value["data"], "okved"),
                    value["value"],
                    Dadata.validate(value["data"], "address", "value"),
                    Dadata.validate(value["data"], "management", "name"),
                    Dadata.validate(value["data"], "state", "status")))
        except TypeError:
            print(super().getdata(self.api_url))

class Bank(Suggestions):
    api_url = Suggestions.base_url + "bank"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}    {!s:}"
                    .format(Dadata.validate(value["data"], "inn"),
                    Dadata.validate(value["data"], "kpp"),
                    value["value"],
                    Dadata.validate(value["data"], "address", "value"),
                    Dadata.validate(value["data"], "state", "status")))
        except TypeError:
            print(super().getdata(self.api_url))

class Fio(Suggestions):
    api_url = Suggestions.base_url + "fio"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}"
                    .format(Dadata.validate(value["data"], "surname"),
                    Dadata.validate(value["data"], "name"),
                    Dadata.validate(value["data"], "patronymic"),
                    Dadata.validate(value["data"], "gender")))
        except TypeError:
            print(super().getdata(self.api_url))

class Email(Suggestions):
    api_url = Suggestions.base_url + "email"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "local"),
                    Dadata.validate(value["data"], "domain")))
        except TypeError:
            print(super().getdata(self.api_url))

class Fias(Address):
    api_url = Suggestions.base_url + "fias"

class FmsUnit(Suggestions):
    api_url = Suggestions.base_url + "fms_unit"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "code")))
        except TypeError:
            print(super().getdata(self.api_url))

class PostalUnit(Suggestions):
    api_url = Suggestions.base_url + "postal_unit"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}    {!s:}    {!s:}"
                    "{!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "address_str"),
                    Dadata.validate(value["data"], "schedule_mon"),
                    Dadata.validate(value["data"], "schedule_tue"),
                    Dadata.validate(value["data"], "schedule_wed"),
                    Dadata.validate(value["data"], "schedule_thu"),
                    Dadata.validate(value["data"], "schedule_fri"),
                    Dadata.validate(value["data"], "schedule_sat"),
                    Dadata.validate(value["data"], "schedule_sun")))
        except TypeError:
            print(super().getdata(self.api_url))

class FnsUnit(Suggestions):
    api_url = Suggestions.base_url + "fns_unit"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "address"),
                    Dadata.validate(value["data"], "comment"),
                    Dadata.validate(value["data"], "phone")))
        except TypeError:
            print(super().getdata(self.api_url))

class RegionCourt(Suggestions):
    api_url = Suggestions.base_url + "region_court"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "name")))
        except TypeError:
            print(super().getdata(self.api_url))

class Metro(Suggestions):
    api_url = Suggestions.base_url + "metro"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "city"),
                    Dadata.validate(value["data"], "line_name")))
        except TypeError:
            print(super().getdata(self.api_url))

class Country(Suggestions):
    api_url = Suggestions.base_url + "country"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "name"),
                    Dadata.validate(value["data"], "code"),
                    Dadata.validate(value["data"], "alfa2"),
                    Dadata.validate(value["data"], "alfa3")))
        except TypeError:
            print(super().getdata(self.api_url))

class Currency(Suggestions):
    api_url = Suggestions.base_url + "currency"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}    {!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "code"),
                    Dadata.validate(value["data"], "strcode"),
                    Dadata.validate(value["data"], "country")))
        except TypeError:
            print(super().getdata(self.api_url))

class Okved2(Suggestions):
    api_url = Suggestions.base_url + "okved2"

    def fine_print(self):
        try:
            for value in super().getdata(self.api_url)["suggestions"]:
                print("{!s:}    {!s:}"
                    .format(value["value"],
                    Dadata.validate(value["data"], "idx")))
        except TypeError:
            print(super().getdata(self.api_url))

if __name__ == "__main__":
    dadata_cli()

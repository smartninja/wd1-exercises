# -*- coding: utf-8 -*-
import datetime
from sqlite3 import OperationalError
import json


class Key:
    get_id = 221424253532525

    def __init__(self):
        self.get_id = 2384723532570237

    @classmethod
    def id(cls):
        return cls.get_id


class Model:
    def __init__(self, **kwargs):
        for attr in kwargs:
            setattr(self, attr, kwargs.get(attr))

        self.key = Key

    @classmethod
    def query(cls, *args, **kwargs):
        return cls

    @classmethod
    def fetch(cls):
        table_name = cls.__name__

        # connect to the SQLite database
        conn, cursor = cls._connect_db()
        conn.text_factory = str

        try:
            fetch_all = "select * from {0}".format(table_name)
            cursor.execute(fetch_all)

            result = cls._parse_sqlite_result(cursor)
        except OperationalError:
            result = []

        conn.commit()
        conn.close()

        return result

    def put(self):
        table_name = self.__class__.__name__
        table_fields = {}

        for key in self.__class__.__dict__:
            if not key.startswith("_") and not key.startswith("key"):
                table_fields[key] = getattr(self, key)

        # connect to the SQLite database
        conn, cursor = self._connect_db()

        # create a table
        table_fields_str = str(table_fields.keys()).replace("[", "").replace("]", "").replace("'", "")
        try:
            create_table = "create table {0}({1})".format(table_name, table_fields_str)
            print create_table
            cursor.execute(create_table)
        except OperationalError:
            print "table already exists"

        # needed in order to convert __repr__ default data of type instance into string
        values = []
        for val in table_fields.values():
            values.append(unicode(val).encode("utf-8"))

        # insert object data into the table
        values_str = json.dumps(values, ensure_ascii=False).replace("[", "").replace("]", "")  # json.dumps needed to remove unicode u'
        insert_into = "insert into {0}({1}) values ({2})".format(table_name, table_fields_str, values_str)
        print insert_into

        try:
            cursor.execute(insert_into)
        except Exception as e:
            # a column might be missing
            last_word = e.message.split()[-1]
            print "This column is missing from the database: " + str(last_word) + ". Adding this column to the table now."
            if last_word in table_fields.keys():
                alter_table = "alter table {0} add column {1}".format(table_name, last_word)
                cursor.execute(alter_table)
                cursor.execute(insert_into)

        print "saved into the database"

        conn.commit()
        conn.close()

        return self

    @staticmethod
    def _connect_db():
        # prepare the SQLite database
        import sqlite3
        print "connect the localhost SQLite database"
        conn = sqlite3.connect('localhost.db', detect_types=sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()

        return conn, cursor

    @staticmethod
    def _parse_sqlite_result(cursor):
        fetch_all = cursor.fetchall()
        description = cursor.description

        fields = []
        for row in description:
            for item in row:
                if item:
                    fields.append(item)

        result = []
        for id, row in enumerate(fetch_all):
            row_dict = {}

            for i, item in enumerate(row):
                if type(item) is str:
                    if str(item).startswith("datetime"):
                        item = datetime.datetime.strptime(item.replace("datetime.datetime(", "").replace(")", ""),
                                                          '%Y, %m, %d, %H, %M, %S, %f')
                    else:
                        item = unicode(item, "utf8")
                row_dict[fields[i]] = item

            row_dict["get_id"] = id

            result.append(row_dict)

        return result

    @staticmethod
    def to_serializable(val):
        if isinstance(val, datetime.datetime):
            return val.strftime('%d %B %Y at %H:%M')
        elif isinstance(val, Exception):
            return {
                "error": val.__class__.__name__,
                "args": val.args,
            }

        return unicode(val).encode("utf-8")


class TextProperty:
    def __init__(self, default=None):
        if default and isinstance(default, str):
            self.value = default
        else:
            self.value = None

    def __repr__(self):
        return repr(self.value)


class StringProperty:
    def __init__(self, default=None):
        if default and isinstance(default, str):
            self.value = default
        else:
            self.value = None

    def __repr__(self):
        return repr(self.value)


class IntegerProperty:
    def __init__(self, default=None):
        if default and isinstance(default, int):
            self.value = default
        else:
            self.value = 0

    def __repr__(self):
        return repr(self.value)


class FloatProperty:
    def __init__(self, default=None):
        if default and isinstance(default, float):
            self.value = default
        else:
            self.value = 0.0

    def __repr__(self):
        return repr(self.value)


class BooleanProperty:
    def __init__(self, default=None):
        if default and isinstance(default, bool):
            self.value = default
        else:
            self.value = False

    def __repr__(self):
        return repr(self.value)


class DateTimeProperty:
    def __init__(self, auto_now_add=True):
        if auto_now_add and isinstance(auto_now_add, bool):
            self.value = datetime.datetime.now()
        else:
            self.value = None

    def __repr__(self):
        return repr(self.value)

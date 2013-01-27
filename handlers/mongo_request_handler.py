"""
MongoDb Request Handler
This module defines a request handler that can be shared(inherited) across other handlers.
Specifically handlers which make MongoDb queries and return results as json.
"""

import logging
import tornado.web
import pymongo
import json

from bson.objectid import ObjectId

import config

class MongoRequestHandler(tornado.web.RequestHandler):
    """handles requests which return results from MongoDb"""

    @property
    def db(self):
        """db property for pymongo pointing to datastore 'core'"""
        if not hasattr(self, '_db'):
            self._db = pymongo.Connection(config.MONGO_IP, config.MONGO_PORT).planning_poker
        return self._db

    def prepare(self):
        """
        Request body is loaded as json data. Except for in case of GET, DELETE & OPTIONS.
        """

        self.add_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')

        if not self.request.method in ['GET', 'OPTIONS', 'DELETE']:
            if 'application/json' in self.request.headers.get('Content-Type', 'unknown'):
                self.data = json.loads(self.request.body)
            else:
                logging.error("application/json not in Content-Type")
                raise tornado.web.HTTPError(400)

    def _write_json(self, obj):
        """
        obj can be cursor or a python dict.
        Firstly walks through a cursor returned from MongoDb.
        Secondly filters out '_id' attribute from response_data.
        Finally serializes response into json and completes the HTTP request.
        """

        response = {}
        if isinstance(obj, pymongo.cursor.Cursor):
            records = []
            for record in obj:
                logging.info(record)
                record = self.rename_key(record, '_id', 'id')
                records.append(record)
            response = records
        else:
            record = self.rename_key(obj, '_id', 'id')
            response = record

        self.write(json.dumps(response, default=self.bson_serializer))
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.finish()

    def rename_key(self, obj, from_key, to_key):
        """
        swaps the value at 'from_key' to 'to_key' and deletes 'from_key'.
        Returns the updated dict, Hence has side-effects.
        """

        if from_key in obj:
            obj[to_key] = obj[from_key]
            del obj[from_key]
        return obj


    def bson_serializer(self, obj):
        """serializes bson object to string"""

        if isinstance(obj, ObjectId):
            return str(obj)
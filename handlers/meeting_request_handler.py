import logging
import tornado.web
import pymongo
import json
import urllib
from bson.objectid import ObjectId

from handlers.mongo_request_handler import MongoRequestHandler
import config

class MeetingRequestHandler(MongoRequestHandler):

    @tornado.web.asynchronous
    def get(self, meeting_id=None):
        print meeting_id
        self.write("Hello, world")
        self.finish()

    @tornado.web.asynchronous
    def post(self, meeting_id=None):
        """handles http post requests"""
        self.data['user_agent'] = self.request.headers.get('User-Agent', 'unknown')
        self.data['remote_ip'] = self.request.remote_ip
        print self.data
        meeting_id = self.db.meeting.insert(self.data, safe=True)
        meeting = self.db.meeting.find_one({"_id": meeting_id})
        self._write_json(meeting)
        print meeting
        self.finish()
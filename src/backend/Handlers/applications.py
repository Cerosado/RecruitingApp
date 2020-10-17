import json
from flask import jsonify
from DAO.applicationsDAO import ApplicationsDao


class ApplicationsHandler:

    def map_to_Application(self, row):
        result = {}
        result['user_id'] = row[0]
        result['posting_id'] = row[1]
        return result

    def getApplicationByJobPostingId(self, uid):
        dao = ApplicationsDao()
        result = dao.getApplicationsByPosting(uid)
        result = self.map_to_Application(result)
        return jsonify(result)

    def getApplicationByUserId(self, uid, name):
        dao = ApplicationsDao()
        result = dao.getApplicationsByUser(uid)
        result = self.map_to_Application(result)
        return jsonify(result)

    def getApplication(self, uid, pid):
        dao = ApplicationsDao()
        result = dao.getApplication(uid, pid)
        result = self.map_to_Application(result)
        return jsonify(result)

    def createApplication(self, data):
        user_id = data['user_id']
        posting_id = data['posting_id']
        dao = ApplicationsDao()
        id = dao.registerApplication(user_id, posting_id)
        return jsonify(Appplicationid=id)

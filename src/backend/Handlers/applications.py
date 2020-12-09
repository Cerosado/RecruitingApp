from flask import jsonify
from ..DAO.applicationsDAO import ApplicationsDao
from ..DAO.resumeDAO import ResumeDao
from ..DAO.modelsDAO import ModelsDAO
import joblib
from ..Handlers.resume import ResumeHandler


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

    def createApplication(self, user_id, posting_id):
        resume_dao = ResumeDao()
        parsed_resume = resume_dao.get_resume_ranking_parameters(user_id)
        rank = ResumeHandler.rank_resume(parsed_resume, posting_id)
        dao = ApplicationsDao()
        application_id = dao.registerApplication(user_id, posting_id, rank)
        return jsonify(Appplicationid=application_id)

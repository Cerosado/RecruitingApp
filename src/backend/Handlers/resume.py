from flask import jsonify
from src.backend.DAO.resumeDAO import ResumeDao


class ResumeHandler:

    def map_to_Resume(self, row):
        result = {}
        result['resume_data'] = row[0]
        result['resume_extension'] = row[1]
        result['last_updated'] = row[2]
        result['user_id'] = row[2]
        return result

    def getResumeByUserId(self, uid):
        dao = ResumeDao()
        result = dao.getResumeById(uid)
        result = self.map_to_Resume(result)
        return jsonify(result)

    def createResume(self, data):
        resume_data = data['resume_data']
        resume_extension = data['resume_extension']
        last_updated = data['last_updated']
        user_id = data['user_id']
        dao = ResumeDao()
        result = dao.registerResume(resume_data, resume_extension, last_updated, user_id)
        result = self.map_to_Resume(result)
        return jsonify(result)

    def editResume(self, data):
        resume_data = data['resume_data']
        resume_extension = data['resume_extension']
        last_updated = data['last_updated']
        user_id = data['user_id']
        dao = ResumeDao()
        result = dao.editResume(resume_data, resume_extension, last_updated, user_id)
        result = self.map_to_Resume(result)
        return jsonify(result)


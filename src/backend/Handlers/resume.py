import json
from flask import jsonify
from DAO.resumeDAO import ResumeDao


class ResumeHandler:

    def map_to_Resume(self, row):
        result={}
        result['resume_data']=row[0]
        result['resume_extension']=row[1]
        result['education']=row[2]
        result['college_name']=row[3]
        result['degree']=row[4]
        result['designation']=row[5]
        result['experience']=row[6]
        result['company_names']=row[7]
        result['skills']=row[8]
        result['total_experience']=row[9]
        result['last_updated']=row[10]
        result['user_id']=row[11]
        return result

    def getResumeByUserId(self, uid):
        dao = ResumeDao()
        result = dao.getResumeById(uid)
        result = self.map_to_Resume(result)
        return jsonify(result)

    #Create resume, must provide all data.
    def createResume(self, data): 
        resume_data = data['resume_data']
        resume_extension = data['resume_extension']
        education = data['education']
        college_name = data['college_name']
        degree = data['degree']
        designation = data['designation']
        experience = data['experience']
        company_names = data['company_names']
        skills = data['skills']
        total_experience = data['total_experience']
        last_updated = data['last_updated']
        user_id = data['user_id']
        dao = ResumeDao()
        result = dao.registerResume(resume_data, resume_extension, education, college_name, degree, designation, experience, company_names, skills, total_experience, last_updated, user_id)
        result = self.map_to_Resume(result)
        return jsonify(result)

    #Edit resume, data can have less than the amount of data needed. Defaults original data.
    def editResume(self, data):
        dao = ResumeDao()
        original = dao.getResumeByUserId(data['user_id'])
        for item in original:
            if (data.get(item)==None):
                data[item]=original[item]
        result = dao.editResume(data['resume_data'], data['resume_extension'], data['last_updated'], data['user_id'])
        result = self.map_to_Resume(result)
        return jsonify(result)


from datetime import datetime

from flask import jsonify
from src.backend.DAO.resumeDAO import ResumeDao
from src.resume_parser.custom_resume_parser import CustomResumeParser


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
        if len(data) != 12:
            return jsonify(Error="Malformed post request"), 400
        else:
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

    def parse_resume(self, file, skills_file=None):
        resume = CustomResumeParser(file, skills_file=skills_file).get_extracted_data()
        resume_data = file
        resume_extension = file.name.split('.')[1]
        education = resume['education']
        college_name = resume['college_name']
        degree = resume['degree']
        designation = resume['designation']
        experience = resume['experience']
        company_names = resume['company_names']
        skills = resume['skills']
        total_experience = resume['total_experience']
        last_updated = datetime.now()
        user_id = 1
        dao = ResumeDao()
        result = dao.registerResume(resume_data.read(), resume_extension, education, college_name, degree, designation,
                                    experience, company_names, skills, total_experience, last_updated, user_id)
        # result = self.map_to_Resume(result)
        return jsonify(user_id=result)


import inspect
import os
from datetime import datetime

import pandas
from flask import jsonify
from joblib import load

from ..DAO.applicationsDAO import ApplicationsDao
from ..DAO.resumeDAO import ResumeDao
from ..resume_parser.custom_resume_parser import CustomResumeParser


class ResumeHandler:

    def map_to_Resume(self, row):
        result = {}
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

    # Create resume, must provide all data.
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

    # Edit resume, data can have less than the amount of data needed. Defaults original data.
    def editResume(self, data):
        dao = ResumeDao()
        original = dao.getResumeByUserId(data['user_id'])
        for item in original:
            if (data.get(item)==None):
                data[item]=original[item]
        result = dao.editResume(data['resume_data'], data['resume_extension'], data['last_updated'], data['user_id'])
        result = self.map_to_Resume(result)
        return jsonify(result)

    def parse_and_rank_resume(self, file, skills_file=None):
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

        df = pandas.DataFrame.from_dict([resume])

        # Load ML model
        ranking_model = load('./resume_parser/ranking_model.joblib')

        # Load Vectorizer
        vect = load('./resume_parser/vectorizer.joblib')

        # Get skills column and transform with Vectorizer
        skills_col = df['skills'].map(lambda skills_list: str(skills_list))
        vect_data = vect.transform(skills_col)

        # Get predict probabilty of category 'Experienced'
        prob = ranking_model.predict_proba(vect_data)
        rank = int(prob[0, 1] * 100)

        resume_dao = ResumeDao()
        result = resume_dao.registerResume(
            resume_data.read(), resume_extension, education, college_name, degree, designation,
            experience, company_names, skills, total_experience, last_updated, user_id)

        # Call applications dao to create application to posting
        app_dao = ApplicationsDao()
        result_app = app_dao.registerApplication(user_id=user_id, posting_id=1, rank=rank)

        # TODO: Handle errors and rollback
        return jsonify(user_id=result)


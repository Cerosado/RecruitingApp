import copy
import inspect
import os
from datetime import datetime
from pathlib import Path
import sys

import pandas
from flask import jsonify
from joblib import load
import flask_praetorian

from ..DAO.applicationsDAO import ApplicationsDao
from ..DAO.resumeDAO import ResumeDao
from ..DAO.userDAO import UserDao
from ..DAO.modelsDAO import ModelsDAO
from ..resume_parser.custom_resume_parser import CustomResumeParser
from ..DAO.modelsDAO import ModelsDAO


class ResumeHandler:

    def map_to_Resume(self, row):
        result = {}
        result['resume_data']=row['resume_data']
        result['resume_extension']=row['resume_extension']
        result['education']=row['education']
        result['college_name']=row['college_name']
        result['degree']=row['degree']
        result['designation']=row['designation']
        result['experience']=row['experience']
        result['company_names']=row['company_names']
        result['skills']=row['skills']
        result['total_experience']=row['total_experience']
        result['last_updated']=row['last_updated']
        result['user_id']=row['user_id']
        return result

    def getResumeByUserId(self, uid):
        dao = ResumeDao()
        result = dao.getResumeById(uid)
        if(result):
            result = self.map_to_Resume(result)        
        return result
        
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

    def parse_resume(self, resume_file, resume_filename, skills_file=None):
        resume_file_copy = copy.deepcopy(resume_file)
        resume_file_copy.name = resume_filename
        resume = CustomResumeParser(resume_file_copy, skills_file=skills_file).get_extracted_data()
        resume_data = resume_file
        resume_extension = resume_filename.split('.')[1]

        user = flask_praetorian.current_user()
        user_id = user.identity

        education = resume['education']
        education_section = resume['education_section']
        college_name = resume['college_name']
        degree = resume['degree']
        designation = resume['designation']
        experience = resume['experience']
        company_names = resume['company_names']
        skills = resume['skills']
        total_experience = resume['total_experience']
        last_updated = datetime.now()

        resume_dao = ResumeDao()
        result = None
        currentResume = resume_dao.getResumeById(user.user_id)
        if(currentResume):
            result = resume_dao.editResume(
            resume_data.read(), resume_extension, education, college_name, degree, designation,
            experience, education_section, company_names, skills, total_experience, last_updated, user_id)
        else:
            result = resume_dao.registerResume(
            resume_data.read(), resume_extension, education, college_name, degree, designation,
            experience, education_section, company_names, skills, total_experience, last_updated, user_id)
        # TODO: Handle errors and rollback
        return jsonify(user_id=result)

    @staticmethod
    def rank_resume(resume_dict, posting_id):
        df = pandas.DataFrame.from_dict([resume_dict])[['skills', 'experience', 'education_section']]
        df.fillna('no_info')
        models_dao = ModelsDAO()
        model_info = models_dao.get_model_name(posting_id)
        base_path = Path(__file__).parent
        model_path = '../ranking_models/%s%s.pkl' % \
                     (model_info['model_name'], '' if model_info['use_education'] else '_no_edu',)
        file_path = (base_path / model_path).resolve()
        model_pipeline = load(file_path)
        prob = model_pipeline.predict_proba(df)
        rank = int(prob[0, 1] * 100)
        return rank





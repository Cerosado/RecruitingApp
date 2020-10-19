from flask import jsonify
from DAO.jobPostingsDAO import JobPostingsDao
import sys


class JobPostingHandler:

    def build_jobPosting_dict(self, row):
        result = {}
        result['position_name'] = row[0]
        result['location'] = row[1]
        result['description'] = row[2]
        result['key_details'] = row[3]
        result['pay_type'] = row[4]
        result['pay_amount'] = row[5]
        result['user_id'] = row[6]
        result['deadline'] = row[7]
        result['presentationDate'] = row[8]
        return result

    def build_jobPosting_attributes(self, position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline, presentationDate):
        result = {}
        result['position_name'] = position_name
        result['location'] = location
        result['description'] = description
        result['key_details'] = key_details
        result['pay_type'] = pay_type
        result['pay_amount'] = pay_amount
        result['user_id'] = user_id
        result['deadline'] = deadline
        result['presentationDate'] = presentationDate
        return result

    ###########################################
    #             GETS                        #
    ###########################################
    def getAllJobPostings(self):
        dao = JobPostingsDao()
        jobPostings_list = dao.getAllJobPostings()
        result_list = []
        for row in jobPostings_list:
            result = self.build_jobPosting_dict(row)
            result_list.append(result)
        return jsonify(JobPostings=result_list)

    def getJobPostingById(self, posting_id):
        dao = JobPostingsDao()
        result = dao.getJobPostingById(posting_id)
        result = self.build_jobPosting_dict(result)
        return jsonify(result)

    def getJobPostingsByUserId(self, user_id):
        dao = JobPostingsDao()
        result = dao.getJobPostingByUserId(user_id)
        result = self.build_jobPosting_dict(result)
        return jsonify(result)

    def getRankedApplicationsByJobPostingId(self, posting_id):
        dao = JobPostingsDao()
        result = dao.getRankedApplicationsByJobPostingId(posting_id)
        result = self.build_jobPosting_dict(result)
        return jsonify(result)

    ###########################################
    #             POST                        #
    ###########################################
    def createJobPosting(self, data):
        if len(data) != 1:
            return jsonify(Error="Malformed post request"), 400
        else:
            position_name = data['position_name']
            location = data['location']
            description = data['description']
            key_details = data['key_details']
            pay_type = data['pay_type']
            pay_amount = data['pay_amount']
            user_id = data['user_id']
            deadline = data['deadline']
            dao = JobPostingsDao()
            jid = dao.registerJobPosting(position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline)
            # result = self.build_chat_attributes(position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline)
            return jsonify(CreatedJobPosting=jid), 201

    def editJobPosting(self, data, posting_id):
        dao = JobPostingsDao()
        original = dao.getJobPostingById(posting_id)
        for item in original:
            if (data.get(item)==None):
                data[item]=original[item]
        result = dao.editJobPosting(data['position_name'], data['location'], data['description'], data['key_details'], data['pay_type'], data['pay_amount'], data['user_id'], data['deadline'])
        return jsonify(Result=result)

    # def deleteChat(self, data):
    #     dao = ChatsDAO()
    #     result = dao.deleteChat(data['uid'], data['cid'])
    #     return jsonify(Result=result)


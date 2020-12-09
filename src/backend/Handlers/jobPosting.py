import flask_praetorian
from flask import jsonify
from ..DAO.jobPostingsDAO import JobPostingsDao


class JobPostingHandler:

    # def build_jobPosting_dict(self, row):
    #     result = {}
    #     result['posting_id'] = row[0]
    #     result['position_name'] = row[1]
    #     result['location'] = row[2]
    #     result['description'] = row[3]
    #     result['key_details'] = row[4]
    #     result['pay_type'] = row[5]
    #     result['pay_amount'] = row[6]
    #     result['user_id'] = row[7]
    #     result['deadline'] = row[8]
    #     result['presentationDate'] = row[9]
    #     return result

    # def build_jobPosting_attributes(self, position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline, presentationDate):
    #     result = {}
    #     result['position_name'] = position_name
    #     result['location'] = location
    #     result['description'] = description
    #     result['key_details'] = key_details
    #     result['pay_type'] = pay_type
    #     result['pay_amount'] = pay_amount
    #     result['user_id'] = user_id
    #     result['deadline'] = deadline
    #     result['presentationDate'] = presentationDate
    #     return result

    ###########################################
    #             GETS                        #
    ###########################################
    def getAllJobPostings(self):
        dao = JobPostingsDao()
        jobPostings_list = dao.getAllJobPostings()
        result_list = []
        # for row in jobPostings_list:
        #     result = self.build_jobPosting_dict(row)
        #     result_list.append(result)
        return jsonify(jobPostings_list)

    def getJobPostingById(self, posting_id):
        dao = JobPostingsDao()
        result = dao.getJobPostingById(posting_id)
        # result = self.build_jobPosting_dict(result)
        return jsonify(result)

    def getJobPostingsByUserId(self, user_id):
        dao = JobPostingsDao()
        applicants_list = dao.getJobPostingByUserId(user_id)
        # result_list = []
        # for row in applicants_list:
        #     result = self.build_jobPosting_dict(row)
        #     result_list.append(result)
        return jsonify(applicants_list)

    def getRankedApplicationsByJobPostingId(self, posting_id):
        current_user = flask_praetorian.current_user()
        dao = JobPostingsDao()
        if current_user.identity != dao.get_recruiter_id(posting_id):
            return jsonify(Error="Access denied"), 403
        applicants_list = dao.getRankedApplicationsByJobPostingId(posting_id)
        posting_details = dao.getJobPostingById(posting_id)
        return jsonify(posting=posting_details, applicants=applicants_list)

    ###########################################
    #             POST                        #
    ###########################################
    def createJobPosting(self, data, user_id):
        if len(data) != 7:
            return jsonify(Error="Malformed post request"), 400
        else:
            position_name = data['positionName']
            location = data['location']
            description = data['description']
            key_details = data['keyDetails']
            pay_type = data['payType']
            pay_amount = data['payAmount']
            deadline = data['deadline']
            user_id = user_id
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


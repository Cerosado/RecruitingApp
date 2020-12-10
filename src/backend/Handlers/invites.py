import flask_praetorian
from flask import jsonify
from ..DAO.invitesDAO import InvitesDao


class InvitesHandler:
    invitesDao = InvitesDao()
    def getAllEventInvites(self, event_id):
        invites_list = invitesDao.getAllEventInvites(event_id)
        return invites_list
    def getAllRecruiterInvites(self, recruiter_id):
        invites_list = invitesDao.getAllRecruiterInvites(recruiter_id)
        return invites_list
    def getAllApplicantInvites(self,applicant_id):
        invites_list = invitesDao.getAllApplicantInvites(applicant_id)
        return invites_list
    def deleteInvite(self,data):
        return InvitesDao.deleteInvite(data['event_id'],data['applicant_id'],data['recruiter_id'])
    def registerInvite(self,data):
        return InvitesDao.registerInvite(data['event_id'],data['applicant_id'],data['recruiter_id'])
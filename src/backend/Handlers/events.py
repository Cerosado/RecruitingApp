import flask_praetorian
from flask import jsonify
from ..DAO.eventsDAO import EventsDao
from ..DAO.invitesDAO import InvitesDao
import flask_praetorian


class EventsHandler:
    ###########################################
    #             GETS                        #
    ###########################################
    def getEventById(self, event_id):
        eventsDao = EventsDao()
        result = eventsDao.getEventById(event_id)
        return result

    def getAllEvents(self):
        eventsDao = EventsDao()
        result = eventsDao.getAllEvents()
        return result

    def get_events_by_user_id(self):
        dao = EventsDao()
        user = flask_praetorian.current_user()
        is_company = "recruiter" in user.rolenames
        if is_company:
            results = dao.get_events_by_recruiter_id(user.identity)
        else:
            results = dao.get_events_by_applicant_id(user.identity)
        return jsonify(events=results)

    def registerEvent(self, data):
        events_dao = EventsDao()
        invites_dao = InvitesDao()

        recruiter_id = flask_praetorian.current_user().identity
        applicant_id = data['applicant_id']

        if len(data) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            event_id = events_dao.registerEvent(data['location'], data['additionalDetails'],
                                                True, data['date'])
            invites_id = invites_dao.registerInvite(event_id, applicant_id, recruiter_id)
            return jsonify(message="Event Created"), 201

    def deleteEventById(self,event_id):
        eventsDao = EventsDao()
        eventsDao.deleteEvent(event_id)
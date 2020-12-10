import flask_praetorian
from flask import jsonify
from ..DAO.eventsDAO import EventsDao


class EventsHandler:
    eventsDao = EventsDao()
    ###########################################
    #             GETS                        #
    ###########################################
    def getEventById(self, event_id):
        result = eventsDao.getEventById(event_id)
        return result
    def getAllEvents(self):
        result = eventsDao.getAllEvents()
        return result
    def registerEvent(self,data):
        if len(data) != 4:
            return jsonify(Error="Malformed post request"), 400
        else:
            return EventsDao.registerEvent(data['location'],data['description'],data['is_interview'],data['date'])
    def deleteEventById(self,event_id):
        eventsDao.deleteEvent(event_id)
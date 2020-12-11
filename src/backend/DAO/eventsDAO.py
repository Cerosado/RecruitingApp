from ..config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class EventsDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllEvents(self): 
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM events"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_events_by_applicant_id(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT e.*, a.first_name " \
                "FROM events e inner join invites i on e.event_id = i.event_id " \
                "inner join accounts a on a.user_id = i.recruiter_id " \
                "WHERE applicant_id = %s" % (user_id,)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_events_by_recruiter_id(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT e.*, a.first_name " \
                "FROM events e " \
                "inner join invites i on e.event_id = i.event_id " \
                "inner join accounts a on a.user_id = i.recruiter_id " \
                "WHERE recruiter_id = %s" % (user_id,)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getEventById(self, event_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from events WHERE event_id = %s;"
        cursor.execute(query, (event_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def registerEvent(self, location, description, is_interview, date):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO events(location, description, is_interview, date) VALUES (%s,%s,%s,%s) RETURNING event_id;"
        cursor.execute(query, (location, description, is_interview, date))
        event_id = cursor.fetchone()['event_id']
        self.conn.commit()
        cursor.close()
        return event_id

    #Delete one application by both ids
    def deleteEvent(self, event_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM events WHERE event_id=%s RETURNING event_id;"
        cursor.execute(query, (event_id))
        event_id = cursor.fetchone()['event_id']
        self.conn.commit()
        cursor.close()
        return event_id

#debugging script
# if __name__=='__main__':
#     dao=JobPostingsDao()
#     print("Job Postings:\n")
#     print(dao.getAllJobPostings())
    # print(dao.registerJobPosting("Software Engineer", 'Puerto Rico', 'Entry Level Position blah blah', 'Databases','Hourly','20','20','2001-09-28'))
    # print("All Job Postings: "+ str(dao.getAllJobPostings())+"\n\n")
    # dao.editJobPosting("Lead Developer", 'Puerto Rico', 'Entry Level Position blah blah', 'Databases','Hourly','20','20','2001-09-28')
    # firstPosting = dao.getJobPostingById(dao.getAllJobPostings()[0]['posting_id'])
    # print("Job Posting By ID: "+ str(firstPosting)+"\n\n")
    # print("Deleting first Posting:")
    # print(dao.deleteJobPosting(firstPosting['posting_id']))
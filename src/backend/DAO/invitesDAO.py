from ..config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class InvitesDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllInvites(self): 
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM invites"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

#Get all invites associated to event
    def getAllEventInvites(self, event_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from invites WHERE event_id = %s;"
        cursor.execute(query, (event_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
#Get all event invites associated to applicant
    def getAllApplicantInvites(self, applicant_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from invites WHERE applicant_id = %s;"
        cursor.execute(query, (applicant_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
#Get all events created by recruiter
    def getAllRecruiterInvites(self, recruiter_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from invites WHERE recruiter_id = %s;"
        cursor.execute(query, (recruiter_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def registerInvite(self, event_id, applicant_id, recruiter_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO events(event_id, applicant_id, recruiter_id) VALUES (%s, %s,%s) RETURNING event_id;"
        cursor.execute(query, (event_id, applicant_id, recruiter_id))
        event_id = cursor.fetchone()['event_id']
        self.conn.commit()
        cursor.close()
        return event_id

    #Delete one application by both ids
    def deleteInvite(self, event_id, applicant_id, recruiter_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM events WHERE event_id=%s, applicant_id=%s, recruiter_id=%s RETURNING event_id;"
        cursor.execute(query, (event_id, applicant_id, recruiter_id))
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
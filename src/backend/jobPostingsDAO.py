import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class JobPostingsDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllJobPostings(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM jobpostings"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    def getJobPostingById(self, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from jobpostings WHERE posting_id = %s;"
        cursor.execute(query, (posting_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    def registerJobPosting(self, position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO jobpostings(position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING posting_id;"
        cursor.execute(query, (position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline))
        posting_id = cursor.fetchone()['posting_id']
        self.conn.commit()
        cursor.close()
        return posting_id
    def editJobPosting(self, position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE jobpostings SET position_name=%s, location=%s, description=%s, key_details=%s, pay_type=%s, pay_amount=%s, user_id=%s, deadline=%s RETURNING posting_id;"
        cursor.execute(query, (position_name, location, description, key_details, pay_type, pay_amount, user_id, deadline))
        posting_id = cursor.fetchone()['posting_id']
        self.conn.commit()
        cursor.close()
        return posting_id
    def deleteJobPosting(self, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM jobpostings WHERE posting_id=%s RETURNING posting_id;"
        cursor.execute(query, (posting_id,))
        posting_id = cursor.fetchone()['posting_id']
        self.conn.commit()
        cursor.close()
        return posting_id
    def deleteJobPostingsByUser(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM jobpostings WHERE user_id=%s RETURNING user_id;"
        cursor.execute(query, (user_id,))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id
        
#debugging script
if __name__=='__main__':
    dao=JobPostingsDao()
    print("Job Postings:\n")
    print(dao.getAllJobPostings())
    # print(dao.registerJobPosting("Software Engineer", 'Puerto Rico', 'Entry Level Position blah blah', 'Databases','Hourly','20','20','2001-09-28'))
    # print("All Job Postings: "+ str(dao.getAllJobPostings())+"\n\n")
    # dao.editJobPosting("Lead Developer", 'Puerto Rico', 'Entry Level Position blah blah', 'Databases','Hourly','20','20','2001-09-28')
    # firstPosting = dao.getJobPostingById(dao.getAllJobPostings()[0]['posting_id'])
    # print("Job Posting By ID: "+ str(firstPosting)+"\n\n")
    # print("Deleting first Posting:")
    # print(dao.deleteJobPosting(firstPosting['posting_id']))
from ..config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class ApplicationsDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllApplications(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM applications"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    #Get all applications by user_id
    def getApplicationsByUser(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM applications "\
        "INNER JOIN jobpostings "\
        "ON applications.posting_id = jobpostings.posting_id "\
        "WHERE applications.user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    #Get all applications by posting_id
    def getApplicationsByPosting(self, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from applications WHERE posting_id = %s;"
        cursor.execute(query, (posting_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    #Get a single application by both ids
    def getApplication(self, user_id, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from applications WHERE user_id = %s and posting_id = %s;"
        cursor.execute(query, (user_id,posting_id))
        result = cursor.fetchone()
        cursor.close()
        return result
    def registerApplication(self, user_id, posting_id, rank):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO applications(user_id, posting_id, rank) VALUES (%s, %s,%s) RETURNING user_id;"
        cursor.execute(query, (user_id, posting_id,rank))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id
    #Edit not available because it shouldn't be editable

    #Delete all applications by user_id
    def deleteApplicationsByUser(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM applications WHERE user_id=%s RETURNING user_id;"
        cursor.execute(query, (user_id,))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id
    #Delete all applications by posting_id
    def deleteApplicationsByPosting(self, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM applications WHERE posting_id=%s RETURNING posting_id;"
        cursor.execute(query, (posting_id,))
        posting_id = cursor.fetchone()['posting_id']
        self.conn.commit()
        cursor.close()
        return posting_id
    #Delete one application by both ids
    def deleteApplication(self, user_id, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM applications WHERE posting_id=%s and user_id=%s RETURNING user_id;"
        cursor.execute(query, (posting_id, user_id))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id


#debugging script
if __name__=='__main__':
    dao=ApplicationsDao()
    print("All applications:\n")
    print(dao.getAllApplications())
    # print("All applications by User ID: 17")
    # print(dao.getApplicationsByUser("17"))
    # print("All applicants for Posting ID: 7")
    # print(dao.getApplicationsByPosting("7"))
    # print(dao.deleteApplicationsByPosting("7"))
    # print(dao.registerApplication("17","7"))
    # print(dao.deleteApplicationsByUser("17"))
    # print(dao.registerApplication("17","7"))
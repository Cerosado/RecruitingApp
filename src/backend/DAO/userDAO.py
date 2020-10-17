import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class UserDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllAccounts(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM accounts"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    def getAllRecruiters(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM accounts WHERE is_recruiter=TRUE"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    def getAllApplicants(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM accounts WHERE is_recruiter=FALSE"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    def getUserByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from accounts WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result
    def getUserById(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from accounts WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    def getUsersByFirstName(self, firstName):
        cursor = self.conn.cursor()
        query = "select * from accounts where first_name = %s;"
        result = cursor.fetchall()
        return result
    def getUsersByLastName(self, lastName):
        cursor = self.conn.cursor()
        query = "select * from accounts where last_name = %s;"
        result = cursor.fetchall()
        return result
    def getUsersByName(self, firstName, lastName):
        cursor = self.conn.cursor()
        query = "select * from accounts where first_name = %s and last_name = %s;"
        cursor.execute(query, (firstName,lastName,))
        result = cursor.fetchall()
    def getUserByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from accounts where email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result
    #Registers using by all info
    def registerUser(self, username, password, first_name, last_name, email, is_recruiter):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO accounts(username, password, first_name, last_name, email, is_recruiter) VALUES (%s, %s, %s, %s, %s,%s) RETURNING user_id;"
        cursor.execute(query, (username, password, first_name, last_name, email, is_recruiter))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id
    #Edits user by ID, requires all info
    def editUser(self, username, password, first_name, last_name, email, is_recruiter,user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE account SET username=%s, password=%s, first_name=%s, last_name=%s, email=%s, is_recruiter=%s WHERE user_id =%s RETURNING user_id;"
        cursor.execute(query, (username, password, first_name, last_name, email, is_recruiter,user_id))
        uid = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return uid
    #Deletes user by ID
    def deleteUser(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM accounts WHERE user_id=%s RETURNING user_id;"
        cursor.execute(query, (user_id,))
        uid = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return uid

#debugging script
if __name__=='__main__':
    dao=UserDao()
    print("Accounts:\n")
    print(dao.getAllAccounts())
    # print("Adding Moyi:")
    # print(dao.registerUser('Moyi', 'password', 'Moises', 'Garip', 'moises.garip@upr.edu', 'FALSE'))
    # print("Adding GE:")
    # print(dao.registerUser('GE', 'password', '', '', 'GE@ge.org', 'TRUE'))
    # print("All accounts: "+ str(dao.getAllAccounts())+"\n")
    # print("All recruiters: "+ str(dao.getAllRecruiters())+"\n")
    # print("All applicants: "+ str(dao.getAllApplicants())+"\n")
    # print("Deleting Moyi:")
    # print(dao.deleteUser(dao.getUserByUsername('Moyi')['user_id']))
    # print("Deleting GE:")
    # print(dao.deleteUser(dao.getUserByUsername('GE')['user_id']))

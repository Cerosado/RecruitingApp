from ..config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class ResumeDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'],
                                                pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def getAllResumes(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM resumes"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getResumeById(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from resumes WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_resume_ranking_parameters(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT skills, experience, education_section from resumes WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def registerResume(self, resume_data, resume_extension, education, college_name, degree, designation, experience, education_section, company_names, skills, total_experience, last_updated, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO resumes(resume_data, resume_extension, education, college_name, degree, designation, experience, education_section, company_names, skills, total_experience, last_updated, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_id;"
        cursor.execute(query, (resume_data, resume_extension, education, college_name, degree, designation, experience, education_section, company_names, skills, total_experience, last_updated, user_id))
        user_id = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return user_id

    def editResume(self, resume_data, resume_extension, education, college_name, degree, designation, experience, education_section, company_names, skills, total_experience, last_updated, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE resumes SET resume_data=%s, resume_extension=%s, education=%s, college_name=%s, degree=%s, designation=%s, experience=%s, education_section=%s, company_names=%s, skills=%s, total_experience=%s, last_updated=%s WHERE user_id =%s RETURNING user_id;"
        cursor.execute(query, (resume_data, resume_extension, education, college_name, degree, designation, experience, education_section, company_names, skills, total_experience, last_updated, user_id))
        uid = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return uid

    #resume pkey is user_id:
    def deleteResume(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM resumes WHERE user_id=%s RETURNING user_id;"
        cursor.execute(query, (user_id,))
        uid = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()
        return uid

#debugging script
if __name__=='__main__':
    dao=ResumeDao()
    print("Resumes: \n")
    print(dao.getAllResumes())
    # print(dao.registerResume("E'\x7f\x7f'", '.pdf', '2016-06-22 19:10:25-07', '17'))
    # print("All Resumes: "+ str(dao.getAllResumes())+"\n")
    # firstResume = dao.getResumeById(dao.getAllResumes()[0]['user_id'])
    # print("Resume By ID: "+ str(firstResume)+"\n")
    # print("Deleting first resume:")
    # print(dao.deleteResume(firstResume['user_id']))

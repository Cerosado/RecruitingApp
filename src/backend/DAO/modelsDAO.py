from ..config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class ModelsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host'])

        self.conn = psycopg2._connect(connection_url)

    def get_model_name(self, posting_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT model_name, use_education " \
                "from models m inner join jobpostings j on m.model_id = j.model_id WHERE j.posting_id = %s;"
        cursor.execute(query, (posting_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_models_id_and_desc(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT model_id, description from models"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results


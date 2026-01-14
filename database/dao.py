from database.DB_connect import DBConnect
from model.state import State

class DAO:
    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()
        anni = []
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT DISTINCT YEAR(s_datetime) as anno
                    FROM sighting
                    """

        cursor.execute(query)
        for row in cursor:
            anni.append(row['anno'])
        cursor.close()
        conn.close()
        return anni

    @staticmethod
    def get_forme():
        conn = DBConnect.get_connection()
        forme = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT shape
                    FROM sighting"""

        cursor.execute(query)
        for row in cursor:
            forme.append(row['shape'])
        cursor.close()
        conn.close()
        return forme

    @staticmethod
    def get_stati_connessi(year, shape):
        """Dizionario (s1,s2) --> peso_totale"""
        conn = DBConnect.get_connection()
        stati_connessi_peso = {}
        cursor = conn.cursor(dictionary=True)

        query = """SELECT n.state1, n.state2, COUNT(s.id) as avvistamenti
                    FROM neighbor n, sighting s
                    WHERE (s.state = n.state1 OR s.state = n.state2)
                    AND YEAR(s.s_datetime) = %s
                    AND s.shape = %s
                    GROUP BY n.state1, n.state2"""

        cursor.execute(query, (year, shape))
        for row in cursor:
            stati_connessi_peso[(row['state1'], row['state2'])] = row['avvistamenti']
        cursor.close()
        conn.close()
        return stati_connessi_peso

    @staticmethod
    def get_stati():
        conn = DBConnect.get_connection()
        stati = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT id, name, capital
                    FROM state"""

        cursor.execute(query)
        for row in cursor:
            stato = State(row['id'], row['name'], row['capital'])
            stati.append(stato)
        cursor.close()
        conn.close()
        return stati


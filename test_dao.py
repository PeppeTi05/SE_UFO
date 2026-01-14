from database.dao import DAO

anni = DAO.get_anni()
print(anni)

forme = DAO.get_forme()
print(forme)

stati_connessi = DAO.get_stati_connessi(1980, 'circle')
print(stati_connessi)

stati = DAO.get_stati()
print(stati)
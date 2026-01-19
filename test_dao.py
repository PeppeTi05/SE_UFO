from database.dao import DAO

anni = DAO.get_anni()
print(anni)

forme = DAO.get_forme(1999)
print(forme)

stati = DAO.get_stati()
print(stati)

stati_confinanti = DAO.get_stati_confinanti()
print(stati_confinanti)
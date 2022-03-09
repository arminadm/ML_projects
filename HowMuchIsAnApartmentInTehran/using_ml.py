#Armin Darabi Mahboub

from sklearn import tree
import mysql.connector

def main():
    """connecting to database"""
    cnx = mysql.connector.connect(user = "root", password = "sql13131350", database="propertyofshebash")
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM propertyinfo")
    
    #required lists for ML
    x = []
    y = []
    
    for loc, which_type, area, room, year, price, pricePerM in cursor:        
        """fitting data into list"""
        x.append([area, room, year])
        y.append([price])
        # print(f"loc: {loc}, which_type: {which_type}, area: {area}, room: {room}, year: {year}, price: {price}, pricePerM: {pricePerM}")

    """fitting data info ML tree"""
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(x, y)

    print("done")

    new_Data = [[200, 1, 1380]]
    answer = clf.predict(new_Data)
    print(answer)

if (__name__) == "__main__":
    main()
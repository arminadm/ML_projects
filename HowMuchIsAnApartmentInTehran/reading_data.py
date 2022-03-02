#Armin Darabi Mahboub

from requests import get
from bs4 import BeautifulSoup
import re
import mysql.connector

def main():
    """setting up the database"""
    cnx = mysql.connector.connect(user="root", password="123", database="propertyOfShebash")
    cursor = cnx.cursor()

    """getting all of the required data from shabeh.com"""
    for i in range(1, 201):
        response = get(f"https://shabesh.com/search/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86?page={i}")
        soup = BeautifulSoup(response.text, "html.parser")
        result_each_page = soup.find_all("div", attrs={"class": "list_infoBox__iv8WI p-2 align-self-center"})
        for element in result_each_page:
            #some elements doesn't have all of the variables, we need to ignore them
            try:
                price_as_string = re.findall("\<span class\=\"list\_infoItem\_\_8EH57 list\_infoPrice\_\_\_aJXK d\-block\"\>(.*?)تومان<\/span>", str(element))[0].replace(",","") 
                location = re.findall("<span class=\"list_infoItem__8EH57 ellipsis d-block\">(.*?)</span>", str(element))[0].replace("<!-- -->", "")
                price_as_float = float(price_as_string)
                pricePerM_as_string = re.findall("\<span class=\"list_infoItem__8EH57 font-14 global_colorGray1__i1u0y d-block\"\>متری <!-- -->(.*?)<!-- --> تومان</span>", str(element))
                pricePerM_as_float = float(pricePerM_as_string[0].replace(",", ""))
                propertyType = re.findall("<span class=\"list_infoItem__8EH57 ellipsis d-block font-14\">(.*?)</span>", str(element))[0]
                area = int(re.findall("<i class=\"icons_shMeter2__FhIjt\"></i><span class=\"px-1 font-12\">(.*?)</span>", str(element))[0].replace("<!-- --> متر", ""))
                room = int(re.findall("<span class=\"d-inline-flex ps-2 align-items-center\"><i class=\"icons_shBed2__R3PVt\"></i><span class=\"px-1 font-12\">(.*?)</span>", str(element))[0].replace("<!-- --> خواب", ""))
                year = int(re.findall("<span class=\"d-inline-flex align-items-center\"><i class=\"icons_shCalendar__3qrT7\"></i><span class=\"px-1 font-12\">(.*?)</span>", str(element))[0])
                access = True

            except:
                access = False
            
            if access: 
                print(price_as_float)
                print(pricePerM_as_float)
                print(propertyType)
                print(location)
                print(f"masahat: {area}, khabha: {room}, saalesakht: {year}")
                print("==================")
                
                """updating database"""
                cursor.execute(f"INSERT INTO propertyInfo VALUES(\"{location}\", \"{propertyType}\", {area}, {room}, {year}, {price_as_float}, {pricePerM_as_float})")
                cnx.commit()
        print(f"page {i} done")
    
    cnx.close()            
    

if (__name__) == "__main__":
    main()
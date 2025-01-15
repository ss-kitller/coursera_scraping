
from bs4 import BeautifulSoup
import requests

import time
from selenium import webdriver




def scrolling ():
    driver = webdriver.Chrome()  # Replace with your WebDriver
    driver.get("https://www.coursera.org/search?query=data%20engineering&aid=true")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5) # We wait 5 seconds so the page loads up
    driver.quit()


link = 'https://www.coursera.org/search?query=data%20engineering&aid=true'
response = requests.get(link)
soup = BeautifulSoup(response.text, 'lxml')
scrolling()
courses_list = soup.find('ul',class_="cds-9 css-5t8l4v cds-10")
courses = courses_list.find_all('li',class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90")
List = []
for course in courses:
    course_name = course.find('h3', class_ ="cds-CommonCard-title css-6ecy9b").text
    List.append(course_name)
print(List)
with open ('name_of_courses.txt', 'w') as f:
    for i in List:
        f.write(i)
        f.write("\n")
    f.close()
print("writing complete")

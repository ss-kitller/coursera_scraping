from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
import os

def scrolling ():
    driver = webdriver.Chrome()
    search_key = input("donner le mot que vous voulez chercher dans Coursera ")
    link = f'https://www.coursera.org/search?query={search_key}'
    driver.get(link)

        # à fixer ces valeurs en prenons en considération la vitesse de chargement des élements de la page
    scroll_pause_time = 0.5  # Time to wait between scrolls
    scroll_duration = 20  # Total scroll duration
    scroll_amount = 500  # Pixels to scroll each time


    start_time = time.time()
    while time.time() - start_time < scroll_duration:
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(scroll_pause_time)

        # Get the page source after scrolling
    page_source = driver.page_source
    time.sleep(10)
    driver.quit()

    return page_source

    #lists I will append to
response = scrolling()
soup = BeautifulSoup(response, 'lxml')



all_courses = []
all_names = []
all_levels = []
all_certif_type = []
all_duration = []
all_ratings = []
all_skills = []



outer_div = soup.find_all('ul', class_="cds-9 css-5t8l4v cds-10")
for outer_div_1 in outer_div:
    inner_div = outer_div_1.find_all('li', class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90")
    for j in inner_div:
            #liste des noms des certifs
        course_name = j.find('h3', class_ ="cds-CommonCard-title css-6ecy9b").text
        all_courses.append(course_name)



            #nom des sociétés
        name = j.find('p', class_="cds-ProductCard-partnerNames css-vac8rf")
        if name:
            all_names.append(name.text)
        else:
            all_names.append("name not found")



            # information sur le niveau, durée,
        levels = j.find('div', class_="cds-CommonCard-metadata")
        level = levels.find('p', class_="css-vac8rf")
        if level:
            # il faut que les informations soient aplaties ou bien dans une liste pour garder une bonne symétrie
            level_in_list = [level.text.split('·')[0]]
            certif_in_list = [level.text.split('·')[1]]
            duration_in_list = [level.text.split('·')[2]]


            all_levels.append(level_in_list)
            all_certif_type.append(certif_in_list)
            all_duration.append(duration_in_list)
        else:
            all_levels.append("no info dispo")



            # Ratings sur la certif
        ratings = j.find('div', class_="cds-RatingStat-sizeLabel css-1i7bybc")
        if ratings:
            result = ratings.find('span',class_="css-6ecy9b")
        elif result :
            all_ratings.append(result.text)
        else:
            all_ratings.append("no information :/")



            # Skills que la certif guarantit
        temp_list = []
        result = j.find('div', class_="cds-ProductCard-body")
        if result:
            h = result.find('div', class_="cds-CommonCard-bodyContent")
            skill = h.find('p', class_="css-vac8rf").text.strip()
            temp_list.append(skill)
            all_skills.append(temp_list[0][32::])
        else:
            temp_list.append("No information given")
            all_skills.append(temp_list)


    # Making the arrays the same length
min_length = min(len(all_courses),len(all_ratings), len(all_skills), len(all_levels), len(all_certif_type), len(all_duration), len(all_names))
all_courses = all_courses [:min_length]
all_names =  all_names[:min_length]
all_levels = all_levels[:min_length]
all_certif_type = all_certif_type[:min_length]
all_duration = all_duration[:min_length]
all_ratings = all_ratings[:min_length]
all_skills = all_skills[:min_length]


    # ENREGISTREMENT SUR UN FICHIER EXCEL
file_name = "table.csv"
if os.path.exists(file_name):
    os.remove(file_name)

df = pd.DataFrame({
    "Course Name": all_courses,
    "Certificate Provider": all_names,
    "Certification Level": all_levels,
    "Certification Type": all_certif_type,
    "Duration": all_duration,
    "Certification Rating": all_ratings,
    "Skills": all_skills
})

# Save to CSV file
df.to_csv(file_name, index=False, encoding="utf-8")

print("dataframe saved successfully :) ")













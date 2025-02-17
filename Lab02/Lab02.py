import csv
import requests
import re
import json

from bs4 import BeautifulSoup
from pprint import pprint
from typing import Dict, List, Union
import urllib.parse as urlparse

fieldnames = ['Name of Course', 'Type of Course', 'Long text', 'Number', 'Short text', 'Term', 'Hours per week in term', 'Expected no. of participants', 'Max. participants', 
'Turnus', 'Assignment', 'Credits', 'Additional Links', 'Language', 'application period', 'Responsible Instructor']

def problem_1(name: str) -> List[Dict[str, Union[str, List[str]]]]:
    # TODO Write your code for Problem 1 here.
    url = "https://how-i-met-your-mother.fandom.com/wiki/"+name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    table = soup.find("table", class_="infobox character")
    rows = table.findAll('tr')
    infobox=[]
    
    for row in rows:
        row_dic = {}
        val = ""
        addVal = False
        attrs = row.findAll("div")
 
        for idx, ele in enumerate(attrs):
            if not ele:
                break
            if idx == 0:
                row_dic["attribute"] = ele.text
                addVal = True
            else:
                val = ele.get_text(separator=" ").strip()
                val = re.sub("(\[).*?(\])", "", val)
                val = re.sub('\s+', ' ', val)
                row_dic["value"] = val
    
        if addVal: 
            infobox.append(row_dic)

    return infobox


def problem_2_1() -> List[Dict[str, str]]:
    base_url = "https://www.lsf.uni-saarland.de/qisserver/rds?state=wtree&search=1&trex=step&root120221=320944|310559|318658|311255&P.vx=kurz&noDBAction=y&init=y"
    # TODO Write your code for Problem 2.1 here.
    url = eng_url(base_url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    all_courses=[]
    all_headers = soup.findAll("a", {"class": "ueb"})

    headers = []
    for header in all_headers:
        if header.has_attr('title'):
            headers.append(header.attrs.get('href'))

    for i, url in enumerate(headers):
        if i <= 3:
            continue
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        courses = soup.findAll("td", {"class": ["mod_n_odd", "mod_n_even"]})
        for course in courses:
            a_tag = course.find("a", {"class": "regular"})
            if not a_tag:
                continue

            one_course={}    
            name = a_tag.text
            link = a_tag.attrs.get('href')
            one_course["Name of Course"] = name
            one_course["URL"] = link
            all_courses.append(one_course)
    
    return all_courses


def problem_2_2(url: str) -> Dict[str, Union[str, List[str]]]:
    # TODO Write your code for Problem 2.2 here.
    page = requests.get(eng_url(url))
    soup = BeautifulSoup(page.content, "html.parser")
    course_data = {key: "" for key in fieldnames}

    table = soup.find("a", {"name": "basicdata"}).find_next_sibling("table")

    rows = table.findAll("tr")
    for row in rows:
        headers = row.findAll("th")
        data = row.findAll("td")
        for h, d in zip(headers, data):
            key = re.sub('\s+', ' ', h.text)
            key = key.strip()
            val = re.sub('\s+', ' ', d.text)
            val = re.sub(",", " ", val)
            val = val.strip()
            course_data[key] = val

    table2 = soup.find("table", {"summary": "Verantwortliche Dozenten"})
    instructors=[]
    if table2:
        data = table2.findAll("td", {"headers": "persons_1"})
        for d in data:
            instr = d.a.text.strip()
            instr = re.sub(",", " ", instr)
            instructors.append(instr)
    
    course_data["Responsible Instructor"] = instructors

    return course_data

def problem_2_3() -> None:
    # TODO Write your code for Problem 2.3 here.
    course_list = problem_2_1()
    with open('courses.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
    
    with open('courses.csv', 'a', encoding='UTF8') as f:

        for course in course_list:
            course_name = course["Name of Course"] 
            course_data = problem_2_2(course["URL"])

            f.write(course_name)
            f.write(",")

            for key in fieldnames[1:]:
                value = course_data[key]
                if key == "Responsible Instructor" or key == "Additional Links":
                    f.write(json.dumps(value))
                else:
                    f.write(value)
                f.write(",")

            f.write("\n")

    return None

# reference
# https://www.adamsmith.haus/python/answers/how-to-add-parameters-to-an-url-in-python

def eng_url(url: str):
    params = {"language":"en"}
    url_parse = urlparse.urlparse(url)
    query = url_parse.query
    url_dict = dict(urlparse.parse_qsl(query))
    url_dict.update(params)
    url_new_query = urlparse.urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    new_url = urlparse.urlunparse(url_parse)
    #print(new_url)
    return new_url

def main():
    # You can call your functions here to test their behaviours.
    #pprint(problem_1("Tracy McConnell"))
    #pprint(problem_2_1())
    url = "https://www.lsf.uni-saarland.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=136353&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung"
    new_url = eng_url(url) 
    #pprint(problem_2_2(url))
    #pprint(problem_2_3())

if __name__ == "__main__":
    main()
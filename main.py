
import sys
import os
import requests
from bs4 import BeautifulSoup
import tkinter.messagebox
from tkinter import *

cities = ["toronto", "ottawa", "vancouver"]

URL = "https://www.joblist.com/ca/search?l="

location = "blank"
job = "blank"
jobs = []
job_elements = []

root = Tk()
check1 = 3
check2 = 0

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def send_message(arg):
    print(arg)
    global check1, check2, location, jobs
    inp = inputField.get()
    if (inp):
        inp = inp.lower()
        inputField.delete(0, "end")
        text.insert(str(check1) + ".0", "User: " + inp + "\n")
        check1 += 1
        if (arg == 0):
            if (inp in cities):
                check2 += 1
                print(check2)
                location = inp
                text.insert(str(check1) + ".0", "Enter job description: \n")
                check1 += 1
                return check2
            else:
                text.insert(str(check1) + ".0", "Bot: Invalid input. Please, try again: \n")
                check1 += 1
        elif (arg == 1):
            check2 += 1
            jobs = inp.split(" ")
            jobs_str = ""
            for i in jobs:
                jobs_str += i + ' '
            get_jobs(jobs_str, location)
            return check2
        elif(inp == 'yes'):
            check1 = 3
            check2 = 0
            final_str = ''
            for job_element in job_elements:
                title_element = job_element.find("h2", class_="itemHeaderUi")
                company_element = job_element.find("div", class_="itemMetaUi")
                location_element = job_element.find_all("div", class_="itemMetaUi")
                print(title_element.text)
                print(company_element.text)
                print(location_element[1].text)
                print()
                final_str += title_element.text + '\n' + company_element.text + '\n' + location_element[1].text + '\n\n'
            tkinter.messagebox.showinfo(title='Results', message=final_str)
            restart_program()
        else:
            restart_program()
        text.pack()



def get_jobs(j, l):
    global URL, job_elements, check1
    mURL = URL + l + "%2C+ON&q=" + j + "&lr=ANY_LOCATION"

    page = requests.get(mURL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="JobContainer")
    job_elements = results.find_all("div", class_="job-item")

    text.insert(str(check1) + ".0", "Found " + str(len(job_elements)) + " results. Print 'yes' to see results. Otherwise, bot will be restarted")


root['bg'] = '#fafafa'
root.title('Job_Finder')
root.geometry('600x400')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#fafafa', bd=5)
frame_top.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)

frame_bottom = Frame(root, bg='#fafafa', bd=5)
frame_bottom.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.3)

inputField = Entry(frame_bottom, bg='#fafafa', font=30)
inputField.pack()



btn = Button(frame_bottom, text='send', command= lambda: send_message(check2))
btn.pack()

text = Text(frame_top)
text.insert("1.0", "Bot: Hello!\n")
text.insert("2.0", "Bot: Please,enter you city (Toronto, Ottawa, Vancouver): \n")
text.pack()

root.mainloop()



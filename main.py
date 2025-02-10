import os
import time
import pyfiglet

def run_PE():
    file = input("Enter the path and name of the file : ")
    os.system("python3 Extract/PE_main.py {}".format(file))

def run_URL():
    os.system('python3 Extract/url_main.py')

def exit():
    os.system('exit')

def start():
    print(pyfiglet.figlet_format("ZU Detector"))
    print(" Welcome to antimalware detector \n")
    print(" 1. PE scanner")
    print(" 2. URL scanner")
    print(" 3. Exit\n")

    select = int(input("Enter your choice : "))
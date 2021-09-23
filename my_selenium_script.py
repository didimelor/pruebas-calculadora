from typing import Text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("http://127.0.0.1:5000/")
print(driver.title)
#assert "Python" in driver.title

functions = ["(x*x - 16)", 
            "cos(x)- x**3", 
            "x + 20",
            "sin(x) \ 20",
            "1.0 \ x",
            "x - cos(x)",
            "0.3**x-x**2+4",
            "2*cos(x)-(sqrt(x)/2)-1",
            "tan(x)",
            "x-cos(x)",
            "exp(0.3*x)-x**2+4",
            "2*cos(x)-(sqrt(x)/2)-1",
            "3*(x)*(x)+4*(x)-10"]

formWrapper = driver.find_element_by_id("form-wrapper")
theForm = formWrapper.find_element_by_class_name("theForm")
eqHolder = theForm.find_element_by_id("eq-holder")
x0Holder = theForm.find_element_by_id("x0-holder")

for function in functions:
    f = eqHolder.find_element_by_name("eq")
    print(function)
    f.send_keys(function)
    x0Str = x0Holder.find_element_by_name("x0")
    #num = random.uniform(-3.0, 3.0)
    #print(round(num,3))
    num = 0.9 #round(num,3)
    x0Str.send_keys(num) #random.uniform(-3.0, 3.0)
    time.sleep(2)
    driver.find_element_by_name("subBotton").click()
    time.sleep(3)
    driver.back()

driver.quit()


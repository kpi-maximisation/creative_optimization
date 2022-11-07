# import webdriver
from selenium import webdriver
  
# create webdriver object
driver = webdriver.Firefox()
  
# get geeksforgeeks.org
driver.get("https://s3.us-east-1.amazonaws.com/a.futureadlabs.com-us-east-1-backup/us-east-1/games/7fc571f85358c5d37efafde99b6896d7/036c038eab1c4bba5dbf/index.html")
  
# get element 
element = driver.find_element_by_class_name("header--navbar")
  
# click screenshot 
element.screenshot('foo.png')
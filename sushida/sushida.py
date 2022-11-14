from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

window = (750, 620+123)
driver.set_window_size(*window)

i = 1
while i <= 100000000000:
    driver.get('http://www.rays-counter.com/d515_f8_022/6350a333753b3/')

#////

from selenium import webdriver
from xlwt import Workbook
import os
import errno


def scrap():

    driver = webdriver.Chrome(executable_path='chromedriver')

    '''
    Change the url according to the need
    Remember this a static scrapper, will work only for the below URL with a valid values for X and Y
    http://www.espncricinfo.com/cricket/content/player/caps.html?country=X;class=Y 
    
    '''

    url = "http://www.espncricinfo.com/cricket/content/player/caps.html?country=8;class=1"

    driver.get(url)

    element = driver.find_element_by_xpath("//div[@class='ciPlayerbycapstable']")

    wb = Workbook()
    sheet1 = wb.add_sheet('Player List')

    sheet1.write(0, 0, "Player Name")
    sheet1.write(0, 1, "Profile Id")

    count = 1
    for name in element.find_elements_by_class_name("ciPlayername"):

        anchor = name.find_element_by_tag_name("a")
        href = anchor.get_attribute("href")
        number = str(href).split('/')[-1][:-5]
        inner_html = anchor.text
        sheet1.write(count, 0, inner_html)
        sheet1.write(count, 1, number)
        count += 1

    file_name_element = driver.find_element_by_xpath("//div[@class='icc-home']")
    file_name = file_name_element.text.split("/")

    wb.save(os.path.join('Output', file_name[1]+"_"+file_name[2]+".xls"))


def main():

    if not os.path.exists("Output"):
        try:
            os.mkdir("Output")
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    scrap()


if __name__ == '__main__':
    main()

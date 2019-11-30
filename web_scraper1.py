import bs4
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import click
from selenium.webdriver.chrome.options import Options
import pandas as pd

def today(currentURL,driver):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    details=driver.find_elements_by_xpath("//div[contains(@class,'today_nowcard-main')]")
    for items in details:
        click.echo(items.text)
    dict1={}
    i=1
    j=str(i)
    for row in driver.find_elements_by_xpath("//tbody/tr/th"):
        list1=[]
        for column in driver.find_elements_by_xpath("//tbody/tr["+j+"]/td"):
            list1.append(column.text)
        dict1[row.text]=list1
        j=int(j)+1
        j=str(j)
    df1=pd.DataFrame(dict1)
    click.echo(df1)

def hourly(currentURL,driver):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    i=1
    j=str(i)
    l1=[]
    for headers in driver.find_elements_by_xpath("//tbody/tr[1]/td"):
        l2=[]
        for row in driver.find_elements_by_xpath("//tbody/tr["+j+"]/td"):
            l2.append(row.text)
        l1.append(l2)
        j=int(j)+1
        j=str(j)
    df=pd.DataFrame(l1,columns=['INDEX','TIME','DESCRIPTION','TEMP','FEELS','PRECIP','HUMIDITY','WIND'])
    click.echo(df)

def fiveDay(currentURL,driver):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    dict1={}
    i=1
    j=str(i)
    l1=[]
    l1.append('INDEX')
    l3=[]
    for headers in driver.find_elements_by_xpath("//thead//th"):
        l1.append(headers.text)
    click.echo(l1)
    for items in driver.find_elements_by_xpath("//tbody//tr"):
        l2=[]
        for rows in driver.find_elements_by_xpath("//tbody/tr["+j+"]/td"):
            l2.append(rows.text)
        l3.append(l2)
        j=int(j)+1
        j=str(j)       
    df1=pd.DataFrame(l3,columns=l1)
    click.echo(df1)                

def tenDay(currentURL,driver):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    dict1={}
    i=1
    j=str(i)
    l1=[]
    l1.append('INDEX')
    l3=[]
    for headers in driver.find_elements_by_xpath("//thead//th"):
        l1.append(headers.text)
    click.echo(l1)
    for items in driver.find_elements_by_xpath("//tbody//tr"):
        l2=[]
        for rows in driver.find_elements_by_xpath("//tbody/tr["+j+"]/td"):
            l2.append(rows.text)
        l3.append(l2)
        j=int(j)+1
        j=str(j)       
    df1=pd.DataFrame(l3,columns=l1)
    click.echo(df1)  

def weekend(currentURL,driver):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    l3=[]
    l2=[]
    for items in driver.find_elements_by_xpath("//section[contains(@classname,'wxcard')]/header"):
            l2.append(items.text)
    l3.append(l2)
    click.echo(l3)

def monthly(currentURL,date,driver,actions):
    driver.get(currentURL)
    driver.implicitly_wait(15)
    if len(date.strip())>0:
        date_array=date.strip().split("/")
        a=month_list[int(date_array[1])-1]+date_array[2]
        days=month_tdays[int(date_array[1])-2]
        select = Select(driver.find_element_by_css_selector('#month-picker'))
        count=0
        for j in range(0,50):
            try:
                select.select_by_visible_text(a)
            except:
                count+=1
        if count==50:
            click.echo("date out of range")
        else:
            first_date=driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div:nth-child(1) > div.date').text
            if int(first_date)!=1:
                date_index=days-int(first_date)+1+int(date_array[0])
            else:
                date_index=int(date_array[0])
            selected_date=driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div:nth-child('+str(date_index)+') > div.date')
            actions.move_to_element(selected_date)
            actions.click(selected_date)
            actions.perform()
            dateData(driver)
    else:
        dateData(driver)

def dateData(driver):
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col1 > div > div.temp.hi > span').text
        click.echo("Highest Temp:" + str(temp))
    except:
        click.echo("error")

    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col1 > div > div.temp.low > span > span').text
        click.echo("Lowest Temp:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col1 > div > h3').text
        click.echo("Weather Type:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col1 > div > span:nth-child(5) > span').text
        click.echo("Percentage:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col3 > div:nth-child(1) > span').text
        click.echo("Sunrise Time:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col3 > div:nth-child(2) > span').text
        click.echo("Sunset Time:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col4 > div:nth-child(1) > span').text
        click.echo("Moonrise Time:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col4 > div:nth-child(2) > span').text
        click.echo("Moonset Time:" + str(temp))
    except:
        click.echo("error")
    try:
        temp = driver.find_element_by_css_selector('#main-Calendar-21448498-aac6-4a1d-aecc-717f3b4e787b > div > div > span > div.forecast-monthly__day-info.visible > div.forecast-monthly__day-info__content > div.col.col2 > div.moon_phrase > span:nth-child(1)').text
        click.echo("Moon Phase:" + str(temp))
    except:
        click.echo("error")
                            

@click.command()
@click.option('--place', prompt='enter place(mandatody field)',help='Place for which we need weather')
@click.option('--date', prompt='enter date(dd/mm/yyyy) if any otherwise press ENTER',default='',help='Date for which we need weather')
@click.option('--forecast', prompt='enter forecast from hourly, 5day, 10day and monthly or simply press ENTER for choosing today as forecast',default='today',help='Type of forecast')

def getData(place,date,forecast):
    if len(date.strip())>0:
        forecast="monthly"
    if len(place.strip())==0:
        click.echo("please input a place name")
    else:
        driver = webdriver.Chrome('chromedriver')
        actions = ActionChains(driver)
        driver.get("https://weather.com/en-IN/")
        driver.implicitly_wait(15)

        textBox=driver.find_elements_by_css_selector('#header-TwcHeader-144269fc-62bc-4d06-bc79-e158594b14ff > div > div > div > div.styles__content__1OMmY.styles__ready__2ZM2w.all-ready > div > div.styles__input__GVnwF.typeahead-wrapper > div > input')
        textBox[0].send_keys(place)

        city=driver.find_elements_by_css_selector('#header-TwcHeader-144269fc-62bc-4d06-bc79-e158594b14ff > div > div > div > div.styles__content__1OMmY.styles__ready__2ZM2w.all-ready > div > div.styles__root__24hPt.styles__open__3FyHR > div.styles__inner__3moHD.styles__menu__23Qmz > div > ul > li:nth-child(1) > a')
        if len(city)==0:
            click.echo("please enter a valid place name")
        else:
            city[0].click()
            currentURL = driver.current_url
            if len(forecast.strip())!=0:
                if forecast.strip().lower()=="today":
                    currentURL=currentURL
                    today(currentURL,driver)
                    #today page
                elif forecast.strip().lower()=="hourly":
                    currentURL = currentURL.replace("today","hourbyhour")
                    hourly(currentURL,driver)
                    #hourly
                elif forecast.strip().lower()=="5day":
                    currentURL = currentURL.replace("today","5day")
                    fiveDay(currentURL,driver)
                    #5day
                elif forecast.strip().lower()=="10day":
                    currentURL = currentURL.replace("today","tenday")
                    tenDay(currentURL,driver)
                    #10day
                elif forecast.strip().lower()=="weekend":
                    currentURL = currentURL.replace("today","weekend")
                    weekend(currentURL,driver)
                    #weekend
                elif forecast.strip().lower()=="monthly":
                    currentURL = currentURL.replace("today","monthly")
                    monthly(currentURL,date,driver,actions)
                                                 
if __name__ == '__main__':
    month_list=['Jan ','Feb ','Mar ','Apr ','May ','Jun ','Jul ','Aug ','Sep ','Oct ','Nov ','Dec ']
    month_tdays=[31,28,31,30,31,30,31,31,30,31,30,31]
    getData()
                    
                    
        
        
        
        
    

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:56:11 2020

@author: xry
"""
#先登上qq，用的是快速登录
from selenium import webdriver
from lxml import etree
import time
import stu_ml
import stu_dsp
import re


course_url_ml="课程地址"
course_url_dsp="课程地址"
browser = webdriver.Firefox()
browser.get(course_url_ml)#不同
time.sleep(3)
#打开新标签页
req="快速登录窗口的地址"  #原网页找不到
js='window.open("'+req+'");'
browser.execute_script(js)
windows = browser.window_handles
browser.switch_to.window(windows[-1])
time.sleep(2)
#browser.get_screenshot_as_file("D:\\te.jpg")
browser.find_element_by_xpath("//a[@class='face']").click()

browser.switch_to.window(windows[0])

#爬取两次：
stu_set=set()
for times in range(2):
    browser.refresh() #刷新  登录以后回来刷新就可以
    time.sleep(5)
    #点击成员
    #刷新成员列表
    try:
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/div[1]/a[2]").click()
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[1]').click()
    except Exception as e:
        print(e)
    name=[]
    #三次下一页
    try:
        for i in range(3):
            page=browser.page_source
            tree=etree.HTML(page)
            name.extend(tree.xpath("//span[@class='member-item-inner member-item-inner-fullline']/text()"))
            browser.find_element_by_xpath("//span[@class='im-icon icon-font i-v-right']").click()
    except Exception as e:
        print(e)
        print(name)

    #匹配缺勤
    stu_p=[]
    for i in stu_ml.stu_ml:    #不同
        stu_ex=[]
        for j in name: 
            a=re.findall(i,j)
            stu_ex.extend(a)
        if len(stu_ex) == 0:
                stu_p.append(i)
    if times==0:
        set0=set(stu_p)
    if times==1:
        set1=set(stu_p)
stu_set=set0&set1     
browser.quit()

#输出
f=open('D:\\1.xls','w')
for i in stu_set:
    f.write(i+'\n')
f.close()


    

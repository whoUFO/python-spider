# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:38:13 2021
学习强国
@author: DKY
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import os


HOME_PAGE = 'https://www.xuexi.cn/'
VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html'
LONG_VIDEO_LINK = 'https://www.xuexi.cn/f65dae4a57fe21fcc36f3506d660891c/b2e5aa79be613aed1f01d261c4a2ae17.html'
LONG_VIDEO_LINK2 = 'https://www.xuexi.cn/0040db2a403b0b9303a68b9ae5a4cca0/b2e5aa79be613aed1f01d261c4a2ae17.html'
TEST_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'
SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'
LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'
ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'


class DatiError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


def save_cookie(browser):
    cookies = browser.get_cookies()
    # print("开始保存cookie! ", cookies)
    print("开始保存cookie! ")
    pkCookies = pickle.dumps(cookies)
    with open('xuexi.cookie', 'wb+') as f:
        f.write(pkCookies)
        print("cookie已保存！")
    return True


def read_cookie(browser):
    with open('xuexi.cookie', 'rb') as f:
        pkCookies = pickle.load(f)
        # print("开始读取cookie! ", pkCookies)
        print("开始读取cookie! ")
        for item in pkCookies:
            if ('expiry' in item) and (item['expiry'] != (int(item['expiry']))):
                # print("修改前：", item)
                item['expiry'] = int(item['expiry'])  # 学习强国返回的expiry有小数，去掉
                # print("修改后：", item)
                browser.add_cookie(item)
            else:
                # print("未修改：", item)
                browser.add_cookie(item)
    return True


def login_sim(browser):
    print("开始模拟登陆")
    browser.get(LOGIN_LINK)
    browser.maximize_window()
    browser.execute_script("var q=document.documentElement.scrollTop=1000")
    time.sleep(20)
    return True


def login_simulation(browser):
    # """模拟登录"""

    browser.get(HOME_PAGE)
    # time.sleep(5)
    browser.maximize_window()
    if(os.path.exists('xuexi.cookie')):
        print("cookie存在！")
        read_cookie(browser)  # 读cookie
        print("读完cookie，打开首页")
    else:
        print("cookie不存在，进入登录页面！")
        login_sim(browser)  # 模拟登录
        save_cookie(browser)

    browser.get(HOME_PAGE)
    save_cookie(browser)  # 更新cookie

    print("模拟登录完毕\n")
    return True


def read_articles(browser):
    browser.get(url=ARTICLES_LINK)
    article_lis = WebDriverWait(browser, 100).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//span[@style='white-space: nowrap;']")))
    readed = 0
    for article in article_lis:
        article.click()
        if readed > 7:
            break
        all_handles = browser.window_handles
        browser.switch_to.window(all_handles[-1])
        browser.get(browser.current_url)
        for i in range(0, 2000, 100):

            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(5)
        for i in range(2000, 0, -100):
            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(5)
        time.sleep(80)
        browser.close()
        browser.switch_to.window(all_handles[0])

        readed += 1
    print("阅读文章完毕\n")
    return True


def watch_videos(driver):
    driver.get(url=VIDEO_LINK)
    video_lis = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, ".//span[@class='text' ][@style='white-space: nowrap;']")))
    watched = 0
    spend_time = 0
    for video in video_lis:
        video.click()

        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])

        time.sleep(5)
        video_duration_str = driver.find_element_by_xpath(
            "//span[@class='duration']").get_attribute('innerText')
        video_duration = int(video_duration_str.split(
            ':')[0]) * 60 + int(video_duration_str.split(':')[1])
        # 保持学习，直到视频结束
        if video_duration > 70:
            # 只看大于1分钟
            video_duration = 70
            watched += 1
            time.sleep(video_duration + 3)
            spend_time += video_duration + 3
        else:
            print("视频时长少于70秒，跳过。")
        print("已观看{}个视频".format(watched))
        driver.close()
        driver.switch_to.window(all_handles[0])
        if watched > 7:
            print("视频观看结束!")
            break
    return True


def DaTi(driver):
    retry = False
    # 如果查找失败，表示进入答题完成页面。
    try:
        time.sleep(1)  # 等待一秒，其实也无所谓，但是为防止过快操作造成电脑卡顿，还是等待一秒。
        elem_juje = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="q-header"]')))
    except:
        elem_juje = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button/span')))
        if elem_juje:
            return True
        else:
            return False

    try:
        juje = elem_juje.get_attribute('innerText')

        # 在每日答题中，有三类题，判断题、选择题、填空题，所以先获取题的类别
        # 注意 特别需要注意的是 By.XPATH 和 xpath 文本获取稍有却别，By.XPATH 获取文本方式为.get_attribute('innerText')
        print("题型：{}".format(juje))

        if '选' in juje:
            retry = True
            elem_tishi = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[@class="tips"]')))
            elem_tishi.click()
            # 在答题中，答案在查看提示中以红色标记，所以首先要模拟点击查看答案，使答案加载
            time.sleep(0.5)
            elem_answer = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@class="line-feed"]/font')))
            # 提取红色标记的文字，即答案
            time.sleep(0.5)
            # 同样没什么实际意义

            ans_lis = []
            for elem in elem_answer:
                ans_lis.append(elem.get_attribute('innerText'))
            # 因为选择题嘛，不一定就是单选题，所以要存放这些答案，以便于在选项中找答案
            print('得到答案')
            time.sleep(0.5)
            # 同样没什么实际意义

            elem_juje.click()
            # 再次模拟点击的原因是 此时 查看提示 框还处于打开状态，如果不关闭，会影响提交答案的操作
            # 模拟点击网页，关闭 查看提示 框
            time.sleep(0.5)

            elem_xuanxiang = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    '//div[@class="question"]/div[@class="q-answers"]/div[contains(@class,"q-answer")]'
                )))
            # 获取所有的选项节点

            for elem in elem_xuanxiang:
                data = elem.get_attribute('innerText')[3:].replace('-', '')
                print(data)
                for i in ans_lis:
                    if i in data:
                        elem.click()
                        ans_lis.remove(i)
                        # 根据依次A -- > D 遍历答案,将两者对照进行选择与否，所以满足要求后去除该答案
                        # 防止对选项多次点击造成取消选择或其他错误
                        time.sleep(0.5)  # 防止过快操作，每次选择后等待0.5秒
                        break

            elem_next = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="action-row"]/button')))
            elem_next.click()
            retry = False
            # 模拟点击确定按钮跳转下一题
            DaTi(driver)
        elif '填' in juje:
            retry = True
            elem_tishi = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[@class="tips"]')))
            elem_tishi.click()

            time.sleep(0.5)
            elem_answer = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="line-feed"]')))

            time.sleep(0.5)
            if '请观看视频' in elem_answer.get_attribute('innerText'):
                # 在填空题中会有观看视频的题目，而且查看提示中会写‘请观看视频’而不会直接给出答案，所以要人工选择
                print("需要观看视频,不直接给出答案，要人工选择，拒绝做题")
                retry = True
                raise DatiError("拒绝做题")

            elem_answer = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     './/div[@class="line-feed"]/font[@color="red"]')))
            answer = []
            time.sleep(0.5)
            for elem in elem_answer:
                answer.append(elem.get_attribute('innerText'))
            # 同样填空题中也有多个空的情况，所以将答案放在列表里
            time.sleep(1)
            print(answer)
            elem_data = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//input[@class="blank"]')))
            # 找到每个空
            for i in range(len(answer)):
                elem_data[i].send_keys(answer[i])
                time.sleep(0.5)
            # 通过遍历空，将对应的答案写入
            elem_data[0].click()
            time.sleep(1)
            # 模拟点击网页，因为在写完空后，不点击网页会有确定按钮为不可点的情况
            elem_next = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="action-row"]/button')))
            elem_next.click()
            retry = False
            DaTi(driver)
        elif '判' in juje:  # 同上，判断题不会直接给出答案，所以只能手动吧
            print("判断题无提示，无法自动完成，拒绝做判断题")
            retry = True
            raise DatiError("拒绝做题")

    except DatiError as e:
        print(e.args)
        if retry:
            driver.execute_script("window.onbeforeunload = function() {};")

            driver.get(url='https://pc.xuexi.cn/points/exam-practice.html')
            DaTi(driver)

    return True


def main():
    executable_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    times = 0
    while True:
        driver = webdriver.Chrome(
            executable_path=executable_path, options=options)
        login_simulation(driver)

        # 开始答题
        print("开始答题！")
        driver.get(url='https://pc.xuexi.cn/points/exam-practice.html')
        if DaTi(driver) == True:
            break
        times += 1
        if times > 3:
            break
        driver.quit()

    watch_videos(driver)
    read_articles(driver)
    print("学习完毕！")
    driver.quit()


if __name__ == '__main__':
    main()

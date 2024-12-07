from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageDraw
import requests
import json

# تحديد المتغيرات الأساسية
BASE_URL_LOGIN = "https://api.imvu.com/login"
BASE_URL_SUBSCRIPTIONS = "https://api.imvu.com/profile/profile-user-376547310/subscriptions?limit=50"
BASE_URL_FOLLOW = "https://api.imvu.com/profile/profile-user-376547310/subscriptions/profile-user-352763477?limit=50"  # مثال على متابعة الحساب

HEADERS = {
    "Host": "api.imvu.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "Accept": "application/json; charset=utf-8",
    "Content-Type": "application/json; charset=UTF-8",
    "sec-ch-ua-mobile": "?0",
    "X-imvu-application": "welcome/1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "https://pt.secure.imvu.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://pt.secure.imvu.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

# بيانات تسجيل الدخول
payload = {
    "username": "conq1@gmail.com",
    "password": "Moammedmax2",
    "gdpr_cookie_acceptance": False,
}

# إرسال طلب تسجيل الدخول
login_response = requests.post(BASE_URL_LOGIN, headers=HEADERS, data=json.dumps(payload))

if login_response.status_code == 200:
    try:
        login_data = login_response.json()
        if login_data.get("status") == "success":
            print("Login successful!")
            
            # الآن قم بالبحث عن الحساب واتباعه
            follow_payload = {
                "id": "https://api.imvu.com/profile/profile-user-352763477"  # هنا يتم تحديد ID الحساب الذي سيتم متابعته
            }

            # إرسال طلب فولو
            follow_response = requests.post(BASE_URL_FOLLOW, headers=HEADERS, data=json.dumps(follow_payload))
            
            if follow_response.status_code == 201:
                print("Successfully followed the user!")
                print("Follow Response:", follow_response.json())
            else:
                print(f"Failed to follow the user. Status code: {follow_response.status_code}")
                print("Response:", follow_response.text)
            
        elif login_data.get("status") == "failure":
            print("Login failed. Details:", login_data)
        else:
            print("Unexpected status:", login_data)
    except json.JSONDecodeError:
        print("Failed to decode response JSON:", login_response.text)
else:
    print(f"Request failed with status code {login_response.status_code}")
    print("Response:", login_response.text)

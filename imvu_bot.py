import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# إعدادات المتصفح
options = Options()
options.add_argument("--headless")  # اختياري: تشغيل بدون واجهة
driver = webdriver.Firefox(options=options)

try:
    # فتح صفحة تسجيل الدخول
    driver.get("https://secure.imvu.com/login/")

    # العثور على حقول البريد الإلكتروني وكلمة المرور
    email_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # إدخال بيانات تسجيل الدخول
    email = "conq1@gmail.com"
    password = "Moammedmax2"      # استبدل هذا بكلمة مرورك
    email_field.send_keys(email)
    password_field.send_keys(password)

    # الضغط على زر تسجيل الدخول
    password_field.send_keys(Keys.RETURN)

    # الانتظار حتى يتم تسجيل الدخول
    time.sleep(5)

    # الانتقال إلى الصفحة المطلوبة
    driver.get("https://www.imvu.com/next/av/L7AJ/")

    # استخراج الكوكيز
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(cookie)

    # إذا كنت تحتاج إلى محتوى الصفحة
    print(driver.page_source)

finally:
    # إغلاق المتصفح
    driver.quit()


# دالة لحفظ التوكن في ملف
def save_token(token):
    with open('token.json', 'w') as file:
        json.dump({"token": token}, file)

# دالة لتحميل التوكن من الملف
def load_token():
    try:
        with open('token.json', 'r') as file:
            data = json.load(file)
            return data["token"]
    except FileNotFoundError:
        return None

# دالة لاستخراج الكوكيز
def extract_cookies(cookies):
    sid = cookies.get("osCsid")
    sn = cookies.get("sncd")
    nm = cookies.get("_imvu_avnm")
    sess = cookies.get("browser_session")
    sess2 = cookies.get("window_session")
    
    return sid, sn, nm, sess, sess2

import requests

# دالة لتسجيل الدخول والحصول على التوكن و sauce
def login(username, password):
    url = "https://api.imvu.com/login"
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)

    if response.status_code == 201:
        # طباعة الاستجابة الكاملة للتحقق من تنسيق البيانات
        response_json = response.json()
        print("استجابة تسجيل الدخول:", response_json)

        # استخراج الـ sauce والتوكن من المسار الصحيح
        login_id = response_json.get("id")
        sauce = response_json.get("denormalized", {}).get(login_id, {}).get("data", {}).get("sauce")
        token = login_id  # التوكن هو الرابط الموجود في "id"
        
        if sauce and token:
            print("تم تسجيل الدخول بنجاح")
            return token, sauce
        else:
            print("لم يتم العثور على التوكن أو sauce في الاستجابة")
            return None, None
    else:
        print(f"حدث خطأ في تسجيل الدخول: {response.status_code}")
        return None, None
import requests

def get_cookies_from_page(url, headers):
    """
    جلب الكوكيز من صفحة معينة.
    """
    session = requests.Session()
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        # استخراج الكوكيز من الاستجابة
        cookies = session.cookies.get_dict()
        print("تم الحصول على الكوكيز بنجاح")
        return cookies
    else:
        print("فشل في الحصول على الكوكيز")
        return None


def follow_user(user_to_follow, token, sauce, sid, sn, nm, sess, sess2):
    """
    دالة متابعة مستخدم مع معطيات إضافية مثل الـ session و الـ sid و الـ sn.
    """
    if not token or not sauce:
        print("التوكن أو السورس غير صالح.")
        return

    # دمج الكوكيز في الهيدر
    cookie_header = f"sid={sid}; sn={sn}; nm={nm}; sess={sess}; sess2={sess2}"
    
    # بناء الهيدرز
    headers = {
        'Accept': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {token}',
        'X-Imvu-Application': 'next_desktop/1',
        'X-Imvu-Sauce': sauce,
        'Cookie': cookie_header,
        'Origin': 'https://www.imvu.com',
        'Referer': 'https://www.imvu.com/next/av/L7AJ/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    }

    # بيانات الطلب
    data = {
        "id": f"https://api.imvu.com/profile/{user_to_follow}"
    }

    # URL طلب المتابعة
    url = "https://api.imvu.com/profile/profile-user-376547310/subscriptions?limit=50"

    # إرسال طلب متابعة المستخدم
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("تمت متابعة المستخدم بنجاح")
    else:
        print(f"حدث خطأ: {response.status_code}")
        print(response.json())

# مثال على كيفية استخدام الكود
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
}

# استبدال URL صفحة الفولو بـ URL الفعلي الذي تحتاجه
url_to_follow_page = "https://www.imvu.com/next/av/L7AJ/"
cookies = get_cookies_from_page(url_to_follow_page, headers)

# مثال للاستخدام
username = "conq1@gmail.com"
password = "Moammedmax2"
user_to_follow = "376547310"  # معرف المستخدم الذي تريد متابعته

# تسجيل الدخول للحصول على التوكن و sauce
token, sauce = login(username, password)

if token and sauce:
    sid = "session_id_example"
    sn = "sncd_example"
    nm = "name_example"
    sess = "browser_session_example"
    sess2 = "window_session_example"
    
    # متابعة المستخدم بعد تسجيل الدخول
    follow_user(user_to_follow, token, sauce, sid, sn, nm, sess, sess2)
else:
    print("فشل تسجيل الدخول، لم يتم متابعة المستخدم.")

import requests
import json

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

# دالة لتسجيل الدخول وجلب التوكن
# دالة لاستخراج الكوكيز
def extract_cookies(cookies):
    sid = cookies.get("osCsid")
    sn = cookies.get("sncd")
    nm = cookies.get("_imvu_avnm")
    sess = cookies.get("browser_session")
    sess2 = cookies.get("window_session")
    
    return sid, sn, nm, sess, sess2

# دالة لتسجيل الدخول وجلب التوكن
def login_and_get_token(username, password):
    login_url = "https://api.imvu.com/login"
    headers = {
        "Content-Type": "application/json"
    }

    # بيانات تسجيل الدخول
    data = {
        "username": username,
        "password": password
    }

    # إرسال الطلب لتسجيل الدخول
    response = requests.post(login_url, json=data, headers=headers)

    # طباعة الاستجابة كاملة لتشخيص الخطأ
    print("استجابة تسجيل الدخول:", response.text)

    # التحقق من الاستجابة
    if response.status_code in [200, 201]:
        try:
            # استخراج التوكن من "denormalized"
            response_data = response.json()
            denormalized_data = response_data.get("denormalized", {})
            
            if denormalized_data:
                sauce = denormalized_data.get("https://api.imvu.com/login", {}).get("data", {}).get("sauce")
                
                if sauce:
                    # استخراج الكوكيز
                    cookies = response.cookies
                    sid, sn, nm, sess, sess2 = extract_cookies(cookies)
                    
                    # حفظ التوكن والكوكيز
                    save_token(sauce)
                    print(f"تم تسجيل الدخول بنجاح وحفظ التوكن: {sauce}")
                    return sauce, sid, sn, nm, sess, sess2
                else:
                    print("لم يتم العثور على التوكن (sauce) في الاستجابة")
                    return None, None, None, None, None, None
            else:
                print("لم يتم العثور على بيانات denormalized في الاستجابة")
                return None, None, None, None, None, None
        except ValueError:
            print("حدث خطأ أثناء قراءة الاستجابة كـ JSON")
            return None, None, None, None, None, None
    else:
        print(f"فشل تسجيل الدخول: {response.status_code}")
        return None, None, None, None, None, None

# دالة لتنفيذ الفولو باستخدام التوكن والكوكيز
def follow_user(user_to_follow, token, sid, sn, nm, sess, sess2):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Cookie': f'osCsid={sid}; sncd={sn}; _imvu_avnm={nm}; browser_session={sess}; window_session={sess2}'
    }

    data = {
        "id": f"https://api.imvu.com/profile/{user_to_follow}"
    }

    url = "https://api.imvu.com/profile/profile-user-376547310/subscriptions?limit=50"

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("تمت متابعة المستخدم بنجاح")
    else:
        print(f"حدث خطأ: {response.status_code}")
        print(response.json())

# استخدام الدوال في التطبيق
username = "conq1@gmail.com"
password = "Moammedmax2"

token, sid, sn, nm, sess, sess2 = login_and_get_token(username, password)

if token:
    follow_user("profile-user-352763477", token, sid, sn, nm, sess, sess2)

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

            # البحث عن التوكن داخل الـ "denormalized" باستخدام المفتاح المتغير
            for key, value in denormalized_data.items():
                sauce = value.get("data", {}).get("sauce")
                
                if sauce:
                    save_token(sauce)  # حفظ التوكن بعد تسجيل الدخول
                    print("تم تسجيل الدخول بنجاح وحفظ التوكن")
                    return sauce
            print("لم يتم العثور على التوكن (sauce) في الاستجابة")
            return None
        except ValueError:
            print("حدث خطأ أثناء قراءة الاستجابة كـ JSON")
            return None
    else:
        print(f"فشل تسجيل الدخول: {response.status_code}")
        return None


# دالة لتنفيذ الفولو باستخدام التوكن المحفوظ
def follow_user(user_to_follow):
    # تحميل التوكن المحفوظ
    token = load_token()

    if token:
        headers = {
            'Authorization': f'Bearer {token}',  # تأكد من تضمين التوكن هنا
            'Content-Type': 'application/json',
        }

        # بناء البيانات المطلوبة للفولو
        data = {
            "id": f"https://api.imvu.com/profile/{user_to_follow}"
        }

        # URL للفولو
        url = "https://api.imvu.com/profile/profile-user-376547310/subscriptions?limit=50"

        # إرسال طلب الفولو
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print("تمت متابعة المستخدم بنجاح")
        else:
            print(f"حدث خطأ: {response.status_code}")
            print(response.json())
    else:
        print("التوكن غير موجود، يرجى تسجيل الدخول أولاً.")
        
# استخدام الدوال في التطبيق
username = "conq1@gmail.com"
password = "Moammedmax2"

# تسجيل الدخول وجلب التوكن
token = login_and_get_token(username, password)

# إذا كان التوكن موجودًا، نفذ الفولو
if token:
    follow_user("profile-user-352763477")  # استبدل بمعرف المستخدم الفعلي

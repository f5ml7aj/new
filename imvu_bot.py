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
                login_data = denormalized_data.get("https://api.imvu.com/login", {})
                sauce = login_data.get("data", {}).get("sauce")
                
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

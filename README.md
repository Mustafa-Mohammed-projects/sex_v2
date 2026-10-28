# 🖼️ معرضي — موقع Django لنشر الصور والفيديوهات

![CI](../../actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-4.2%20%7C%205.x-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

موقع شخصي احترافي لنشر صوري وفيديوهاتي: واجهة عربية RTL، وضع ليلي، بحث وفلترة، عارض صور، دعم يوتيوب، ولوحة تحكم جاهزة. مناسب للنشر على PythonAnywhere.

> ⚠️ لا ترفع ملف `.env` ولا مجلد `media/` ولا `db.sqlite3` إلى GitHub (مستثناة في `.gitignore`).


## تشغيل محلي
```bash
cp .env.example .env   # اختياري
python -m venv venv && source venv/bin/activate   # ويندوز: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
افتح http://127.0.0.1:8000 ولوحة التحكم على /admin/ ، وأضف التصنيفات ثم الصور والفيديوهات.

## النشر على PythonAnywhere
1. ارفع المشروع (zip من تبويب Files ثم `unzip`) إلى `/home/USERNAME/mysite`.
2. في Bash console:
```bash
cd ~/mysite
mkvirtualenv --python=/usr/bin/python3.10 siteenv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```
3. تبويب **Web** ← Add a new web app ← Manual configuration ← اختر نفس نسخة بايثون.
4. **Virtualenv**: `/home/USERNAME/.virtualenvs/siteenv`
5. **Source/Working directory**: `/home/USERNAME/mysite`
6. افتح ملف WSGI واستبدل محتواه بـ:
```python
import os, sys
path = '/home/USERNAME/mysite'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ['DJANGO_DEBUG'] = '0'
os.environ['DJANGO_SECRET_KEY'] = 'ضع-مفتاحًا-عشوائيًا-طويلًا'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'USERNAME.pythonanywhere.com'
os.environ['DJANGO_CSRF_ORIGINS'] = 'https://USERNAME.pythonanywhere.com'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
7. في **Static files** أضف:
   - `/static/` ← `/home/USERNAME/mysite/staticfiles`
   - `/media/` ← `/home/USERNAME/mysite/media`
8. اضغط **Reload**.

## ملاحظات
- غيّر اسم الموقع وروابط التواصل من `config/settings.py` (SITE_NAME / SOCIAL_LINKS).
- الحساب المجاني مساحته محدودة (512MB): للفيديوهات الكبيرة استخدم "رابط يوتيوب" بدل الرفع.
- للمنطقة الزمنية عدّل `TIME_ZONE` في الإعدادات.

## الاختبارات
```bash
python manage.py test
```
يتم تشغيلها تلقائيًا عبر GitHub Actions عند كل push.

## الترخيص
MIT — انظر ملف `LICENSE`.

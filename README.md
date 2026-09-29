# أبو رامي AI

تطبيق ذكي متعدد الموديلات + محادثة صوتية + توليد تطبيقات.

الشعار: لسنا الوحيدين، لكن الأفضل بذكاء

## الميزات

- واجهة عربية كاملة RTL
- محادثة صوتية مباشرة
- تبديل تلقائي بين Gemini / Groq / OpenRouter / DeepSeek
- توليد تطبيقات PWA قابلة للتثبيت
- تحديث تلقائي فوري عند تحديث الخادم

## التشغيل

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

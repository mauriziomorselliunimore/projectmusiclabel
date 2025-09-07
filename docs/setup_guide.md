# MyLabel - Setup Guide

## 🛠️ Local Development Setup

### Prerequisites

1. **Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Copy `.env.example` to `.env` and configure:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:pass@localhost:5432/mylabel
   REDIS_URL=redis://localhost:6379/1
   CLOUDINARY_URL=cloudinary://key:secret@name
   ```

4. **Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py populate_db  # Optional: demo data
   ```

## 🚀 Production Deployment

1. **Additional Requirements**
   ```bash
   pip install -r requirements_prod.txt
   ```

2. **Environment Setup**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   CSRF_TRUSTED_ORIGINS=https://your-domain.com
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **SSL Certificate**
   Configure SSL with your hosting provider

## 🧪 Testing

1. **Run Tests**
   ```bash
   python manage.py test
   ```

2. **Coverage Report**
   ```bash
   coverage run manage.py test
   coverage report
   coverage html  # Optional: HTML report
   ```

## 📊 Monitoring Setup

1. **Sentry**
   Add to settings.py:
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-dsn")
   ```

2. **Debug Toolbar**
   ```python
   if DEBUG:
       INSTALLED_APPS += ['debug_toolbar']
       MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
   ```

3. **Logging**
   Ensure logs directory exists:
   ```bash
   mkdir logs
   chmod 755 logs
   ```

## 🔒 Security Checklist

1. **Django Settings**
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Headers Configuration**
   Already configured in middleware

3. **Database Backup**
   ```bash
   python manage.py dumpdata > backup.json
   ```

## 📱 API Documentation

1. **Generate Schema**
   ```bash
   python manage.py spectacular --file schema.yml
   ```

2. **View Documentation**
   - Swagger UI: `/api/swagger/`
   - ReDoc: `/api/redoc/`

## 🎨 Frontend Assets

1. **Compile CSS**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Optimize Images**
   ```bash
   python manage.py optimize_images
   ```

## 🔍 Troubleshooting

1. **Check System**
   ```bash
   python manage.py check --deploy
   ```

2. **Test Email**
   ```bash
   python manage.py send_test_email
   ```

3. **Clear Cache**
   ```bash
   python manage.py clearcache
   ```

## 📈 Performance Tips

1. **Database Optimization**
   ```bash
   python manage.py showmigrations  # Check migrations
   python manage.py dbshell         # Direct DB access
   ```

2. **Cache Warming**
   ```bash
   python manage.py warmup_cache
   ```

3. **Media Optimization**
   ```bash
   python manage.py optimize_images
   ```

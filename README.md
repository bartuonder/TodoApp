# TodoApp (FastAPI)

FastAPI ile yazılmış, **JWT tabanlı kimlik doğrulama** kullanan ve hem **REST API** hem de **Jinja2 + Bootstrap** ile hazırlanmış basit bir web arayüzü sunan Todo uygulaması.

## Özellikler

- **Kullanıcı kayıt / giriş**: `/auth` üzerinden kullanıcı oluşturma, `/auth/token` ile JWT üretimi
- **Todo CRUD**
  - **UI sayfaları**: Todo listeleme / ekleme / düzenleme
  - **API**: Todo listeleme / oluşturma / güncelleme / silme
- **Admin endpoint’leri**: Admin rolü ile tüm todo’ları görme ve silme
- **DB & migration**: SQLAlchemy modelleri + Alembic migration’ları
- **Testler**: `pytest` ile FastAPI `TestClient` testleri

## Teknoloji

- FastAPI, Starlette, Pydantic, Pytest
- SQLAlchemy 2.x
- Alembic
- Jinja2 (templates) + Bootstrap (static)
- Auth: OAuth2 Password Flow (`/auth/token`) + `python-jose` ile JWT

## Proje yapısı (özet)

- `main.py`: FastAPI uygulaması, router’lar, static mount, health endpoint
- `database.py`: SQLAlchemy engine + session (varsayılan SQLite)
- `models.py`: `Users` ve `Todos` tabloları
- `routers/`
  - `auth.py`: login/register sayfaları + token + kullanıcı oluşturma
  - `todos.py`: UI sayfaları + todo API endpoint’leri
  - `admin.py`: admin todo yönetimi
  - `users.py`: kullanıcı bilgisi, şifre ve telefon güncelleme
- `templates/`: Jinja2 HTML dosyaları
- `static/`: CSS/JS (ör. `static/js/base.js`)
- `alembic/` + `alembic.ini`: migration’lar
- `test/`: Pytest testleri

## Kurulum

Python 3.10+ önerilir.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

Bu repo **paket (package) yapısında** olduğu için (`main.py` içinde relative import’lar var), uygulamayı genellikle proje klasörünün **bir üst dizininden** module path ile çalıştırmak en sorunsuz yöntemdir.

### Seçenek A (önerilen): Üst dizinden çalıştırma

```bash
cd ..
uvicorn TodoApp.main:app --reload
```

### Seçenek B: PYTHONPATH ile (repo içinden)

```bash
PYTHONPATH="$(pwd)/.." uvicorn TodoApp.main:app --reload
```

Uygulama ayağa kalkınca:

- Ana yönlendirme: `GET /` → `/todos/todo-page`
- Health check: `GET /healthy` → `{"status": "Healthy"}`

## Web arayüzü akışı

- **Kayıt**: `GET /auth/register-page`
- **Giriş**: `GET /auth/login-page`
  - Form submit olunca tarayıcı `POST /auth/token` çağırır.
  - Dönen `access_token` değeri `access_token=<jwt>` şeklinde **cookie** olarak kaydedilir.
- **Todo sayfası**: `GET /todos/todo-page`

Not: UI tarafında istekler `static/js/base.js` içinde `Authorization: Bearer <token>` header’ı ile yapılır; token cookie’den okunur.

## API (özet)

### Auth

- `POST /auth` (201): kullanıcı oluşturur
- `POST /auth/token` (200): access token döner

### Todos

- `GET /todos` (200): giriş yapmış kullanıcının todo’ları
- `GET /todos/todo/{todo_id}` (200): tek todo
- `POST /todos/todo` (201): todo oluşturma
- `PUT /todos/todo/{todo_id}` (204): todo güncelleme
- `DELETE /todos/todo/{todo_id}` (204): todo silme

### User

- `GET /user` (200): mevcut kullanıcı bilgisi
- `PUT /user/change_password` (204): şifre değiştir
- `PUT /user/phonenumber/{phone_number}` (204): telefon güncelle

### Admin

- `GET /admin/todo` (200): **admin** ise tüm todo’ları getirir
- `DELETE /admin/todo/{todo_id}` (204): **admin** ise herhangi bir todo’yu siler

## Veritabanı ve migration

Varsayılan veritabanı SQLite’tır:

- Uygulama DB: `sqlite:///./todos_app.db` (`database.py`)
- Alembic DB URL: `sqlite:///./todos_app.db` (`alembic.ini`)

Migration komutları:

```bash
alembic upgrade head
```

## Testler

```bash
pytest -q
```

Testler SQLite üzerinde ayrı bir test DB (`testdb.db`) ile çalışacak şekilde override edilmiş fixture’lar içerir.

## Güvenlik / üretim notları

- `routers/auth.py` içinde `SECRET_KEY` sabit (hardcoded). Gerçek ortamda bunu environment variable olarak yönetmeniz önerilir.
- Cookie’de tutulan token için **HttpOnly/Secure/SameSite** gibi ayarlar bu örnek projede uygulanmıyor; üretimde eklenmeli.


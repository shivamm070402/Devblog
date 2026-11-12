# 📝 DevBlog - Technical Blog Platform

A modern technical blog platform built with Django, PostgreSQL, and System Design focused content.

![Python](https://img.shields.io/badge/Python-3.14.0-blue.svg)
![Django](https://img.shields.io/badge/Django-6.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[**Live Demo**](http://127.0.0.1:8000/) | [**Admin Panel**](http://127.0.0.1:8000/admin/) | [**GitHub**](https://github.com/shivamm070402/Devblog)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Database Design](#database-design)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [System Design Posts](#system-design-posts)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🎨 **Modern UI** - Responsive design with dark mode toggle
- 📊 **Reading Progress** - Visual progress bar at top
- 📚 **System Design Content** - Deep-dive technical articles
- 🔍 **Search** - Full-text search across posts
- 📱 **Mobile Responsive** - Works on all devices
- 🌗 **Dark Mode** - Built-in theme switching
- ⚡ **Fast Performance** - Optimized queries and caching
- 📊 **Analytics Ready** - Post metadata and stats
- 🎯 **Categories** - Organized by topic
- 🔒 **Security** - CSRF, XSS, SQL injection protection

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.14 + Django 6.1 |
| **Database** | PostgreSQL (production) / SQLite (development) |
| **Web Framework** | Django (ORM, auth, admin, templates) |
| **Frontend** | HTML5 + Bootstrap 4.6 + Vanilla JavaScript |
| **Icons** | Font Awesome 6.5 |
| **Fonts** | Inter, Playfair Display (Google Fonts) |
| **Deployment** | WSGI (Gunicorn/uWSGI) |

---

## 📸 Screenshots

### Home Page
![Home Page](docs/screenshot-home.png)

### Post Detail
![Post Detail](docs/screenshot-post.png)

### Admin Panel
![Admin Panel](docs/screenshot-admin.png)

### Dark Mode
![Dark Mode](docs/screenshot-dark.png)

---

## 🗄️ Database Design

### ERD
See full database schema in [DevBlog Database Design ERD](https://raw.githubusercontent.com/shivamm070402/Devblog/main/ERD.html)

### Tables

#### auth_user (Django default)
- id (PK)
- username, email (unique)
- password, is_staff, is_active, is_superuser
- date_joined, last_login

#### blog_category
- id (PK)
- name, slug (unique)

#### blog_post
- id (PK)
- title, slug
- author_id (FK → auth_user)
- category_id (FK → blog_category)
- body (TEXT)
- image (optional)
- status (draft/published)
- created_at, updated_at

### Relationships
- **User → Posts**: 1:N (One user writes many posts)
- **Category → Posts**: 1:N (One category has many posts)

---

## 🏗️ Architecture

### System Architecture
![System Architecture](docs/architecture.png)

```
Client → CDN → Django App → PostgreSQL
                         ↓
                      Media Files
```

### Tech Stack Details

| Component | Description |
|-----------|-------------|
| **Django ORM** | Database abstraction, query optimization |
| **Templates** | Jinja2-based HTML rendering |
| **Views** | Request/response logic, filtering |
| **Middleware** | Auth, CSRF, Session management |
| **Static Files** | CSS, JS, images served via CDN |
| **Media Files** | User uploads stored in /media/ |

---

## 📦 Installation

### Prerequisites

- Python 3.14+
- PostgreSQL (optional, for production)
- Git

### Steps

```bash
# 1. Clone repository
git clone https://github.com/shivamm070402/Devblog.git
cd Devblog

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database (SQLite - no setup needed)
# For PostgreSQL:
# createdb homeblog_db
# createuser -s postgres

# 5. Run migrations
python manage.py migrate

# 6. Seed sample data
python manage.py seed_data

# 7. Create superuser
python manage.py createsuperuser

# 8. Start development server
python manage.py runserver

# 9. Open browser
http://127.0.0.1:8000/
```

---

## 🚀 Usage

### Development

```bash
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check

# Run tests
python manage.py test
```

### Data Management

```bash
# Seed system design posts
python manage.py seed_data

# Seed industry news from tech blogs
python manage.py seed_industry_news

# Reset database (warning: deletes all data)
python manage.py seed_data --reset
```

### Admin Panel

1. Navigate to `/admin/`
2. Login with superuser credentials
3. Manage posts, categories, users

---

## 📚 System Design Posts

### Available Categories

| Category | Posts | Description |
|----------|-------|-------------|
| **System Design** | 6 | Load balancing, caching, CAP theorem, sharding, queues, consistent hashing |
| **Security** | 1 | Critical vulnerability management |
| **Technology** | 4 | Django, PostgreSQL, Stripe, Google Cloud, AWS |
| **Sports** | 1 | Test cricket analysis |
| **Health** | 1 | Healthy living tips |
| **Travel** | 1 | Budget travel guides |

### Featured Posts

1. **[Choosing QuePaxa, an Unusual Consensus Algorithm](#)** - Cloudflare's experimental consensus service
2. **[How We Halved DNS Build Delay](#)** - Cloudflare DNS optimization
3. **[Introducing Zero Wire](#)** - Critical vulnerability management
4. **[Sync Real-Time Stripe Data](#)** - Stripe Data Pipeline architecture
5. **[Google Virgo Network](#)** - Scale-out AI data center fabric

---

## 📁 Project Structure

```
Devblog/
├── blog/                     # Django app
│   ├── management/
│   │   └── commands/
│   │       ├── seed_data.py
│   │       └── seed_industry_news.py
│   ├── admin.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── homeblog/                 # Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/                   # Static assets
│   ├── css/
│   │   └── blog.css
│   └── images/
│       ├── logo.svg
│       ├── logo-dark.svg
│       ├── logo-favicon.svg
│       └── cricket.jpg
├── templates/                # Django templates
│   ├── base.html
│   └── blog/
│       ├── post_list.html
│       ├── post_detail.html
│       ├── category_posts.html
│       └── search.html
├── media/                    # User uploads (ignored in git)
├── .github/                  # GitHub config
├── .gitignore
├── requirements.txt
├── db.sqlite3               # SQLite database
├── manage.py
└── README.md
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Install PostgreSQL
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use Gunicorn/UWSGI instead of runserver
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure environment variables

### Quick Deploy

```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn homeblog.wsgi:application -w 4 -b 0.0.0.0:8000
```

### Environment Variables

```bash
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com
export DB_NAME=homeblog_db
export DB_USER=postgres
export DB_PASSWORD=secure_password
export DB_HOST=localhost
export DB_PORT=5432
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `python manage.py test`
5. Commit: `git commit -m 'Add your feature'`
6. Push: `git push origin feature/your-feature`
7. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- Cloudflare, Stripe, AWS, Google Cloud for technical content inspiration
- Bootstrap team for the responsive framework
- Font Awesome for icons

---

## 📞 Contact

**Author:** Shivam Mohite  
**GitHub:** [@shivamm070402](https://github.com/shivamm070402)  
**Repository:** [Devblog](https://github.com/shivamm070402/Devblog)

---

*Built with ❤️ using Python, Django, and PostgreSQL*

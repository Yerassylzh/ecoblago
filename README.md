This is a Django-based web application that provides the opportunity to purchase used goods at a reduced price and shares the remaining food with those in need

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Yerassylzh/ecoblago.git
cd ecoblago
```

### 2. Create and Activate a Virtual Environment
#### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Environment Variables
#### Create .env file in the current directory
```bash
DJANGO_SECRET_KEY=<PUT HERE YOUR SECRET KEY>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1, localhost
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up the Database and load fixtures
```bash
python manage.py migrate
python manage.py loaddata fixtures/data.json
```

### 6. Create a Superuser
#### Create an admin user to access the Django admin interface (if needed).
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

### 8. Access the Project
```bash
http://127.0.0.1:8000/
```

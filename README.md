# 🛒 SmartCommerce AI - AI-Powered E-commerce Platform

SmartCommerce AI is a modern, high-performance e-commerce platform built with **Django**, featuring a personalized **AI Recommendation System** optimized with **Cython** for lightning-fast performance.

---

## 🌟 Key Features

- **🚀 AI-Powered Recommendations**: Personalized product suggestions based on user "likes" and price similarity algorithms.
- **⚡ Performance Optimized**: Core mathematical computations for product similarity are written in **Cython** for near C-level execution speeds.
- **🛍️ Complete Shopping Flow**:
  - Dynamic Product Listing
  - "Like" Feature for personalization
  - Integrated Shopping Cart
  - Seamless Checkout Process
- **📱 Responsive Design**: A clean, modern UI that works across all devices.
- **🛡️ Secure & Scalable**: Built on the robust Django framework with a clean Model-View-Template (MVT) architecture.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 5.x
- **Database**: SQLite (Development)
- **AI/Math**: NumPy, Cython
- **Frontend**: HTML5, Vanilla CSS (Modern Aesthetics)
- **Images**: Pillow

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mayankahuja-pro/ecoomerce-app.git
cd ecoomerce-app
```

### 2. Set up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Compile Cython Modules
To ensure the recommendation engine runs at peak performance, you need to build the Cython extension:
```bash
cd ecommerce/store
python setup.py build_ext --inplace
cd ../..
```

### 5. Run Migrations & Start Server
```bash
cd ecommerce
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser to start shopping!

---

## 🧠 How the AI Works

The recommendation system uses a **Content-Based Filtering** approach:
1. It tracks user interactions (Likes).
2. It calculates the average price range of products the user is interested in.
3. It uses a **Cython-optimized similarity function** to compare candidate product prices against the user's preference profile.
4. It returns the top `N` most relevant products instantly.

---

## 📁 Project Structure

```text
ecommerce/
├── store/
│   ├── recommender.py       # AI Recommendation Logic
│   ├── price_similarity.pyx # Optimized Cython Code
│   ├── setup.py             # Build script for Cython
│   ├── models.py            # Core Database Schemas
│   ├── views.py             # Application logic
│   └── templates/           # UI Layouts
├── ecommerce/               # Project configuration
└── manage.py
```

---

## 👨‍💻 Author
**Mayank Ahuja**

License: MIT

# 📰 News Translation Project

A **Django-based project** that fetches the latest Editorial & Opinion articles from **Dawn** and **China Daily**,  
filters only **recent (today’s)** articles, and translates them into **Urdu** using Google Translate API.

---

## ✨ Features
✅ Scrapes **Dawn Editorial & Opinion** sections  
✅ Detects **relative timestamps** ("hours ago", "minutes ago") and **absolute dates**  
✅ Keeps only **today's articles**  
✅ Translates content **English → Urdu**  
✅ Logs processed articles  

---

## 🛠️ Tech Stack
- 🐍 **Python 3.10+**
- 🌐 **Django**
- 📡 **Requests**
- 🍵 **BeautifulSoup4**
- 🌍 **googletrans**
- 🗄️ **SQLite3** (default Django database)

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/news_trans.git
cd news_trans
2️⃣ Create & activate virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate # on macOS/Linux
3️⃣ Install dependencies

pip install -r requirements.txt
▶️ Usage
Apply migrations

python manage.py migrate
Fetch & translate articles

python manage.py fetch_articles
Run Project
python manage.py runserver
📂 Project Structure
Copy code
news_trans/
│── manage.py
│── requirements.txt
│── README.md
│── newsapp/
│   ├── utils.py
│   ├── models.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── fetch_articles.py
🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to change.

📜 License
This project is open source and available under the MIT License.

👤 Author
Muzalfa













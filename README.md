# PROJECT4_INTERNSHIP-ELEVATE-LABS
Cyber Threat Intelligence Dashboard
# 🔐 Cyber Threat Intelligence Dashboard

A simple **Flask-based web application** to check whether an IP address is **Safe or Malicious** using real-time threat intelligence and a custom blacklist system.

---

## 🚀 Features

* 🔍 IP Address Lookup
* 📊 Threat Score Detection
* 🚨 Malicious / ⚠ Suspicious / ✔ Safe Classification
* 🧠 Smart Detection Logic (based on Abuse score)
* 🗂 Dashboard with Scan History
* 🔐 Admin Panel (Add/Delete Blacklisted IPs)
* 💾 Persistent Storage using SQLite

---

## 🛠 Tech Stack

* Python (Flask)
* SQLite Database
* HTML / CSS
* REST API Integration

---

## 📂 Project Structure

```
project/
│── app.py
│── init_db.py
│── cti.db
│── templates/
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   ├── login.html
│   └── admin.html
```

---

## ⚙️ Setup Instructions

1. Clone the repository

```
git clone <your-repo-link>
cd project
```

2. Install dependencies

```
pip install flask requests
```

3. Create database

```
python init_db.py
```

4. Run the application

```
python app.py
```

5. Open in browser

```
http://127.0.0.1:5000/
```

---

## 🔑 Admin Login

```
Username: admin
Password: admin123
```

---

## 🧪 Usage

* Enter an IP address to check its threat level
* View scan history in the dashboard
* Add malicious IPs manually via admin panel

---

## 📌 Note

* Requires an API key from AbuseIPDB
* Some IP results depend on real-time data

---

## 🎯 Future Improvements

* Graph-based dashboard
* Export reports (CSV)
* Advanced filtering & search
* Multi-user authentication

---

## 👨‍💻 Author

Sharafat Sable

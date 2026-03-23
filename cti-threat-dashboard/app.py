from flask import Flask, render_template, request, redirect, session
import requests
import re
import json
import os

app = Flask(__name__)
app.secret_key = "cti_secret"

API_KEY = "dd2c2bd7ddf255db5afb1a6144fe2f0d445f13fbccccf3f23cce2e9898ec2891d0ee041c742cbb10"


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

SCAN_FILE = "scans.json"
BLACKLIST_FILE = "blacklist.json"


# LOAD / SAVE DATA
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


scan_history = load_data(SCAN_FILE)
blacklist = load_data(BLACKLIST_FILE)


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# CHECK IP
@app.route("/check", methods=["POST"])
def check():

    ip = request.form["ip"]

    # VALIDATION
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return "Enter valid IP (numbers only)"

    score = 0
    country = "Unknown"
    isp = "Unknown"

    # BLACKLIST CHECK (HIGHEST PRIORITY)
    if ip in blacklist:
        result = "Malicious"
        country = "Blacklisted"
        isp = "Blacklisted"
        score = 100

    else:
        try:
            url = "https://api.abuseipdb.com/api/v2/check"

            headers = {
                "Key": API_KEY,
                "Accept": "application/json"
            }

            params = {
                "ipAddress": ip,
                "maxAgeInDays": "90"
            }

            response = requests.get(url, headers=headers, params=params)
            data = response.json()["data"]

            score = data["abuseConfidenceScore"]
            country = data["countryCode"]
            isp = data["isp"]

        except:
            return "API Error or No Internet"

        # 🔥 SMART DETECTION LOGIC
        if score >= 75:
            result = "Malicious"
        elif score >= 30:
            result = "Suspicious"
        elif score > 0:
            result = "Low Risk"
        else:
            result = "Safe"

    # SAVE SCAN
    scan_history.append({
        "ip": ip,
        "country": country,
        "isp": isp,
        "status": result
    })

    save_data(SCAN_FILE, scan_history)

    return render_template(
        "result.html",
        ip=ip,
        country=country,
        isp=isp,
        score=score,
        result=result
    )


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    total = len(scan_history)

    malicious = len([x for x in scan_history if x["status"] == "Malicious"])
    safe = len([x for x in scan_history if x["status"] == "Safe"])

    return render_template(
        "dashboard.html",
        scans=scan_history,
        total=total,
        malicious=malicious,
        safe=safe
    )


# ADMIN LOGIN PAGE
@app.route("/admin_login")
def admin_login():
    return render_template("login.html")


# LOGIN
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin"] = True
        return redirect("/admin")

    return "Invalid Login"


# ADMIN PANEL
@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/admin_login")

    return render_template("admin.html", blacklist=blacklist)


# ADD IP TO BLACKLIST
@app.route("/add_ip", methods=["POST"])
def add_ip():

    ip = request.form["ip"]

    if ip not in blacklist:
        blacklist.append(ip)
        save_data(BLACKLIST_FILE, blacklist)

    return redirect("/admin")


# DELETE IP
@app.route("/delete_ip/<ip>")
def delete_ip(ip):

    if ip in blacklist:
        blacklist.remove(ip)
        save_data(BLACKLIST_FILE, blacklist)

    return redirect("/admin")


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# RUN
if __name__ == "__main__":
    app.run(debug=True)
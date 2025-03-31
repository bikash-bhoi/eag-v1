from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import base64
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Email Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Your email address
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

def get_access_token():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    creds.refresh(Request())
    return creds.token


def summarize_link(url):
    prompt = f"""Summarize the content of this link in 200-250 words: {url} 
    return 3 most relevant wikipedia link with key as the title and value as the link to wikipedia
    at the end return the text as just a json format with summary as a key and links as second key
    with the 3 links in a list"""

    try:
        print(f"""{"*"*100}\nInput prompt\n{"*"*100}\n{prompt}\n{"*"*100}\n""")
        response = model.generate_content(prompt)
        print(f"""{"*"*40}\nResponse from LLM\n{"*"*40}\n{response.text}\n{"*"*40}\n""")
        return response.text
    except Exception as e:
        print(f"Error summarizing link: {e}")
        return "Error Summarizing Link"

def send_email(email_address, link, text):
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email_address
    msg['Subject'] = f"Link Analysis: {link}"
    access_token = get_access_token()
    auth_string = f"user={EMAIL_ADDRESS}\1auth=Bearer {access_token}\1\1"
    auth_string = base64.b64encode(auth_string.encode()).decode()
    start = text.find("{") 
    end = text.rfind("}") 
    if start != -1 and end != -1:
        text = text[start:end+1]
    dic = json.loads(text)
    keywords = dic.get("links", [])
    keywords_fmt = format = "</br></br>    ".join([f"""<a href="{list(kw.values())[0]}">{list(kw.keys())[0]}</a>""" for kw in keywords])
    print("Building Email format")

    html = f"""
    <html>
    <body>

        <table border="1">
            <tr>
                <td>URL</td>
                <td><a href="{link}">{link}</a></td>
            </tr>
            <tr>
                <td>Summary</td>
                <td>{dic.get("summary")}</td>
            </tr>
             <tr>
                <td>Keywords</td>
                <td>{keywords_fmt}</td>
            </tr>
        </table>
    </body>
    </html>
    """

    part = MIMEText(html, 'html')
    msg.attach(part)

    try:
        try:
            print("Starting Oauth")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.docmd("AUTH", "XOAUTH2 " + auth_string)
            server.sendmail(EMAIL_ADDRESS, email_address, msg.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            print(f"Quitting server")
            server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/analyze', methods=['POST'])
def analyze_link():
    data = request.get_json()
    link = data['link']
    email = data['email']

    summary = summarize_link(link)

    send_email(email, link, summary)

    return jsonify({"status": "success", "message": "Email sent!"})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)

def add_scheme_to_url(url):
    # Add a default scheme (http) if missing
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = urlunparse(('http',) + parsed_url[1:])
    return url

def fetch_website_content(url):
    try:
        url = add_scheme_to_url(url)
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching website content: {e}"}

def analyze_website_content(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        
        # Perform analysis here (you can extend this as needed)
        # For simplicity, let's just check for the presence of certain keywords
        suspicious_keywords = ["fraud", "scam", "malicious"]
        has_suspicious_keywords = any(keyword in html_content.lower() for keyword in suspicious_keywords)

        return {"is_fraudulent": has_suspicious_keywords}

    except Exception as e:
        return {"error": f"Error analyzing website content: {e}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_to_analyze = request.form['url']
        website_content = fetch_website_content(url_to_analyze)

        if isinstance(website_content, dict) and 'error' in website_content:
            return render_template('index.html', url=url_to_analyze, result={"error": website_content['error']})

        analysis_result = analyze_website_content(website_content)

        return render_template('index.html', url=url_to_analyze, result=analysis_result)

    return render_template('index.html', url=None, result=None)

if __name__ == '__main__':
    app.run(debug=True)

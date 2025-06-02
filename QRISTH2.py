from flask import Flask, request, render_template_string, redirect, url_for
import os
import qrcode
from io import BytesIO
import base64
import uuid
import webbrowser
import subprocess

app = Flask(__name__)

def generate_unique_code():
    while True:
        code = uuid.uuid4().hex[:32]
        directory = f'mumbers/{code}'
        if not os.path.exists(directory):
            os.makedirs(os.path.join(directory, 'qrcode'), exist_ok=True)
            os.makedirs(os.path.join(directory, 'posts'), exist_ok=True)
            # Generate QR code and save it
            url = url_for('index', mumbers_code=code, _external=True)
            img = qrcode.make(url)
            img.save(os.path.join(directory, 'qrcode', f'{code}.png'))
            return code

@app.route('/', methods=['GET', 'POST'])
def index():
    mumbers_code = request.args.get('mumbers_code', '')
    img_str = ''
    
    if mumbers_code:
        url = url_for('index', mumbers_code=mumbers_code, _external=True)
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
    
    if request.method == 'POST':
        mumbers_code = request.form['mumbers_code']
        visitor_type = request.form['visitor_type']
        activity_name = request.form['activity_name']
        remarks = request.form['remarks']
        
        # Build directories and file paths
        directory = f'mumbers/{mumbers_code}/posts'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, 'mp.md')
        
        # Write to file in append mode
        with open(file_path, 'a') as file:
            file.write(f'Mumbers Code: {mumbers_code}\n')
            file.write(f'Visitor Type: {visitor_type}\n')
            file.write(f'Activity Name: {activity_name}\n')
            file.write(f'Remarks: {remarks}\n')
            file.write('---\n')
        
        # Open user directory
        subprocess.Popen(f'explorer {os.path.abspath(directory)}')
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>QPISTH2</title>
        <style>
          .container { display: flex; }
          .form-container { flex: 1; }
          .qr-container { flex: 1; text-align: center; }
          .button-container button {
            padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;
            }
        </style>
        <link rel="icon" href="https://czxieddan.top/favicon.ico">
      </head>
      <body>
        <div class="container">
          <div class="form-container">
            <h1>Quick Personnel Information Storage Tool(HTML) v2.1.0</h1>
            <h2>Visitor Form</h2>
            <form method="post">
              <div>
                <label for="mumbers_code">Mumbers Code:</label>
                <input type="text" id="mumbers_code" name="mumbers_code" value="{{ mumbers_code }}" required>
              </div>
              <div>
                <label for="visitor_type">Visitor Type:</label>
                <select id="visitor_type" name="visitor_type">
                  <option value="Test Attribute 1">Test 1</option>
                  <option value="Test Attribute 2">Test 2</option>
                  <option value="Test Attribute 3">Test 3</option>
                  <option value="Test Attribute 4">Test 4</option>
                </select>
              </div>
              <div>
                <label for="activity_name">Activity Name:</label>
                <input type="text" id="activity_name" name="activity_name" required>
              </div>
              <div>
                <label for="remarks">Remarks:</label>
                <textarea id="remarks" name="remarks"></textarea>
              </div>
              <button type="submit" style="padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Submit</button>
            </form>
            <h2>Read Posts</h2>
            <form method="get" action="/read">
              <div>
                <label for="read_mumbers_code">Mumbers Code:</label>
                <input type="text" id="mumbers_code" name="mumbers_code" value="{{ mumbers_code }}" required>
              </div>
              <button type="submit" style="padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Read Posts</button>
            </form>
            <h2>Register New Mumbers Code</h2>
            <form method="post" action="/register">
              <button type="submit" style="padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Register</button>
            </form>
          </div>
          <div class="qr-container">
            {% if img_str %}
              <h2>QR Code</h2>
              <img src="data:image/png;base64,{{ img_str }}" alt="QR Code">
            {% endif %}
          </div>
        </div>
      </body>
        <footer id="footer" class="footer">
        <div class="copyright" style="text-align: center;">
        <span>©<a href="https://x.com/CzXieDdan" target="_blank">CzXieDdan</a> & <a href="https://czxieddan.top" target="_blank">czxieddan.top</a></span>
        </div>
        </footer>
    </html>
    ''', mumbers_code=mumbers_code, img_str=img_str)

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        mumbers_code = request.form['mumbers_code']
        url = url_for('index', mumbers_code=mumbers_code, _external=True)
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>QR Code</title>
          </head>
          <body>
            <div class="container">
              <h1>QR Code</h1>
              <img src="data:image/png;base64,{{ img_str }}" alt="QR Code">
              <p>Scan this QR code to fill the form with the mumbers code: {{ mumbers_code }}</p>
            </div>
          </body>
        </html>
        ''', img_str=img_str, mumbers_code=mumbers_code)
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Generate QR Code</title>
      </head>
      <body>
        <div class="container">
          <h1>Generate QR Code</h1>
          <form method="post">
            <div>
              <label for="mumbers_code">Mumbers Code:</label>
              <input type="text" id="mumbers_code" name="mumbers_code" required>
            </div>
            <button type="submit">Generate QR Code</button>
          </form>
        </div>
      </body>
    </html>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mumbers_code = generate_unique_code()
        directory = f'mumbers/{mumbers_code}'
        subprocess.Popen(f'explorer {os.path.abspath(directory)}')
        return redirect(url_for('index', mumbers_code=mumbers_code))
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Register Mumbers Code</title>
      </head>
      <body>
        <div class="container">
          <h1>Register Mumbers Code</h1>
          <form method="post">
            <button type="submit">Register New Mumbers Code</button>
          </form>
        </div>
      </body>
    </html>
    ''')

@app.route('/read', methods=['GET'])
def read():
    mumbers_code = request.args.get('mumbers_code')
    file_path = f'mumbers/{mumbers_code}/posts/mp.md'
    img_str = ''
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        # Generate QR code
        url = url_for('index', mumbers_code=mumbers_code, _external=True)
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
    else:
        content = "No posts found for this Mumbers Code."
    
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Read Posts</title>
        <style>
          .container { display: flex; }
          .content-container { flex: 1; }
          .qr-container { flex: 1; text-align: center; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="content-container">
            <h1>Posts for Mumbers Code: {{ mumbers_code }}</h1>
            <pre>{{ content }}</pre>
            <a href="/">Back to Form</a>
          </div>
          <div class="qr-container">
            {% if img_str %}
              <h2>QR Code</h2>
              <img src="data:image/png;base64,{{ img_str }}" alt="QR Code">
            {% endif %}
          </div>
                       
        </div>
      </body>
    </html>
    ''', mumbers_code=mumbers_code, content=content, img_str=img_str)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
  #QPISTH2 v2.1.0 by @czxieddan 2025.1.20 czxieddan.top
  #The final explanation right belongs to ©czxieddan
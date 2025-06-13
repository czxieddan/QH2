<div align="center">
<!-- Title: -->
  <a href="https://github.com/czxieddan/">
    <img src="https://czxieddan.top/favicon.ico" height="200">
  </a>
  <h1><a href="https://github.com/czxieddan/">CzXieDdan</a> - QH2</h1>
</div>

 # <div align="center"><img src="GIKU.ico" height="200"><div align="center"><a href="https://github.com/czxieddan/QPIST-Quick-Personnel-Information-Storage-Tool/releases/tag/QH2">QH2</a> </div></div>
Quick Personnel Information Storage Tool(HTML) v2.1.0 By _[CzXieDdan](https://x.com/CzXieDdan)_

A **complementary** tool to help manage **large** numbers of people at scale, **quickly** and **lightly**.

## SYNOPISIS

### ENVIRONMENT
[![pypi supported versions](https://img.shields.io/pypi/pyversions/kubernetes.svg)](https://pypi.python.org/pypi/kubernetes)

```
from flask import Flask, request, render_template_string, redirect, url_for
import os
import qrcode
from io import BytesIO
import base64
import uuid
import webbrowser
import subprocess
```

**The above environment needs to be configured.**

### TYPE
You can replace it with your desired attribute by modifying the ‘Test Attribute’.

```
              <div>
                <label for="visitor_type">Visitor Type:</label>
                <select id="visitor_type" name="visitor_type">
                  <option value="Test Attribute 1">Test 1</option>
                  </select>
              </div>
```
Of course, it's stackable
```
                  <option value="Test Attribute 1">Test 1</option>
                  <option value="Test Attribute 2">Test 2</option>
                  <option value="Test Attribute 3">Test 3</option>
                  <option value="Test Attribute 4">Test 4</option>
```
### HOME
When you run a programme you usually come to ‘HOME’.
```
@app.route('/', methods=['GET', 'POST'])
```
### REGISTER
You can use the ‘Register’ button to generate a new mumber.
```
            <h2>Register New Mumbers Code</h2>
            <form method="post" action="/register">
              <button type="submit" style="padding: 10px 20px; background-color: #4395ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">Register</button>
            </form>
```
You can do this in ‘HOME’ or open its own interface.
```
@app.route('/register', methods=['GET', 'POST'])
```
### QR
Generate QR code and save it:
```
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
```
You can do this in ‘HOME’ or open its own interface too.
```
          <div class="qr-container">
            {% if img_str %}
              <h2>QR Code</h2>
              <img src="data:image/png;base64,{{ img_str }}" alt="QR Code">
            {% endif %}
          </div>
```
its own interface:
```
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
# It is associated with ‘generate_unique_code’ and should never be used alone.
```
When you generate a new QR code it will automatically open the directory where it is located, you can remove this effect by deleting it.
```
# Open user directory
        subprocess.Popen(f'explorer {os.path.abspath(directory)}')
```
## READ
for the same reason.
```
@app.route('/read', methods=['GET'])
```
> [!WARNING]
> Incorrect operation may result in data loss at your own risk.

**email**: _czxieddan@czxieddan.top_

[QH2](https://github.com/czxieddan/QPIST-Quick-Personnel-Information-Storage-Tool)

[QRISTHv2.1.0](https://github.com/czxieddan/QPIST-Quick-Personnel-Information-Storage-Tool/releases/tag/QH2) by [@czxieddan](https://www.czxieddan.top) 2025.1.20
The final explanation right belongs to [©czxieddan](https://www.czxieddan.top)

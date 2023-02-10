const express = require('express');
const session = require('express-session')
const crypto = require('crypto');
const https = require('https');
const fs = require('fs');

const app = express();
app.set('view engine', 'ejs');
app.use(express.json({ type: Object }));
app.use(session({
  secret: crypto.randomBytes(16).toString('hex'),
  resave: false,
  saveUninitialized: false,
  cookie:{
    httpOnly: true,
    sameSite: 'none',
    secure: true
  }
}))

const BOT_HOST = process.env.BOT_HOST || 'localhost';
const BOT_PORT = process.env.BOT_PORT || 7777;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '<YOU DONT KNOW THIS>';
const FLAG = process.env.FLAG || 'FLAG{dummyflag}';

const db = new Map();
db.set('admin', {password: crypto.createHash('sha256').update(ADMIN_PASSWORD, 'utf8').digest('hex'), todo: [{checked: 1, text: FLAG}]});
Object.freeze(db.get('admin'));
const csrfSecret = crypto.randomBytes(16).toString('hex');

app.get("/", function (req, res) {
  	let nonce = crypto.randomBytes(16).toString('hex');
    if (req.session.username) return res.redirect('/todo');
    res.render('index', {nonce: crypto.randomBytes(16).toString('hex')})
});

app.get("/todo", function (req, res) {
    if (!req.session.username) return res.redirect('/');
    let salt = crypto.randomBytes(4).toString('hex');
    res.render('todo', {
      nonce: crypto.randomBytes(16).toString('hex'),
      csrfToken: salt + crypto.createHash('md5').update(salt + req.ip + csrfSecret, 'utf8').digest('hex')
    })
});

app.get("/api/todo", function (req, res) {
    if (!req.session.username) return res.json({ error: "Login first!" });
		let username = req.session.username;
    if (!db.has(username)) return res.json({ error: "User doesn't exist!" });

		return res.json(db.get(username).todo);
});

app.get("/api/logout", function (req, res) {
		req.session.destroy();
		return res.redirect('/');
});

app.post("/api/todo", function (req, res) {
    const { todo, csrfToken } = req.body;
    if (typeof csrfToken !== 'string') return res.json({ error: "Invalid csrfToken" });
    let salt = csrfToken.substr(0,8);
    if (csrfToken.substr(8) !== crypto.createHash('md5').update(salt + req.ip + csrfSecret, 'utf8').digest('hex'))
      return res.json({ error: "Invalid csrfToken" });

    if (!req.session.username) return res.json({ error: "Login first!" });
		let username = req.session.username;
    if (!db.has(username)) return res.json({ error: "User doesn't exist!" });
		db.get(username).todo = todo;
    return res.json({ success: true });
});

app.post("/api/register", function (req, res) {
    const { username, password }= req.body;
    if (typeof username !== 'string') return res.json({ error: "Invalid username" });
    if (typeof password !== 'string') return res.json({ error: "Invalid password" });

    if (db.has(username)) return res.json({ error: "User already exist!" });
    const hash = crypto.createHash('sha256').update(password, 'utf8').digest('hex');

    db.set(username, {password: hash, todo: []});
    req.session.username = username;
    return res.json({ success: true });
});

app.post("/api/login", function (req, res) {
    const { username, password }= req.body;
    if (typeof username !== 'string') return res.json({ error: "Invalid username" });
    if (typeof password !== 'string') return res.json({ error: "Invalid password" });

    if (!db.has(username)) return res.json({ error: "User doesn't exist!" });
    const hash = crypto.createHash('sha256').update(password, 'utf8').digest('hex');
    if (db.get(username)?.password !== hash) return res.json({ error: "Wrong password!" });

    req.session.username = username;
    return res.json({ success: true });
});

const net = require('net');

app.post("/api/report", function (req, res) {
    const { url, csrfToken } = req.body;
    if (typeof url !== 'string') return res.send("Invalid URL");
    if (typeof csrfToken !== 'string') return res.send("Invalid csrfToken");
    let salt = csrfToken.substr(0,8);
    if (csrfToken.substr(8) !== crypto.createHash('md5').update(salt + req.ip+ csrfSecret, 'utf8').digest('hex'))
      return res.send("Invalid csrfToken");

    if (!url || !RegExp('^https?://.*$').test(url)) {
        return res.status(400).send('Invalid URL');
    }
    try {
        const client = net.connect(BOT_PORT, BOT_HOST, () => {
            client.write(url)
        })

    		let response = `[+] Sending ${url} to bot:`;
        client.on('data', data => {
            response += data.toString()
            client.end()
        })

        client.on('end', () => res.send(response))
    } catch (e) {
        console.log(e)
        res.status(500).send('Something is wrong...')
    }
});

https.createServer({
  key: fs.readFileSync('/opt/selfsigned.key'),
  cert: fs.readFileSync('/opt/selfsigned.crt')
}, app).listen(443)

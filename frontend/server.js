const express = require("express");
const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");
const mysql = require("mysql2");

const app = express();
const db = mysql.createConnection({ host: "db.buildmart.internal", user: "app", database: "shop" });
const UPLOADS = path.resolve("/srv/uploads");

app.get("/api/customers", (req, res) => {
  db.query(`SELECT id, email FROM customers WHERE city = '${req.query.city}'`, (err, rows) => res.json(rows));
});

app.get("/api/ping", (req, res) => {
  exec("ping -c 1 " + req.query.host, (err, stdout) => res.send(stdout));
});

app.post("/api/calc", express.json(), (req, res) => {
  res.json({ result: eval(req.body.expression) });
});

app.get("/api/reports", (req, res) => {
  fs.readFile(path.join("/srv/reports", req.query.file), "utf8", (err, data) => res.send(data));
});

app.get("/welcome", (req, res) => {
  res.send(`<h1>Welcome ${req.query.name}</h1>`);
});

app.get("/api/v2/customers", (req, res) => {
  db.query("SELECT id, email FROM customers WHERE city = ?", [req.query.city], (err, rows) => res.json(rows));
});

app.get("/api/v2/reports", (req, res) => {
  const target = path.resolve(UPLOADS, String(req.query.file));
  if (!target.startsWith(UPLOADS + path.sep)) return res.status(400).end();
  fs.readFile(target, "utf8", (err, data) => res.send(data));
});

app.listen(3000);

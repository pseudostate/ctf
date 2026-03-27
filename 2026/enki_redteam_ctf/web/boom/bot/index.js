const express = require("express");
const { visit } = require("./bot");

async function handleVisit(req, res) {
  const target = req.body.url;
  if (typeof target !== "string" || !target.startsWith("/")) {
    return res.status(400).json({ error: "url must start with /" });
  }
  try {
    await visit(target);
    return res.json({ ok: true, path: target });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: "visit failed" });
  }
}

const app = express();
app.use(express.json());
app.post("/visit", handleVisit);
app.listen(3001, "0.0.0.0");

const puppeteer = require("puppeteer")

const APP_HOST = "localhost";
const APP_PORT = "3000";
const APP_URL = `http://${APP_HOST}:${APP_PORT}`;
const FLAG = process.env.FLAG ?? "ENKI{redacted}";

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

const visit = async (path) => {
  if (typeof path !== "string" || !path.startsWith("/")) {
    throw new Error("path must start with /");
  }

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.setCookie({
      name: "FLAG",
      value: FLAG,
      domain: APP_HOST,
      httpOnly: true,
      path: "/",
    });
    await page.goto(APP_URL + path);
    await sleep(5 * 1000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await browser.close();
};

module.exports = { visit }

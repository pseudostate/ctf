const express = require("express");
const puppeteer = require("puppeteer");

const app = express();

const BOT_PORT = 3000;
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || "admin";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "REDACTED";

const BASE_URL = `http://leakage:8080`;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

const UUID_SEGMENT = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}";
const MEMO_PATH_REGEX = new RegExp(`^(${UUID_SEGMENT})(?:/(${UUID_SEGMENT}))?$`);

function normalizeMemoPath(rawPath) {
    if (typeof rawPath !== "string" || !rawPath.trim()) {
        throw new Error("path is required.");
    }

    let path = rawPath.trim();
    if (path.startsWith("/")) {
        path = path.slice(1);
    }
    if (path.endsWith("/")) {
        path = path.slice(0, -1);
    }

    if (!MEMO_PATH_REGEX.test(path)) {
        throw new Error("path must be uuid or uuid/uuid.");
    }

    return `/${path}`;
}

async function loginAsAdmin(page) {
    await page.goto(`${BASE_URL}/login`, {
        waitUntil: "networkidle2",
        timeout: 15000,
    });

    await page.waitForSelector('input[name="usernameOrEmail"]', { timeout: 10000 });
    await page.waitForSelector('input[name="password"]', { timeout: 10000 });

    await page.type('input[name="usernameOrEmail"]', ADMIN_USERNAME, { delay: 15 });
    await page.type('input[name="password"]', ADMIN_PASSWORD, { delay: 15 });

    await Promise.all([
        page.click('button[type="submit"]'),
        page.waitForNavigation({ waitUntil: "networkidle2", timeout: 15000 }),
    ]);
}

app.post("/visit", async (req, res) => {
    const rawPath = req.body.path;

    let browser;
    try {
        const memoPath = normalizeMemoPath(rawPath);
        const targetUrl = `${BASE_URL}${memoPath}`;

        browser = await puppeteer.launch({
            headless: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--ignore-certificate-errors",
            ],
        });

        const page = await browser.newPage();
        await loginAsAdmin(page);
        await page.goto(targetUrl, {
            waitUntil: "networkidle2",
            timeout: 15000,
        });
        await sleep(1500);

        res.status(200).send(`Bot visited: ${targetUrl}`);
    } catch (error) {
        res.status(400).send(`Error: ${error.message}`);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
});

app.listen(BOT_PORT, () => {
    console.log(`Bot server running on port ${BOT_PORT}`);
    console.log(`Target base URL: ${BASE_URL}`);
});

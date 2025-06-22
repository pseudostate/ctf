const express = require('express'); 
const session = require('express-session');
const puppeteer = require('puppeteer');
const crypto = require('crypto');

const db = require('./db');

const SAFE_INTEGER = 2**48-1
const adminToken = crypto.randomBytes(64).toString('hex');

const app = express();
const sessionRouter = express.Router();
const noSessionRouter = express.Router();
app.use(express.urlencoded({ extended: true }));

app.use(function(err, req, res, next) {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

hosting_template = `<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    {{CSP}}
                    <title>User made site hosted on our Free Parking Network</title>
                </head>
                <body>
                    <a href="/approve/{{site.id}}/{{site.approveToken}}">Approve this site</a>
                    {{site.html}}
                </body>
                </html>`

app.use(session({ 
    // It holds the secret key for session 
    secret: crypto.randomBytes(16),
  
    // Forces the session to be saved 
    // back to the session store 
    resave: true, 
  
    // Forces a session that is "uninitialized" 
    // to be saved to the store 
    saveUninitialized: true,
})) 

app.use(noSessionRouter);
app.use(sessionRouter);



sessionRouter.use(async function(req, res, next) {
    if (!req.session.returning) {
        // session was just created
        req.session.returning = true;
        let id = crypto.randomInt(1, SAFE_INTEGER);
        req.session.userId = id;
    }

    res.locals.session = req.session;
    next();
})


noSessionRouter.get('/admin/login', async (req, res, next) => {
    let adminToken = req.query.adminToken;

    if (req.query.adminToken !== adminToken) {
        res.send("Token is wrong");
        return;
    }

    req.session.returning = true;
    req.session.userId = 0;
    res.sendStatus(200);
});


noSessionRouter.get('/review/:siteId', async (req, res) => {
    try {
        const browser = await puppeteer.launch({ executablePath: process.env.BROWSER, args: process.env.BROWSER_ARGS.split(',') });
        const page = await browser.newPage();
        await page.goto(`http://localhost:1337/admin/login?adminToken=${adminToken}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        // make sure js execution isn't blocked
        await page.waitForFunction('true');


        await page.goto(`http://localhost:1337/site/${req.params.siteId}`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        // make sure js execution isn't blocked
        await page.waitForFunction('true');
        await browser.close();
        res.send("The review process has been completed.");
    } catch(e) {console.error(e); res.send("internal error :( pls report to admins")}
});

// Upload HTML endpoint
sessionRouter.post('/upload', async (req, res) => {
    const html = req.body.html;
    let headers = req.body.headers;
    if (typeof html !== 'string' || html.length < 1 || html.length > 65536) {
        return res.status(400).json({ error: 'Invalid HTML.' });
    }

    if (typeof headers !== 'string' || headers.length < 1 || headers.length > 65536) {
        return res.status(400).json({ error: 'Invalid headers.' });
    }

    try {
        const owner = req.session.userId;
        const { id } = await db.createSite(html, owner, headers);
        res.redirect(`/site/${id}`);
    } catch (e) {
        res.status(500).json({ error: 'Failed to create site.' });
    }
});

// Serve uploaded HTML with custom headers
sessionRouter.get('/site/:id', async (req, res) => {
    try {
        const site = await db.getSiteById(req.params.id);
        if (!site) return res.status(404).send('Not found');
        
        if (site.headers){
            site.headers.split("\n").forEach(header => {
                const [key, ...rest] = header.split(":");
                const value = rest.join(":");
                if (key && value) {
                    res.setHeader(key.trim(), value.trim());
                }
            });
        }

        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        if ((req.session.userId !== 0 && req.session.userId !== site.owner) && !site.approved) {
            return res.status(403).send('This site is not approved yet. Please wait for admin approval.');
        }
        
        approveToken = "";
        if (req.session.userId === 0) approveToken = site.approveToken;
        CSP = "";
        if (site.approved !== 1) CSP = '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'">';
        console.log(`Serving site ${site.id} with owner ${site.owner} and approved status ${site.approved}`);
        

        html = hosting_template
            .replaceAll("{{site.html}}", site.html || 'NO HTML FOUND')
            .replaceAll("{{site.id}}", site.id || 'NO ID FOUND, how did this even happen?')
            .replaceAll("{{site.approveToken}}", approveToken)
            .replaceAll("{{CSP}}", CSP);

        res.send(html);
    } catch (e) {
        console.error(e);
        res.status(500).send('Internal error');
    }
});

sessionRouter.get("/approve/:siteId/:approveToken", async (req, res) => {
    let siteId = req.params.siteId;
    let approveToken = req.params.approveToken;

    site = await db.getSiteById(siteId);

    // Check if the approveToken is valid
    if (approveToken !== site.approveToken) {
        res.send("Invalid approval token");
        return;
    }

    // Approve the site
    await db.approveSite(siteId);
    res.send("Site approved");
});

// Serve static index.html on /
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/views/index.html');
});


app.listen(1337, () => console.log('listening on http://localhost:1337'));

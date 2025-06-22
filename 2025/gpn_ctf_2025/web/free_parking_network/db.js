const sqlite3 = require("sqlite3").verbose();
const crypto = require("crypto");
const flag = process.env.FLAG || require('fs').readFileSync('/flag', 'utf8') || "GPNCTF{fake_flag}";


const databaseFilename = "./sqlite.db";
const db = new sqlite3.Database(databaseFilename);

const sites = `CREATE TABLE IF NOT EXISTS sites (
    id TEXT PRIMARY KEY NOT NULL,
    approveToken TEXT NOT NULL,
    html TEXT NOT NULL,
    owner integer NOT NULL,
    approved boolean NOT NULL DEFAULT false,
    headers TEXT DEFAULT '' NOT NULL
);`;

db.serialize(() => {
    db.run(sites);
    // Insert a default user site if it doesn't exist
    db.get('SELECT * FROM sites WHERE id = ?', ['flag'], (err, row) => {
        if (!row) {
            const approveToken = crypto.randomBytes(12).toString('hex');
            db.run(
                'INSERT INTO sites (id, approveToken, html, owner, approved, headers) VALUES (?, ?, ?, ?, ?, ?)',
                [
                    'flag',
                    approveToken,
                    `<h1>Welcome to my secret site!</h1><p>Here is your voucher to get always Free Parking: ${flag}</p>`,
                    -1,
                    false,
                    ''
                ]
            );
        }
    });
});


function createSite(html, owner, headers = {}) {
    return new Promise((resolve, reject) => {
        const id = crypto.randomBytes(16).toString('hex');
        const approveToken = crypto.randomBytes(16).toString('hex');
        db.run(
            'INSERT INTO sites (id, approveToken, html, owner, approved, headers) VALUES (?, ?, ?, ?, ?, ?)',

            [id, approveToken, html, owner, false, headers],
            function (err) {
                if (err) return reject(err);
                resolve({ id, approveToken });
            }
        );
    });
}

function getSiteById(id) {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM sites WHERE id = ?', [id], (err, row) => {
            if (err) return reject(err);
            resolve(row);
        });
    });
}

function approveSite(id) {
    return new Promise((resolve, reject) => {
        db.run('UPDATE sites SET approved = 1 WHERE id = ?', [id], function (err) {
            if (err) return reject(err);
            resolve(this.changes > 0);
        });
    });
}

module.exports = {
    db,
    createSite,
    getSiteById,
    approveSite,
};





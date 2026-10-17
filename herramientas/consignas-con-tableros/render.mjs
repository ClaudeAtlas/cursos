// Dibuja en Chromium los tableros que pide requests.json, con el renderer del IDE.
// Uso: node render.mjs <monorepo> <cursos> <exercises.json> <requests.json> <outdir>
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const [mono, cursos, exercisesPath, requestsPath, outdir] = process.argv.slice(2);
const require = createRequire(path.join(mono, 'apps/ide/package.json'));
const { chromium } = require('playwright');

const exercises = JSON.parse(fs.readFileSync(exercisesPath, 'utf8')).exercises;
const requests = JSON.parse(fs.readFileSync(requestsPath, 'utf8'));
fs.mkdirSync(outdir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setContent('<html><body></body></html>');
await page.addScriptTag({ path: path.join(path.dirname(new URL(import.meta.url).pathname), 'harness.js') });
await page.waitForFunction(() => window.ready === true);

const loaded = new Set();
let done = 0;
for (const r of requests) {
    const file = path.join(outdir, `${r.key}.png`);
    if (fs.existsSync(file)) continue;
    const ex = exercises[r.exercise];
    let dressing;
    if (r.mode === 'attire' && ex.attireDir) {
        dressing = ex.attireDir;
        if (!loaded.has(dressing)) {
            const dir = path.join(cursos, ex.attireDir);
            const files = {};
            for (const f of fs.readdirSync(dir)) {
                const full = path.join(dir, f);
                if (fs.statSync(full).isFile()) files[f] = fs.readFileSync(full).toString('base64');
            }
            const problems = await page.evaluate(([id, fl]) => window.loadDressing(id, fl), [dressing, files]);
            if (problems.length) console.log('vestimenta', dressing, problems.slice(0, 3));
            loaded.add(dressing);
        }
    }
    const board = ex.boards[r.board].board;
    const url = await page.evaluate(([b, c, d, l]) => window.renderGrid(b, c, d, l), [board, r.cell, dressing, r.labels ?? false]);
    fs.writeFileSync(file, Buffer.from(url.slice(url.indexOf(',') + 1), 'base64'));
    done++;
}
await browser.close();
console.log('dibujados', done, 'de', requests.length);

// Abre el IDE en el navegador, elige un ejercicio y saca una foto de la consigna.
// Uso: node shoot.mjs <monorepo> <url> <cursos> <salida-prefijo> <curso> <ruta-del-ejercicio>...
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const [mono, url, cursos, prefix, course, ...exercises] = process.argv.slice(2);
const require = createRequire(path.join(mono, 'apps/ide/package.json'));
const { chromium } = require('playwright');

const guides = JSON.parse(fs.readFileSync(path.join(cursos, course, 'guides.json'), 'utf8'));
const where = (exercisePath) => {
    for (const [g, guide] of guides.entries()) {
        const e = guide.exercises.findIndex((each) => each.path === exercisePath);
        if (e >= 0) return [g, e];
    }
    throw new Error(`no está ${exercisePath}`);
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1500, height: 2600 }, locale: 'es-AR' });
page.on('pageerror', (e) => console.log('error:', e.message));
page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('consola:', m.text().slice(0, 300)); });
for (const [n, exercise] of exercises.entries()) {
    const [g, e] = where(exercise);
    await page.goto(url);
    await page.getByLabel('Curso').selectOption(course);
    await page.getByLabel('Guía').selectOption(String(g));
    await page.getByLabel('Ejercicio').selectOption(String(e));
    const consigna = page.getByRole('document', { name: 'Consigna' });
    try {
        await consigna.waitFor({ timeout: 15000 });
    } catch (error) {
        await page.screenshot({ path: `${prefix}-fallo.png` });
        throw error;
    }
    // Que lleguen las imágenes y se dibujen los tableros, con su vestimenta.
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1500);
    const file = `${prefix}-${n + 1}.png`;
    await consigna.screenshot({ path: file });
    const boards = await page.locator('.consigna-tablero-dibujado canvas').count();
    const images = await page.locator('.consigna img').count();
    console.log(file, exercise, 'tableros', boards, 'imágenes', images);
}
await browser.close();

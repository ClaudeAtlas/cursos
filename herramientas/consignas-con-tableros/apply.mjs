// Cambia en las consignas cada captura convertida por los tableros que muestra.
// Uso: node apply.mjs <monorepo> <cursos> <classes.json> <exercises.json> <refs.json> <out-report.json>
import fs from 'node:fs';
import path from 'node:path';

const [mono, cursos, classesPath, exercisesPath, refsPath, reportPath] = process.argv.slice(2);
const { stringifyGbb } = await import(path.join(mono, 'packages/runtime/dist/index.js'));
const classes = JSON.parse(fs.readFileSync(classesPath, 'utf8'));
const exercises = JSON.parse(fs.readFileSync(exercisesPath, 'utf8')).exercises;
const refs = JSON.parse(fs.readFileSync(refsPath, 'utf8')).filter((r) => r.exists);

const report = { converted: [], newGbb: [], removedPng: [] };

for (const [image, v] of Object.entries(classes)) {
    if (v.status !== 'convertida') continue;
    const ex = exercises[v.exercise];
    const base = path.basename(image, path.extname(image));
    const n = v.panels.length;
    const targets = v.panels.map((p, i) => {
        const m = p.match;
        let file = m.board;
        if (file === null) {
            // Un tablero que no es ninguno de los del ejercicio: el final de correr la
            // solución. Va al lado de la captura que reemplaza.
            file = `assets/resources/${base}${n > 1 ? `-${i + 1}` : ''}.gbb`;
            const full = path.join(cursos, v.exercise, file);
            fs.writeFileSync(full, stringifyGbb(ex.boards[m.index].board));
            report.newGbb.push({ file: path.join(v.exercise, file), from: m.from, solution: m.solution });
        }
        const query = m.mode === 'none' && ex.attireDir ? '?vestimenta=ninguna' : '';
        return `${file}${query}`;
    });

    for (const r of refs.filter((each) => each.file === image)) {
        const md = path.join(cursos, r.md);
        const text = fs.readFileSync(md, 'utf8');
        const alt = r.alt;
        const replacement = targets
            .map((t, i) => `![${n > 1 ? `${alt} (${i + 1} de ${n})` : alt}](${t})`)
            .join(' ');
        if (!text.includes(r.match)) {
            console.error('no se encontró', r.match, 'en', r.md);
            continue;
        }
        fs.writeFileSync(md, text.split(r.match).join(replacement));
        report.converted.push({ md: r.md, before: r.match, after: replacement });
    }
}

// Las capturas que ya no nombra ninguna consigna se van: el paquete del IDE las llevaría.
const stillUsed = new Set();
const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        if (e.name === '.git') continue;
        const f = path.join(d, e.name);
        if (e.isDirectory()) walk(f);
        else if (e.name === 'description.md') {
            const text = fs.readFileSync(f, 'utf8');
            for (const r of refs) if (path.join(cursos, r.md) === f && text.includes(r.match)) stillUsed.add(r.file);
        }
    }
};
walk(cursos);
for (const [image, v] of Object.entries(classes)) {
    if (v.status !== 'convertida' || stillUsed.has(image)) continue;
    fs.rmSync(path.join(cursos, image));
    report.removedPng.push(image);
}
fs.writeFileSync(reportPath, JSON.stringify(report, null, 1));
console.log('referencias cambiadas', report.converted.length, 'gbb nuevos', report.newGbb.length, 'png sacados', report.removedPng.length);

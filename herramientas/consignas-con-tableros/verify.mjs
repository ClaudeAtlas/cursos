// Abre con loadActivity cada ejercicio cuya consigna dibuja tableros y cuenta qué trajo.
// Uso: node verify.mjs <monorepo> <cursos>
import fs from 'node:fs';
import path from 'node:path';

const [mono, cursos] = process.argv.slice(2);
const { loadActivity, boardReferencesIn } = await import(path.join(mono, 'packages/courses/dist/index.js'));
const source = {
    file: async (_r, p) => {
        const f = path.join(cursos, p);
        return fs.existsSync(f) && fs.statSync(f).isFile() ? new Uint8Array(fs.readFileSync(f)) : undefined;
    },
    list: async (_r, p) => {
        const f = path.join(cursos, p);
        return fs.existsSync(f) && fs.statSync(f).isDirectory()
            ? fs.readdirSync(f).filter((n) => fs.statSync(path.join(f, n)).isFile())
            : [];
    }
};
const found = [];
const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        if (e.name === '.git') continue;
        const f = path.join(d, e.name);
        if (e.isDirectory()) walk(f);
        else if (e.name === 'description.md') found.push(path.relative(cursos, d));
    }
};
walk(cursos);
let exercises = 0, refs = 0, boards = 0, withAttire = 0;
const problems = [];
for (const dir of found) {
    const text = fs.readFileSync(path.join(cursos, dir, 'description.md'), 'utf8');
    const r = boardReferencesIn(text);
    if (r.length === 0) continue;
    exercises++;
    refs += r.length;
    const a = await loadActivity({ id: dir, name: dir, path: dir, repo: 'x', base: dir.split('/')[0] }, source);
    boards += Object.keys(a.briefBoards).length;
    if (r.some((each) => each.attire.kind === 'exercise') && a.attire) withAttire++;
    for (const p of a.problems) problems.push(`${dir}: ${p}`);
    for (const each of r) if (!a.briefBoards[each.path]) problems.push(`${dir}: falta ${each.path}`);
}
console.log({ exercises, refs, boards, withAttire });
console.log(problems.join('\n'));

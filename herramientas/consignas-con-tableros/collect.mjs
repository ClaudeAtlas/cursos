// Junta, por cada imagen de consigna, el ejercicio: sus tableros (con nombre de archivo) y
// la vestimenta que el IDE le pondría (con la misma lógica: loadActivity).
// Uso: node collect.mjs <monorepo> <cursos> <refs.json> <out.json>
import fs from 'node:fs';
import path from 'node:path';

const [mono, cursos, refsPath, out] = process.argv.slice(2);
const { loadActivity } = await import(path.join(mono, 'packages/courses/dist/index.js'));
const { parseGbb } = await import(path.join(mono, 'packages/runtime/dist/index.js'));
const { run } = await import(path.join(mono, 'packages/runtime/dist/engine.js'));

const REPO = 'local';
const source = {
    file: async (_repo, p) => {
        const full = path.join(cursos, p);
        return fs.existsSync(full) && fs.statSync(full).isFile() ? new Uint8Array(fs.readFileSync(full)) : undefined;
    },
    list: async (_repo, p) => {
        const full = path.join(cursos, p);
        return fs.existsSync(full) && fs.statSync(full).isDirectory() ? fs.readdirSync(full) : [];
    }
};

const refs = JSON.parse(fs.readFileSync(refsPath, 'utf8')).filter((r) => r.exists);
const exercises = new Map();
for (const r of refs) {
    const dir = path.dirname(r.md);
    if (!exercises.has(dir)) exercises.set(dir, []);
    exercises.get(dir).push(r);
}

const byNumber = (a, b) => a.localeCompare(b, undefined, { numeric: true });
const result = { exercises: {} };
// Se puede repartir en varios procesos: SHARD=i/n se queda con uno de cada n ejercicios.
const [shard, shards] = (process.env.SHARD ?? '0/1').split('/').map(Number);
let count = 0;
for (const [dir, rs] of exercises) {
    if (count++ % shards !== shard) continue;
    console.error('ejercicio', count, dir);
    const base = dir.split('/')[0];
    const activity = await loadActivity({ id: dir, name: dir, path: dir, repo: REPO, base }, source);
    const boardsDir = path.join(cursos, dir, 'assets/boards');
    const names = fs.existsSync(boardsDir) ? fs.readdirSync(boardsDir).filter((n) => n.endsWith('.gbb')).sort(byNumber) : [];
    const boards = [];
    for (const n of names) {
        const { board } = parseGbb(fs.readFileSync(path.join(boardsDir, n), 'utf8'));
        if (board) boards.push({ file: `assets/boards/${n}`, board });
    }
    // Los tableros finales: cada solución del ejercicio, corrida sobre cada tablero inicial
    // con la biblioteca del ejercicio. Son los que muestran las capturas de «escenario final».
    const finals = [];
    const solDir = path.join(cursos, dir, 'assets/solutions');
    const solutions = fs.existsSync(solDir) ? fs.readdirSync(solDir).filter((n) => n.endsWith('.gbs')).sort(byNumber) : [];
    const seen = new Set(boards.map((b) => JSON.stringify(b.board)));
    // También el código con el que arranca el ejercicio: en los interactivos —Quell— es el
    // que dibuja el nivel en su INIT, y la captura muestra eso.
    const programs = solutions.map((sol) => [sol, fs.readFileSync(path.join(solDir, sol), 'utf8')]);
    if (activity.code.trim() !== '') programs.push(['content.gbs', activity.code]);
    for (const [sol, code] of programs) {
        for (const initial of boards) {
            const t0 = Date.now();
            const outcome = run(code, { initialBoard: initial.board, library: activity.library, timeoutMs: 3000 });
            const ms = Date.now() - t0;
            if (ms > 500) console.error('lento', ms, dir, sol, initial.file, outcome.diagnostic?.kind);
            // Un interactivo devuelve el tablero después del INIT: es el que se ve al empezar.
            if (!outcome.ok || !outcome.board) continue;
            const key = JSON.stringify(outcome.board);
            if (seen.has(key)) continue;
            seen.add(key);
            finals.push({ file: null, from: initial.file, solution: sol, board: outcome.board });
        }
    }
    boards.push(...finals);
    // La vestimenta: la que encuentra el IDE, o si no la encuentra —el meta.yml la nombra
    // por un nombre que no es el de la carpeta— la carpeta que la tiene, buscada a mano.
    let attireDir;
    let attireFallback = false;
    const metaName = activity.meta.attire ?? activity.meta.inheritedAttires[0];
    if (metaName) {
        const cands = [path.join(dir, 'assets/attires', metaName), path.join(base, 'assets/attires', metaName)];
        attireDir = cands.find((c) => fs.existsSync(path.join(cursos, c, 'config.yml')));
        if (!attireDir) {
            attireFallback = true;
            const norm = (t) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/gi, '').toLowerCase();
            const folders = (d) => (fs.existsSync(path.join(cursos, d)) ? fs.readdirSync(path.join(cursos, d)).map((f) => path.join(d, f)) : []);
            const own = folders(path.join(dir, 'assets/attires'));
            const all = [...own, ...folders(path.join(base, 'assets/attires'))];
            const configName = (d) => (fs.readFileSync(path.join(cursos, d, 'config.yml'), 'utf8').match(/^name:\s*(.+)$/m)?.[1] ?? '').trim();
            attireDir =
                all.find((d) => norm(configName(d)) === norm(metaName)) ??
                all.find((d) => norm(path.basename(d)) === norm(metaName)) ??
                (own.length === 1 ? own[0] : undefined);
        }
    }
    result.exercises[dir] = {
        boards,
        attireDir,
        attireFallback,
        ideAttire: activity.attire?.name,
        metaAttire: activity.meta.attire ?? activity.meta.inheritedAttires[0],
        problems: activity.problems,
        images: [...new Set(rs.map((r) => r.file))]
    };
}
fs.writeFileSync(out, JSON.stringify(result));
const ex = Object.values(result.exercises);
console.log('exercises', ex.length, 'ide attire', ex.filter((e) => e.ideAttire).length, 'metaAttire', ex.filter((e) => e.metaAttire).length, 'attireDir', ex.filter((e) => e.attireDir).length);
console.log('fallbacks', ex.filter((e) => e.attireFallback).map((e) => [e.metaAttire, e.attireDir]));
console.log('finales', ex.reduce((n, e) => n + e.boards.filter((b) => !b.file).length, 0));
console.log('no boards', ex.filter((e) => e.boards.length === 0).length);

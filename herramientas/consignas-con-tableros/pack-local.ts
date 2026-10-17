// Arma el paquete de cursos a partir de una carpeta local (la rama sin publicar), con el
// mismo formato que `pnpm cursos`. Uso: node pack-local.ts <monorepo> <carpeta> <ref> <salida>
import { createHash } from 'node:crypto';
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { basename, extname, join, relative, sep } from 'node:path';

const [mono, dir, ref, out] = process.argv.slice(2);
const { packCourses } = await import(join(mono, 'packages/courses/src/package.ts'));

const READ = new Set(['.json', '.yml', '.yaml', '.gbs', '.gbk', '.gbb', '.gbp', '.md', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']);
const travels = (path: string): boolean =>
    basename(path).toUpperCase().startsWith('LICENSE') || READ.has(extname(path).toLowerCase());

const files: { path: string; bytes: Uint8Array }[] = [];
const walk = (current: string): void => {
    for (const entry of readdirSync(current, { withFileTypes: true })) {
        if (entry.name === '.git') continue;
        const full = join(current, entry.name);
        if (entry.isDirectory()) walk(full);
        else {
            const path = relative(dir, full).split(sep).join('/');
            if (travels(path)) files.push({ path, bytes: readFileSync(full) });
        }
    }
};
walk(dir);
files.sort((a, b) => (a.path < b.path ? -1 : 1));
const hash = (bytes: Uint8Array): string => createHash('sha256').update(bytes).digest('hex').slice(0, 20);
const packed = packCourses(files, hash, { repo: 'ClaudeAtlas/cursos', ref });
rmSync(out, { recursive: true, force: true });
mkdirSync(join(out, 'indices'), { recursive: true });
mkdirSync(join(out, 'archivos'), { recursive: true });
for (const [name, index] of Object.entries(packed.indices)) writeFileSync(join(out, 'indices', `${name}.json`), JSON.stringify(index));
for (const [name, bytes] of Object.entries(packed.archivos)) writeFileSync(join(out, 'archivos', name), bytes as Uint8Array);
const unique = Object.values(packed.archivos as Record<string, Uint8Array>).reduce((s, b) => s + b.length, 0);
console.log(`${files.length} archivos -> ${Object.keys(packed.archivos).length} (${(unique / 1e6).toFixed(1)} MB) en ${out}`);

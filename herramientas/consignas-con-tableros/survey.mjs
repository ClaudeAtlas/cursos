// Relevamiento: qué imágenes referencian las consignas.
import fs from 'node:fs';
import path from 'node:path';
const root = process.argv[2];
const out = [];
const walk = (d) => {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        if (e.name === '.git') continue;
        const f = path.join(d, e.name);
        if (e.isDirectory()) walk(f);
        else if (e.name === 'description.md') out.push(f);
    }
};
walk(root);
const refs = [];
let dataUris = 0;
for (const f of out) {
    const txt = fs.readFileSync(f, 'utf8');
    const dir = path.dirname(f);
    const re = /!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)|<img[^>]*?src=["']([^"']+)["'][^>]*>/g;
    let m;
    while ((m = re.exec(txt))) {
        const src = m[2] ?? m[3];
        if (src.startsWith('data:')) {
            dataUris++;
            continue;
        }
        if (/^https?:/.test(src)) {
            refs.push({ md: path.relative(root, f), src, external: true });
            continue;
        }
        let p;
        try {
            p = path.join(dir, decodeURIComponent(src));
        } catch {
            p = path.join(dir, src);
        }
        refs.push({
            md: path.relative(root, f),
            src,
            match: m[0],
            file: path.relative(root, p),
            exists: fs.existsSync(p),
            alt: m[1] ?? '',
            html: m[3] !== undefined
        });
    }
}
const uniq = new Set(refs.filter((r) => r.exists).map((r) => r.file));
console.log(
    JSON.stringify({
        descriptions: out.length,
        refs: refs.length,
        dataUris,
        external: refs.filter((r) => r.external).length,
        missing: refs.filter((r) => !r.external && !r.exists).length,
        uniqueExisting: uniq.size,
        html: refs.filter((r) => r.html).length
    })
);
const by = {};
for (const x of refs) if (x.exists) (by[x.file.split('/')[0]] ??= new Set()).add(x.file);
for (const k in by) console.log(k, by[k].size);
console.log(refs.filter((x) => !x.external && !x.exists).slice(0, 10));
fs.writeFileSync(process.argv[3], JSON.stringify(refs, null, 1));

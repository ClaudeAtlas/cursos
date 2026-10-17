// Dibuja tableros con el renderer del IDE, para compararlos con las capturas.
// Se empaqueta con esbuild y se carga en Chromium (Playwright).
import { renderBoard, themes } from '../../../../../../../../../home/sawa/workspace/inv/atlas/Gobstones/.claude/worktrees/agent-a2485d7743327f674/packages/board/src/index';
import { loadAttireFiles } from '../../../../../../../../../home/sawa/workspace/inv/atlas/Gobstones/.claude/worktrees/agent-a2485d7743327f674/apps/ide/src/attire';

const dressings = new Map<string, any>();

const fromBase64 = (text: string): Uint8Array => Uint8Array.from(atob(text), (c) => c.charCodeAt(0));

(window as any).loadDressing = async (id: string, files: Record<string, string>): Promise<string[]> => {
    const decoded: Record<string, Uint8Array> = {};
    for (const [k, v] of Object.entries(files)) decoded[k] = fromBase64(v);
    const loaded = await loadAttireFiles(decoded);
    dressings.set(id, loaded.dressing);
    return loaded.problems.map((p: any) => p.message);
};

// Dibuja la grilla sola (sin números), con celdas de `cell` píxeles, y devuelve el PNG.
(window as any).renderGrid = (board: any, cell: number, dressing: string | undefined, labels: boolean): string => {
    const canvas = document.createElement('canvas');
    const pad = 8;
    if (labels) {
        canvas.width = board.width * cell + 200;
        canvas.height = board.height * cell + 200;
    } else {
        canvas.width = board.width * cell + pad * 2;
        canvas.height = board.height * cell + pad * 2;
    }
    renderBoard(canvas, board, {
        theme: themes.light,
        showLabels: labels,
        pixelRatio: 1,
        dressing: dressing === undefined ? undefined : dressings.get(dressing)
    });
    return canvas.toDataURL('image/png');
};
(window as any).ready = true;

#!/bin/bash
# Corre el recolector en 8 procesos y junta lo que dejan.
A9=/tmp/claude-1000/-home-sawa-workspace-inv-atlas-Gobstones/b6db485f-524b-4e09-a55a-6dcfdbf448c1/scratchpad/a9
MONO=/home/sawa/workspace/inv/atlas/Gobstones/.claude/worktrees/agent-a2485d7743327f674
for i in 0 1 2 3 4 5 6 7; do
  SHARD=$i/8 node $A9/tools/collect.mjs $MONO $A9/cursos $A9/refs.json $A9/exercises-$i.json > $A9/collect-$i.log 2>&1 &
done
wait
node -e '
const fs=require("fs");const out={exercises:{}};
for(let i=0;i<8;i++){Object.assign(out.exercises, JSON.parse(fs.readFileSync(process.argv[1]+"/exercises-"+i+".json","utf8")).exercises)}
fs.writeFileSync(process.argv[1]+"/exercises.json", JSON.stringify(out));
const ex=Object.values(out.exercises);
console.log("ejercicios", ex.length, "finales", ex.reduce((n,e)=>n+e.boards.filter(b=>!b.file).length,0));
' $A9

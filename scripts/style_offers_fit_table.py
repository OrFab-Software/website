from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
needle='.offers-fit-row{display:grid;grid-template-columns:minmax(320px,1.8fr) repeat(var(--offer-count,3),minmax(120px,.55fr));background:rgba(242,238,229,.72)}.offers-fit-cell{padding:15px 18px;display:flex;align-items:center;border-left:1px solid rgba(16,36,58,.12)}.offers-fit-cell:first-child{border-left:0}.offers-fit-head{font-weight:850;justify-content:center;text-align:center;background:rgba(242,238,229,.9)}.offers-fit-head:first-child{justify-content:flex-start}'
repl='.offers-fit-row{display:grid;grid-template-columns:minmax(320px,1.8fr) repeat(var(--offer-count,3),minmax(120px,.55fr));background:linear-gradient(180deg,#f3ce77,var(--gold))}.offers-fit-row:first-child{background:var(--blue);color:var(--cream)}.offers-fit-cell{padding:15px 18px;display:flex;align-items:center;border-left:1px solid rgba(16,36,58,.18)}.offers-fit-row:first-child .offers-fit-cell{border-left:1px solid rgba(242,238,229,.22)}.offers-fit-cell:first-child{border-left:0}.offers-fit-head{font-weight:850;justify-content:center;text-align:center;background:transparent;color:inherit}.offers-fit-head:first-child{justify-content:flex-start}'
if needle not in s:
    raise SystemExit('target CSS not found')
s=s.replace(needle,repl,1)
p.write_text(s)

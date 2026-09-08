from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old='.optimization-level{border-radius:16px;padding:18px;border:1px solid rgba(16,36,58,.15);background:rgba(242,238,229,.16)}'
new='.optimization-level{border-radius:16px;padding:18px;border:3px solid var(--blue);background:linear-gradient(180deg,#d8dcdd,var(--silver));box-shadow:0 10px 24px rgba(16,36,58,.10)}'
if old not in s: raise SystemExit('optimization-level style not found')
s=s.replace(old,new,1)
old2='.optimization-level-critical,.optimization-level-structuring,.optimization-level-advanced{border-left:1px solid rgba(16,36,58,.15)}'
new2='.optimization-level-critical,.optimization-level-structuring,.optimization-level-advanced{border-left:3px solid var(--blue)}'
if old2 in s:s=s.replace(old2,new2,1)
p.write_text(s)

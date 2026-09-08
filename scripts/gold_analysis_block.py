from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old='.result-flow{max-width:1120px;margin-top:30px;padding:28px 30px 8px;border-top:0;border-radius:18px;background:var(--cream);color:var(--blue)}.result-flow p{font-size:17px;line-height:1.75;margin:0 0 22px}'
new='.result-flow{max-width:none;width:100%;margin-top:32px;padding:32px 34px 14px;border-top:0;border-radius:22px;background:linear-gradient(180deg,#f1c86f,var(--gold));color:var(--blue);box-shadow:0 10px 28px rgba(4,12,20,.14)}.result-flow p{font-size:17px;line-height:1.75;margin:0 0 22px}.result-flow strong{color:var(--blue)}'
if old not in s: raise SystemExit('result-flow css target not found')
s=s.replace(old,new,1)
p.write_text(s)

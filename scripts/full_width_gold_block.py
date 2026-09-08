from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old='.result-flow{max-width:none;width:100%;margin-top:32px;padding:32px 34px 14px;border-top:0;border-radius:22px;background:linear-gradient(180deg,#f1c86f,var(--gold));color:var(--blue);box-shadow:0 10px 28px rgba(4,12,20,.14)}.result-flow p{font-size:17px;line-height:1.75;margin:0 0 22px}.result-flow strong{color:var(--blue)}'
new='.result-flow{max-width:none;width:calc(100% + 112px);margin:36px -56px 0;padding:40px 56px 22px;border-top:0;border-radius:0;background:linear-gradient(180deg,#f1c86f,var(--gold));color:var(--blue);box-shadow:none}.result-flow p{font-size:17px;line-height:1.75;margin:0 0 22px}.result-flow strong{color:var(--blue)}'
if old not in s: raise SystemExit('result-flow target not found')
s=s.replace(old,new,1)
old='@media(max-width:600px){.question,.map-card,.result-card{padding:22px}'
new='@media(max-width:600px){.question,.map-card,.result-card{padding:22px}.result-flow{width:calc(100% + 44px);margin-left:-22px;margin-right:-22px;padding:30px 22px 14px}'
if old not in s: raise SystemExit('mobile media target not found')
s=s.replace(old,new,1)
p.write_text(s)

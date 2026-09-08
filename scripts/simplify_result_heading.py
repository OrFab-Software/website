from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old="function showResult(){const r=buildResult();$('resultProfileTitle').textContent='Analyse de votre simulation';$('resultProfileText').textContent=r.process;renderPhaseSummary();"
new="function showResult(){const r=buildResult();$('resultProfileTitle').textContent='Votre simulation';$('resultProfileText').textContent='';$('resultProfileText').style.display='none';renderPhaseSummary();"
if old not in s:
    raise SystemExit('showResult target not found')
s=s.replace(old,new,1)
p.write_text(s)

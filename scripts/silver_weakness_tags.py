from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
needle='.analysis-item{background:rgba(242,238,229,.28);border:1px solid rgba(16,36,58,.14);border-radius:14px;padding:16px 18px}'
replacement=needle+'.analysis-section#analysisWeaknessesSection .analysis-item{background:linear-gradient(180deg,#d8dcdd,var(--silver))}'
if needle not in s:
    raise SystemExit('analysis-item CSS target not found')
s=s.replace(needle,replacement,1)
p.write_text(s)

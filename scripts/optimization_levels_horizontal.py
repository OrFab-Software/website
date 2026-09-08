from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
anchor='.optimization-levels{display:grid;gap:18px}'
replacement='.optimization-levels{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;align-items:start}'
if anchor not in s: raise SystemExit('anchor missing')
s=s.replace(anchor,replacement,1)
# keep inner optimization cards in one column inside each priority column
s=s.replace('.optimization-level .analysis-item{background:rgba(242,238,229,.34)}','.optimization-level .analysis-items{grid-template-columns:1fr}.optimization-level .analysis-item{background:var(--blue);color:var(--cream)}.optimization-level .analysis-item strong{color:var(--cream)}.optimization-level .analysis-item p{color:#c7d0d5}',1)
# remove colored vertical priority bars
s=s.replace('.optimization-level-critical{border-left:5px solid #10243a}.optimization-level-structuring{border-left:5px solid #50677a}.optimization-level-advanced{border-left:5px solid rgba(16,36,58,.28)}','.optimization-level-critical,.optimization-level-structuring,.optimization-level-advanced{border-left:1px solid rgba(16,36,58,.15)}',1)
# responsive stacking
marker='@media(max-width:800px)'
if marker in s:
    s=s.replace(marker,'@media(max-width:1050px){.optimization-levels{grid-template-columns:1fr}}'+marker,1)
p.write_text(s)

from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
# Add a final override so the three priority blocks stay side by side on desktop.
override='''<style id="optimization-horizontal-override">
@media (min-width:701px){
  .optimization-levels{
    display:grid!important;
    grid-template-columns:repeat(3,minmax(0,1fr))!important;
    gap:18px!important;
    align-items:start!important;
  }
  .optimization-level{
    min-width:0!important;
    border-left:1px solid rgba(16,36,58,.15)!important;
  }
  .optimization-level .analysis-items{
    grid-template-columns:1fr!important;
  }
}
@media (max-width:700px){
  .optimization-levels{grid-template-columns:1fr!important}
}
</style>
'''
if 'optimization-horizontal-override' not in s:
    if '</head>' not in s: raise SystemExit('head missing')
    s=s.replace('</head>',override+'</head>',1)
# Ensure the individual optimization cards are blue and remove the old colored left bars.
s=s.replace('.optimization-level .analysis-item{background:rgba(242,238,229,.34)}','.optimization-level .analysis-item{background:var(--blue);color:var(--cream)}.optimization-level .analysis-item strong{color:var(--cream)}.optimization-level .analysis-item p{color:#c7d0d5}',1)
s=s.replace('.optimization-level-critical{border-left:5px solid #10243a}.optimization-level-structuring{border-left:5px solid #50677a}.optimization-level-advanced{border-left:5px solid rgba(16,36,58,.28)}','.optimization-level-critical,.optimization-level-structuring,.optimization-level-advanced{border-left:1px solid rgba(16,36,58,.15)}',1)
p.write_text(s)

from pathlib import Path
p=Path('simulation.html')
s=p.read_text(encoding='utf-8')
anchor='.result-flow{max-width:none;'
css='''.phase-summary-card{grid-template-columns:minmax(250px,300px) minmax(0,1fr)!important}\n.phase-summary-head{padding:30px 30px!important}\n.phase-summary-card .summary-phase{font-size:15px!important;letter-spacing:1.7px!important;margin-bottom:12px!important}\n.phase-summary-card h3{font-size:34px!important;line-height:1.08!important;font-weight:650!important}\n.phase-summary-body{padding:24px 10px!important}\n.phase-summary-row{padding:8px 18px 16px!important}\n.phase-summary-row h4{font-size:18px!important;line-height:1.3!important;margin-bottom:11px!important;font-weight:900!important;color:var(--blue)!important}\n.phase-summary-row li{font-size:20px!important;line-height:1.5!important;margin:4px 0!important;font-weight:540!important;color:#17344e!important}\n'''
if css.strip() not in s:
    i=s.find(anchor)
    if i<0: raise SystemExit('anchor not found')
    s=s[:i]+css+s[i:]
p.write_text(s,encoding='utf-8')

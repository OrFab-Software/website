from pathlib import Path
p=Path('simulation.html')
s=p.read_text(encoding='utf-8')
anchor='.result-flow{max-width:none;'
css='''.phase-summary-card .summary-phase{font-size:14px!important;letter-spacing:1.6px!important}\n.phase-summary-card h3{font-size:32px!important;line-height:1.08!important;font-weight:650!important}\n.phase-summary-row h4{font-size:16px!important;line-height:1.35!important;margin-bottom:10px!important;font-weight:900!important}\n.phase-summary-row li{font-size:18px!important;line-height:1.55!important;margin:4px 0!important;font-weight:540!important}\n'''
if css.strip() not in s:
    i=s.find(anchor)
    if i<0: raise SystemExit('anchor not found')
    s=s[:i]+css+s[i:]
p.write_text(s,encoding='utf-8')

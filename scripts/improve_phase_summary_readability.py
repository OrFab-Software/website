from pathlib import Path
p=Path('simulation.html')
s=p.read_text(encoding='utf-8')
anchor='.result-flow{max-width:none;'
css='''.phase-summary-head{padding:28px 28px!important}\n.phase-summary-card .summary-phase{font-size:13px!important;letter-spacing:1.5px!important;margin-bottom:10px!important}\n.phase-summary-card h3{font-size:29px!important;line-height:1.08!important;font-weight:600!important}\n.phase-summary-body{padding:22px 12px!important}\n.phase-summary-row{padding:7px 20px 14px!important}\n.phase-summary-row h4{font-size:14px!important;line-height:1.35!important;margin-bottom:9px!important;color:var(--blue)!important;font-weight:900!important}\n.phase-summary-row ul{padding-left:20px!important}\n.phase-summary-row li{font-size:15px!important;line-height:1.5!important;margin:3px 0!important;color:#17344e!important;font-weight:520!important}\n'''
if css.strip() not in s:
    i=s.find(anchor)
    if i<0: raise SystemExit('anchor not found')
    s=s[:i]+css+s[i:]
p.write_text(s,encoding='utf-8')

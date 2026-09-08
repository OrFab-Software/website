from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old=".phase-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:32px;padding:18px;background:var(--blue);border-radius:22px}.phase-summary-card{border:1px solid rgba(16,36,58,.18);border-radius:18px;padding:20px;background:var(--silver);color:var(--blue)}.phase-summary-card .summary-phase{display:block;color:#9b6c18;font-size:11px;font-weight:850;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:5px}.phase-summary-card h3{font-size:22px;margin:0 0 12px}.phase-summary-row{padding:9px 0;border-top:1px solid rgba(16,36,58,.12)}.phase-summary-row:first-of-type{border-top:0;padding-top:0}.phase-summary-row h4{font-size:12px;line-height:1.35;margin:0 0 7px;color:#50677a;font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif;font-weight:800}.phase-summary-row ul{margin:0;padding-left:18px}.phase-summary-row li{font-size:13px;line-height:1.4;margin:2px 0}"
new=".phase-summary{display:grid;grid-template-columns:1fr;gap:16px;margin-top:32px;padding:18px;background:var(--blue);border-radius:22px}.phase-summary-card{border:1px solid rgba(16,36,58,.18);border-radius:18px;padding:20px 24px;background:var(--silver);color:var(--blue);display:grid;grid-template-columns:minmax(170px,220px) minmax(0,1fr);column-gap:28px;align-items:start}.phase-summary-card .summary-phase{display:block;color:#9b6c18;font-size:11px;font-weight:850;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:5px;grid-column:1}.phase-summary-card h3{font-size:22px;margin:0;grid-column:1}.phase-summary-card .phase-summary-row{grid-column:2;display:grid;grid-template-columns:minmax(150px,220px) minmax(0,1fr);column-gap:18px;align-items:start;padding:8px 0;border-top:1px solid rgba(16,36,58,.12)}.phase-summary-card .phase-summary-row:nth-of-type(1){border-top:0;padding-top:0}.phase-summary-row h4{font-size:12px;line-height:1.35;margin:0;color:#50677a;font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif;font-weight:800}.phase-summary-row ul{margin:0;padding-left:18px}.phase-summary-row li{font-size:13px;line-height:1.4;margin:2px 0}"
if old not in s:
    raise SystemExit('summary css target not found')
s=s.replace(old,new,1)
old_media="@media(max-width:1100px){.grid{grid-template-columns:1fr}.map-card{position:relative;top:auto}.diagnostic-tree,.phase-summary{grid-template-columns:repeat(2,minmax(0,1fr))}}"
new_media="@media(max-width:1100px){.grid{grid-template-columns:1fr}.map-card{position:relative;top:auto}.diagnostic-tree{grid-template-columns:repeat(2,minmax(0,1fr))}.phase-summary{grid-template-columns:1fr}.phase-summary-card{grid-template-columns:1fr}.phase-summary-card .summary-phase,.phase-summary-card h3,.phase-summary-card .phase-summary-row{grid-column:1}.phase-summary-card h3{margin-bottom:12px}.phase-summary-card .phase-summary-row{grid-template-columns:minmax(150px,220px) minmax(0,1fr)}}"
if old_media not in s:
    raise SystemExit('1100 media target not found')
s=s.replace(old_media,new_media,1)
old_mobile="@media(max-width:600px){.question,.map-card,.result-card{padding:22px}.diagnostic-tree,.phase-summary{grid-template-columns:1fr}.diagnostic-toggle{width:100%;margin-left:0;justify-content:flex-start}"
new_mobile="@media(max-width:600px){.question,.map-card,.result-card{padding:22px}.diagnostic-tree,.phase-summary{grid-template-columns:1fr}.phase-summary-card{padding:18px}.phase-summary-card .phase-summary-row{grid-template-columns:1fr}.phase-summary-row h4{margin-bottom:5px}.diagnostic-toggle{width:100%;margin-left:0;justify-content:flex-start}"
if old_mobile not in s:
    raise SystemExit('600 media target not found')
s=s.replace(old_mobile,new_mobile,1)
p.write_text(s)

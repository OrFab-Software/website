from pathlib import Path
import re
p=Path('simulation.html')
s=p.read_text()
# Replace plans container with CTA
s=s.replace('<div class="offers-fit-plans" id="offersFitPlans"></div>','<div class="offers-fit-cta-wrap"><a class="offers-fit-cta" id="offersFitCall" href="#" aria-disabled="true">Programmer un appel visio gratuit — 30 min</a></div>',1)
# Add CTA CSS
anchor='.offers-fit-plan.signature h3,.offers-fit-plan.signature strong{color:var(--cream)}'
css='''.offers-fit-cta-wrap{display:flex;justify-content:center;margin-top:22px}.offers-fit-cta{display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 26px;border-radius:18px;background:linear-gradient(180deg,#f3ce77,#d59c35);color:#090a0c;text-decoration:none;font-weight:850;box-shadow:0 8px 20px rgba(16,36,58,.12)}.offers-fit-cta[aria-disabled="true"]{opacity:.55;cursor:not-allowed}'''
if anchor not in s: raise SystemExit('css anchor not found')
s=s.replace(anchor,anchor+css,1)
# Simplify renderer: remove plans dependency and cards generation
s=s.replace("const section=$('offersFitSection'),table=$('offersFitTable'),plans=$('offersFitPlans');\n  if(!section||!table||!plans)return;","const section=$('offersFitSection'),table=$('offersFitTable'),call=$('offersFitCall');\n  if(!section||!table)return;",1)
pattern=r"\n  const recommended=maxFloor===0\?'essentiel':maxFloor===1\?'plus':'signature';.*?plans\.innerHTML=visibleOffers\.map\(o=>`<article class=\"offers-fit-plan .*?join\(''\);"
s2,n=re.subn(pattern,"",s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('plans renderer block not found')
s=s2
# Keep CTA synced with existing booking URL if later configured
needle="section.hidden=false\n}"
replace="""if(call){const booking=$('bookingLink');const href=booking?booking.getAttribute('href'):'#';const disabled=!href||href==='#'||(booking&&booking.getAttribute('aria-disabled')==='true');call.setAttribute('href',disabled?'#':href);call.setAttribute('aria-disabled',disabled?'true':'false');}\n  section.hidden=false\n}"""
if needle not in s: raise SystemExit('section end not found')
s=s.replace(needle,replace,1)
p.write_text(s)

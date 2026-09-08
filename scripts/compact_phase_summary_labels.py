from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
marker='function phaseAnswers(phase){'
if marker not in s:
    raise SystemExit('phaseAnswers not found')
compact="""function compactSummaryLabel(id,fallback){const labels={channels:'Vos canaux d’entrée',volume:'Volume mensuel',centralized:'Centralisation des informations',centralwhere:'Outil de centralisation',centralmode:'Mode de centralisation',aftercontact:'Après le premier contact',remindertracking:'Suivi des relances',forgotreminder:'Risque d’oubli des relances',conversion:'Passage en client',predocs:'Documents avant engagement',predoclist:'Documents envoyés',predocmode:'Préparation et envoi',transitionactions:'Actions au passage en client',tracking:'Suivi des prestations',recurring:'Actions récurrentes',reentry:'Double saisie',clientdocs:'Documents utilisés',forgotdoc:'Risque d’oubli documentaire',ordered:'Ordre des étapes',deadlines:'Échéances',afterservice:'Après la prestation',reviewauto:'Demande d’avis',followuptime:'Moment du suivi',recallplan:'Planification des relances',recalltime:'Échéance de relance',oldclients:'Identification des anciens clients',newsletterfrequency:'Fréquence de la newsletter'};return labels[id]||fallback}\n"""
if 'function compactSummaryLabel(' not in s:
    s=s.replace(marker,compact+marker,1)
old='rows.push({label:field.title,values})'
new='rows.push({label:compactSummaryLabel(field.id,field.title),values})'
if old not in s:
    raise SystemExit('summary label target not found')
s=s.replace(old,new,1)
p.write_text(s)

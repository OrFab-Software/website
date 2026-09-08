from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old='Voici les offres qui correspondent aux optimisations identifiées dans votre fonctionnement. Seuls les besoins qui vous concernent apparaissent ici.'
new='''<strong>Ces offres sont là pour vous donner un repère.</strong><br>Un CRM OrFab ne se construit jamais sans comprendre précisément votre fonctionnement. Avant toute réalisation, on cartographie donc votre organisation, vos parcours et vos priorités. Cette étape est incluse dans votre projet lorsque vous choisissez de travailler avec OrFab. Le tarif présenté ici reste indicatif : le prix final est confirmé avec vous lors de l’échange visio, une fois votre besoin précisément défini.'''
if old not in s: raise SystemExit('Texte introuvable')
s=s.replace(old,new,1)
p.write_text(s)

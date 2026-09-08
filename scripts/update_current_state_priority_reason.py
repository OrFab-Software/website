from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old="Chaque parcours peut demander des étapes, documents, rappels ou échéances différents ; les traiter exactement de la même manière risque donc de créer des contournements."
new="Vos différents parcours ne suivent pas exactement les mêmes étapes. Aujourd’hui, cela peut compliquer le suivi, augmenter les vérifications et rendre certaines échéances ou actions plus faciles à oublier."
if old not in s:
    raise SystemExit('Texte moteur introuvable')
s=s.replace(old,new,1)
p.write_text(s)

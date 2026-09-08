from pathlib import Path

path = Path('simulation.html')
text = path.read_text(encoding='utf-8')

text = text.replace('<h3>Points forts</h3>', '<h3>Vos points forts</h3>')
text = text.replace('<h3>Points faibles</h3>', '<h3>Vos points d’attention prioritaires</h3>')

marker = '</style>'
css = '''\n/* Mise en valeur des cartes Points forts / Points d’attention prioritaires */\n#analysisStrengthsSection .analysis-item,\n#analysisWeaknessesSection .analysis-item{\n  background:linear-gradient(180deg,#d8dcdd,var(--silver))!important;\n  border:3px solid var(--blue)!important;\n  box-shadow:0 8px 18px rgba(16,36,58,.16);\n}\n'''

if css.strip() not in text:
    if marker not in text:
        raise SystemExit('Balise </style> introuvable')
    text = text.replace(marker, css + marker, 1)

if '<h3>Vos points forts</h3>' not in text:
    raise SystemExit('Titre Vos points forts non appliqué')
if '<h3>Vos points d’attention prioritaires</h3>' not in text:
    raise SystemExit('Titre points d’attention non appliqué')

path.write_text(text, encoding='utf-8')

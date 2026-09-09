from pathlib import Path

path = Path('simulation.html')
html = path.read_text(encoding='utf-8')

marker = "      try{localStorage.setItem('orfab-last-saved-simulation',data.simulationId||submissionId)}catch(e){}"
cleanup = "      try{sessionStorage.removeItem('orfab-simulation-submission-id')}catch(e){}"

if cleanup not in html:
    if marker not in html:
        raise SystemExit('Bloc de succès de la sauvegarde de simulation introuvable')
    html = html.replace(marker, marker + '\n' + cleanup, 1)

path.write_text(html, encoding='utf-8')

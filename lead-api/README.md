# OrFab — API de sauvegarde des simulations

Cette API Cloudflare Worker + D1 reçoit les simulations terminées depuis le site OrFab, les enregistre et les met à disposition du CRM local via une route interne protégée.

## Ce qui est enregistré

- prénom
- nom
- adresse e-mail
- réponses de la simulation
- résultat calculé
- optimisations sélectionnées
- estimation affichée
- date d'enregistrement

Aucune adresse IP n'est stockée par l'application.

## Mise en place Cloudflare

Depuis ce dossier :

```bash
npm install
npx wrangler login
npx wrangler d1 create orfab-simulation-leads --jurisdiction=eu
```

Cloudflare retourne un `database_id`. Copiez ensuite :

```bash
cp wrangler.example.jsonc wrangler.jsonc
```

Puis remplacez `REPLACE_WITH_D1_DATABASE_ID` dans `wrangler.jsonc` par l'identifiant retourné.

Initialisez la base distante :

```bash
npm run db:init:remote
```

Créez ensuite le secret partagé avec le CRM :

```bash
npx wrangler secret put CRM_SYNC_TOKEN
```

Utilisez une valeur longue et aléatoire, par exemple au moins 32 caractères. Cette valeur ne doit jamais être placée dans le site public.

Déployez enfin :

```bash
npm run deploy
```

Wrangler affiche alors l'URL du Worker, par exemple :

```text
https://orfab-simulation-leads.<votre-sous-domaine>.workers.dev
```

Cette URL devra être reportée dans `js/orfab-runtime-config.js` du site.

## Origines autorisées

Par défaut l'exemple autorise :

```text
https://orfab-software.github.io
```

Si le site utilise un domaine personnalisé, ajoutez-le dans `ALLOWED_ORIGINS`, séparé par une virgule :

```json
"ALLOWED_ORIGINS": "https://orfab-software.github.io,https://www.exemple.fr"
```

## Routes

### Publique

`POST /api/simulations`

Reçoit uniquement les données du formulaire et de la simulation. La route applique une validation serveur et une restriction CORS.

### CRM — protégées

`GET /internal/leads?limit=50`

Retourne les simulations pas encore importées dans le CRM.

`POST /internal/leads/:simulationId/ack`

Marque une simulation comme importée.

Ces deux routes exigent :

```text
Authorization: Bearer <CRM_SYNC_TOKEN>
```

## Développement local

```bash
npm run db:init:local
npm run dev
```

Le Worker utilise alors une base D1 locale gérée par Wrangler.

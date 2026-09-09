const JSON_HEADERS = { "Content-Type": "application/json; charset=utf-8" };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";
    const cors = corsHeaders(origin, env);

    if (request.method === "OPTIONS") {
      if (!isAllowedOrigin(origin, env)) return json({ error: "Origin non autorisée" }, 403, cors);
      return new Response(null, { status: 204, headers: cors });
    }

    if (url.pathname === "/health" && request.method === "GET") {
      return json({ ok: true, service: "orfab-simulation-leads" }, 200, cors);
    }

    if (url.pathname === "/api/simulations" && request.method === "POST") {
      if (!isAllowedOrigin(origin, env)) return json({ error: "Origin non autorisée" }, 403, cors);
      return saveSimulation(request, env, cors);
    }

    if (url.pathname === "/internal/leads" && request.method === "GET") {
      if (!isInternalAuthorized(request, env)) return json({ error: "Non autorisé" }, 401, cors);
      return listUnsyncedLeads(url, env, cors);
    }

    const ackMatch = url.pathname.match(/^\/internal\/leads\/([^/]+)\/ack$/);
    if (ackMatch && request.method === "POST") {
      if (!isInternalAuthorized(request, env)) return json({ error: "Non autorisé" }, 401, cors);
      return acknowledgeLead(decodeURIComponent(ackMatch[1]), env, cors);
    }

    return json({ error: "Route introuvable" }, 404, cors);
  },
};

async function saveSimulation(request, env, cors) {
  const contentLength = Number(request.headers.get("Content-Length") || 0);
  if (contentLength > 150_000) return json({ error: "Données trop volumineuses" }, 413, cors);

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "JSON invalide" }, 400, cors);
  }

  // Champ piège anti-bot. On répond comme si tout allait bien sans rien enregistrer.
  if (String(body.companyWebsite || "").trim()) {
    return json({ ok: true, simulationId: crypto.randomUUID() }, 201, cors);
  }

  const firstName = cleanText(body.firstName, 80);
  const lastName = cleanText(body.lastName, 80);
  const email = cleanEmail(body.email);
  const clientSubmissionId = cleanId(body.clientSubmissionId);

  if (!firstName || !lastName || !email || !clientSubmissionId) {
    return json({ error: "Prénom, nom et adresse e-mail valides sont requis." }, 422, cors);
  }

  if (!body.simulation || typeof body.simulation !== "object" || Array.isArray(body.simulation)) {
    return json({ error: "Simulation manquante ou invalide." }, 422, cors);
  }

  const now = new Date().toISOString();
  const emailNormalized = email.toLowerCase();
  const proposedProspectId = crypto.randomUUID();

  await env.DB.prepare(`
    INSERT INTO prospects (
      id, first_name, last_name, email, email_normalized, source, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, 'simulation_site_orfab', ?, ?)
    ON CONFLICT(email_normalized) DO UPDATE SET
      first_name = excluded.first_name,
      last_name = excluded.last_name,
      email = excluded.email,
      updated_at = excluded.updated_at
  `).bind(
    proposedProspectId,
    firstName,
    lastName,
    email,
    emailNormalized,
    now,
    now,
  ).run();

  const prospect = await env.DB.prepare(
    "SELECT id FROM prospects WHERE email_normalized = ? LIMIT 1"
  ).bind(emailNormalized).first();

  if (!prospect?.id) return json({ error: "Impossible d’enregistrer le prospect." }, 500, cors);

  const proposedSimulationId = crypto.randomUUID();
  const simulationJson = safeJson(body.simulation);
  const resultJson = safeJson(body.result || null);
  const selectedJson = safeJson(Array.isArray(body.selectedOptimizations) ? body.selectedOptimizations : []);
  const estimateLabel = cleanText(body.estimateLabel, 120) || null;
  const pageUrl = cleanText(body.pageUrl, 500) || null;
  const noticeVersion = cleanText(body.privacyNoticeVersion, 80) || "2026-09-v1";

  if (!simulationJson || simulationJson.length > 120_000) {
    return json({ error: "La simulation est trop volumineuse." }, 413, cors);
  }

  await env.DB.prepare(`
    INSERT INTO simulations (
      id, client_submission_id, prospect_id, simulation_json, result_json,
      selected_optimizations_json, estimate_label, page_url, privacy_notice_version,
      created_at, updated_at, synced_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
    ON CONFLICT(client_submission_id) DO UPDATE SET
      prospect_id = excluded.prospect_id,
      simulation_json = excluded.simulation_json,
      result_json = excluded.result_json,
      selected_optimizations_json = excluded.selected_optimizations_json,
      estimate_label = excluded.estimate_label,
      page_url = excluded.page_url,
      privacy_notice_version = excluded.privacy_notice_version,
      updated_at = excluded.updated_at,
      synced_at = NULL
  `).bind(
    proposedSimulationId,
    clientSubmissionId,
    prospect.id,
    simulationJson,
    resultJson,
    selectedJson,
    estimateLabel,
    pageUrl,
    noticeVersion,
    now,
    now,
  ).run();

  const simulation = await env.DB.prepare(
    "SELECT id FROM simulations WHERE client_submission_id = ? LIMIT 1"
  ).bind(clientSubmissionId).first();

  return json({ ok: true, simulationId: simulation?.id || proposedSimulationId }, 201, cors);
}

async function listUnsyncedLeads(url, env, cors) {
  const requestedLimit = Number(url.searchParams.get("limit") || 50);
  const limit = Number.isFinite(requestedLimit) ? Math.min(Math.max(Math.trunc(requestedLimit), 1), 100) : 50;

  const { results = [] } = await env.DB.prepare(`
    SELECT
      s.id AS simulation_id,
      s.client_submission_id,
      s.simulation_json,
      s.result_json,
      s.selected_optimizations_json,
      s.estimate_label,
      s.created_at AS simulation_created_at,
      p.id AS prospect_id,
      p.first_name,
      p.last_name,
      p.email,
      p.source
    FROM simulations s
    JOIN prospects p ON p.id = s.prospect_id
    WHERE s.synced_at IS NULL
    ORDER BY s.created_at ASC
    LIMIT ?
  `).bind(limit).all();

  const items = results.map((row) => ({
    simulationId: row.simulation_id,
    clientSubmissionId: row.client_submission_id,
    createdAt: row.simulation_created_at,
    prospect: {
      id: row.prospect_id,
      firstName: row.first_name,
      lastName: row.last_name,
      email: row.email,
      source: row.source,
    },
    simulation: parseJson(row.simulation_json, {}),
    result: parseJson(row.result_json, null),
    selectedOptimizations: parseJson(row.selected_optimizations_json, []),
    estimateLabel: row.estimate_label,
  }));

  return json({ ok: true, count: items.length, items }, 200, cors);
}

async function acknowledgeLead(simulationId, env, cors) {
  if (!/^[0-9a-f-]{20,64}$/i.test(simulationId)) {
    return json({ error: "Identifiant invalide" }, 422, cors);
  }

  const now = new Date().toISOString();
  const result = await env.DB.prepare(
    "UPDATE simulations SET synced_at = ?, updated_at = ? WHERE id = ? AND synced_at IS NULL"
  ).bind(now, now, simulationId).run();

  return json({ ok: true, updated: Number(result.meta?.changes || 0) }, 200, cors);
}

function isInternalAuthorized(request, env) {
  if (!env.CRM_SYNC_TOKEN) return false;
  return request.headers.get("Authorization") === `Bearer ${env.CRM_SYNC_TOKEN}`;
}

function allowedOrigins(env) {
  return String(env.ALLOWED_ORIGINS || "https://orfab-software.github.io")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
}

function isAllowedOrigin(origin, env) {
  return Boolean(origin) && allowedOrigins(env).includes(origin);
}

function corsHeaders(origin, env) {
  const headers = {
    "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
  if (origin && isAllowedOrigin(origin, env)) headers["Access-Control-Allow-Origin"] = origin;
  return headers;
}

function json(payload, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { ...JSON_HEADERS, ...extraHeaders },
  });
}

function cleanText(value, maxLength) {
  if (value === undefined || value === null) return "";
  return String(value).replace(/[\u0000-\u001F\u007F]/g, " ").trim().slice(0, maxLength);
}

function cleanEmail(value) {
  const email = cleanText(value, 254);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return "";
  return email;
}

function cleanId(value) {
  const id = cleanText(value, 100);
  return /^[A-Za-z0-9_-]{8,100}$/.test(id) ? id : "";
}

function safeJson(value) {
  try {
    return JSON.stringify(value);
  } catch {
    return null;
  }
}

function parseJson(value, fallback) {
  try {
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

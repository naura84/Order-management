const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

async function apiFetch(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Erreur API ${response.status}: ${errorText}`);
  }

  return response.json();
}

export async function getClients(page = 1, pageSize = 10) {
  return apiFetch(`/clients?page=${page}&page_size=${pageSize}`);
}

export async function createClient(data) {
  const response = await fetch(
    `${API_URL}/clients`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json();

    const detail = Array.isArray(error.detail)
      ? error.detail.map((item) => item.msg).join(", ")
      : error.detail;

    throw new Error(
      detail || "Impossible de créer le client."
    );
  }

  return response.json();
}

export async function getCommande(id) {
  return apiFetch(`/commandes/${id}`);
}

export async function getLignesCommande(commandeId) {
  const response = await fetch(
    `${API_URL}/commandes/${commandeId}/lignes`,
    {
      headers: {
        "X-API-Key": API_KEY,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Impossible de récupérer les lignes.");
  }

  return response.json();
}

export async function updateCommande(id, data) {
  const response = await fetch(`${API_URL}/commandes/${id}/statut`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Impossible de modifier la commande.");
  }

  return response.json();
}

export async function createCommande(data) {
  const response = await fetch(
    `${API_URL}/commandes`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json();

    const detail = Array.isArray(error.detail)
      ? error.detail.map((item) => item.msg).join(", ")
      : error.detail;

    throw new Error(
      detail || "Impossible de créer la commande."
    );
  }

  return response.json();
}

export async function createLigneCommande(commandeId, data) {
  const response = await fetch(
    `${API_URL}/commandes/${commandeId}/lignes`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail || "Impossible d'ajouter la ligne."
    );
  }

  return response.json();
}

export async function getCommandes(
  page = 1,
  pageSize = 10,
  filters = {}
) {
  const params = new URLSearchParams({
    page,
    page_size: pageSize,
  });

  if (filters.client_id) {
    params.append("client_id", filters.client_id);
  }

  if (filters.statut) {
    params.append("statut", filters.statut);
  }

  if (filters.montant_min !== undefined && filters.montant_min !== "") {
  params.append("montant_min", filters.montant_min);
  }
  
  if (filters.montant_max !== undefined && filters.montant_max !== "") {
    params.append("montant_max", filters.montant_max);
  }
  console.log("Filtres envoyés :", filters);
  console.log("URL :", `${API_URL}/commandes?${params.toString()}`); 

  const response = await fetch(
    `${API_URL}/commandes?${params.toString()}`,
    {
      headers: {
        "X-API-Key": API_KEY,
      },
    }
  );

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail || "Impossible de récupérer les commandes."
    );
  }

  return response.json();
}

export async function getClientStats(clientId) {
  const response = await fetch(
    `${API_URL}/stats/clients/${clientId}`,
    {
      headers: {
        "X-API-Key": API_KEY,
      },
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.detail || "Impossible de récupérer les statistiques du client."
    );
  }

  return response.json();
}
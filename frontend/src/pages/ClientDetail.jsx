import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import {
  getClients,
  getClientStats,
  getCommandes,
  updateClient,
  deleteClient,
} from "../services/api";

function ClientDetail() {
  const { id } = useParams();

  const [client, setClient] = useState(null);
  const [stats, setStats] = useState(null);
  const [commandes, setCommandes] = useState([]);

  const [isEditing, setIsEditing] = useState(false);
  const [editNom, setEditNom] = useState("");
  const [editEmail, setEditEmail] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);

        const [clientsData, statsData, commandesData] =
          await Promise.all([
            getClients(1, 100),
            getClientStats(id),
            getCommandes(1, 100, { client_id: id }),
          ]);

        const foundClient = clientsData.find(
          (client) => client.id === Number(id)
        );

        setClient(foundClient || null);
        setStats(statsData);
        setCommandes(commandesData.items);
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [id]);

  const formatAmount = (amount) =>
    new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: "EUR",
    }).format(Number(amount));
  
  const handleEdit = () => {
  setEditNom(client.nom);
  setEditEmail(client.email);
  setActionError(null);
  setIsEditing(true);
};

const handleCancelEdit = () => {
  setIsEditing(false);
  setActionError(null);
};

const handleSaveEdit = async () => {
  try {
    setActionLoading(true);
    setActionError(null);

    const updatedClient = await updateClient(id, {
      nom: editNom,
      email: editEmail,
    });

    setClient(updatedClient);
    setIsEditing(false);
  } catch (err) {
    console.error(err);
    setActionError(err.message);
  } finally {
    setActionLoading(false);
  }
};

const handleDelete = async () => {
  if (commandes.length > 0) {
    return;
  }

  const confirmed = window.confirm(
    `Supprimer définitivement le client "${client.nom}" ?`
  );

  if (!confirmed) {
    return;
  }

  try {
    setActionLoading(true);
    setActionError(null);

    await deleteClient(id);

    window.location.href = "/clients";
  } catch (err) {
    console.error(err);
    setActionError(err.message);
  } finally {
    setActionLoading(false);
  }
};

  const formatDate = (date) =>
    new Date(date).toLocaleDateString("fr-FR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });

  if (loading) {
    return (
      <div className="loading">
        Chargement du client...
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-card">
        Impossible de charger le client : {error}
      </div>
    );
  }

  if (!client) {
    return (
      <div className="empty-state">
        Client introuvable.
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <Link to="/clients" className="back-link">
            ← Retour aux clients
          </Link>

          <h1>{client.nom}</h1>

          <p>{client.email}</p>
        </div>

        <div className="client-actions">
          {!isEditing && (
            <>
              <button
                className="secondary-button"
                onClick={handleEdit}
                disabled={actionLoading}
              >
                Modifier
              </button>
          
              {commandes.length === 0 && (
                <button
                  className="danger-button"
                  onClick={handleDelete}
                  disabled={actionLoading}
                >
                  Supprimer
                </button>
              )}
            </>
          )}
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <p className="stat-card-title">
            Commandes
          </p>

          <p className="stat-card-value">
            {stats?.nombre_commandes ?? 0}
          </p>

          <p className="stat-card-description">
            Nombre total de commandes
          </p>
        </div>

        <div className="stat-card">
          <p className="stat-card-title">
            Total dépensé
          </p>

          <p className="stat-card-value">
            {formatAmount(stats?.montant_total ?? 0)}
          </p>

          <p className="stat-card-description">
            Montant cumulé
          </p>
        </div>

        <div className="stat-card">
          <p className="stat-card-title">
            Panier moyen
          </p>

          <p className="stat-card-value">
            {formatAmount(stats?.panier_moyen ?? 0)}
          </p>

          <p className="stat-card-description">
            Moyenne par commande
          </p>
        </div>

        <div className="stat-card">
          <p className="stat-card-title">
            Statut fréquent
          </p>

          <p className="stat-card-value">
            {stats?.statut_plus_frequent || "Aucun"}
          </p>

          <p className="stat-card-description">
            Statut le plus représenté
          </p>
        </div>
      </div>
        
      <div className="detail-card client-info-card">
        <h2>Informations client</h2>

        {actionError && (
          <div className="error-card">
            {actionError}
          </div>
        )}

        {isEditing ? (
          <div className="client-edit-form">
            <div>
              <label htmlFor="nom">Nom</label>
              <input
                id="nom"
                type="text"
                value={editNom}
                onChange={(e) => setEditNom(e.target.value)}
              />
            </div>
        
            <div>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={editEmail}
                onChange={(e) => setEditEmail(e.target.value)}
              />
            </div>
        
            <div className="client-edit-actions">
              <button
                className="primary-button"
                onClick={handleSaveEdit}
                disabled={actionLoading}
              >
                {actionLoading ? "Enregistrement..." : "Enregistrer"}
              </button>
        
              <button
                className="secondary-button"
                onClick={handleCancelEdit}
                disabled={actionLoading}
              >
                Annuler
              </button>
            </div>
          </div>
        ) : (
          <div className="detail-info">
            <div>
              <span>Nom</span>
              <strong>{client.nom}</strong>
            </div>
        
            <div>
              <span>Email</span>
              <strong>{client.email}</strong>
            </div>
        
            <div>
              <span>Client depuis</span>
              <strong>{formatDate(client.date_creation)}</strong>
            </div>
          </div>
        )}
      </div>

      <div className="orders-card">
        <div className="orders-card-header">
          <h2>Commandes du client</h2>
        </div>

        {commandes.length === 0 ? (
          <div className="empty-state">
            Ce client n'a aucune commande.
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Date</th>
                  <th>Montant</th>
                  <th>Statut</th>
                </tr>
              </thead>

              <tbody>
                {commandes.map((commande) => (
                  <tr key={commande.id}>
                    <td>
                      <Link
                        to={`/commandes/${commande.id}`}
                        className="order-link"
                      >
                        #{commande.id}
                      </Link>
                    </td>

                    <td>
                      {formatDate(commande.date_commande)}
                    </td>

                    <td>
                      {formatAmount(commande.montant_total)}
                    </td>

                    <td>
                      <StatusBadge
                        status={commande.statut}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default ClientDetail;
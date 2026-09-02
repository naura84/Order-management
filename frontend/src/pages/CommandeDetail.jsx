import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import {
  getCommande,
  getClients,
  getLignesCommande,
  updateCommande,
} from "../services/api";

function CommandeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [commande, setCommande] = useState(null);
  const [client, setClient] = useState(null);
  const [lignes, setLignes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);

        const [commandeData, clientsData, lignesData] = await Promise.all([
          getCommande(id),
          getClients(1, 100),
          getLignesCommande(id),
        ]);

        setCommande(commandeData);
        setLignes(lignesData);

        const foundClient = clientsData.find(
          (client) => client.id === commandeData.client_id
        );

        setClient(foundClient || null);
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [id]);

  const handleStatusChange = async (newStatus) => {
    try {
      setActionLoading(true);
      setError(null);

      const updatedCommande = await updateCommande(id, {
        statut: newStatus,
      });

      setCommande(updatedCommande);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const formatAmount = (amount) =>
    new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: "EUR",
    }).format(Number(amount));

  const formatDate = (date) =>
    new Date(date).toLocaleDateString("fr-FR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });

  if (loading) {
    return <div className="loading">Chargement de la commande...</div>;
  }

  if (error && !commande) {
    return (
      <div className="error-card">
        Impossible de charger la commande : {error}
      </div>
    );
  }

  if (!commande) {
    return (
      <div className="empty-state">
        Commande introuvable.
      </div>
    );
  }

  const isDraft = commande.statut === "brouillon";

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <Link to="/commandes" className="back-link">
            ← Retour aux commandes
          </Link>

          <h1>Commande #{commande.id}</h1>

          <p>
            Créée le {formatDate(commande.date_commande)}
          </p>
        </div>

        <StatusBadge status={commande.statut} />
      </div>

      {error && (
        <div className="error-card">
          {error}
        </div>
      )}

      <div className="detail-grid">
        <div className="detail-card">
          <h2>Informations client</h2>

          <div className="detail-info">
            <div>
              <span>Nom</span>
              <strong>
                {client ? client.nom : `Client #${commande.client_id}`}
              </strong>
            </div>

            <div>
              <span>Email</span>
              <strong>
                {client ? client.email : "Non disponible"}
              </strong>
            </div>
          </div>
        </div>

        <div className="detail-card">
          <h2>Résumé</h2>

          <div className="detail-info">
            <div>
              <span>Commande</span>
              <strong>#{commande.id}</strong>
            </div>

            <div>
              <span>Montant total</span>
              <strong className="total-amount">
                {formatAmount(commande.montant_total)}
              </strong>
            </div>
          </div>
        </div>
      </div>

      <div className="orders-card">
        <div className="orders-card-header">
          <h2>Lignes de commande</h2>

          {isDraft && (
            <Link
              to={`/commandes/${id}/lignes/nouvelle`}
              className="primary-button"
            >
              + Ajouter une ligne
            </Link>
          )}
        </div>

        {lignes.length === 0 ? (
          <div className="empty-state">
            Aucune ligne dans cette commande.
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Référence</th>
                  <th>Article</th>
                  <th>Quantité</th>
                  <th>Prix unitaire</th>
                  <th>Total</th>
                  {isDraft && <th></th>}
                </tr>
              </thead>

              <tbody>
                {lignes.map((ligne) => {
                  const totalLigne =
                    Number(ligne.quantite) *
                    Number(ligne.prix_unitaire);

                  return (
                    <tr key={ligne.id}>
                      <td>{ligne.reference_article}</td>
                      <td>{ligne.libelle}</td>
                      <td>{ligne.quantite}</td>
                      <td>{formatAmount(ligne.prix_unitaire)}</td>
                      <td>{formatAmount(totalLigne)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="detail-card">
        <h2>Actions</h2>

        <div className="status-actions">
          {commande.statut === "brouillon" && (
            <>
              <button
                className="primary-button"
                onClick={() =>
                  handleStatusChange("confirmée")
                }
                disabled={actionLoading}
              >
                Confirmer
              </button>

              <button
                className="danger-button"
                onClick={() =>
                  handleStatusChange("annulée")
                }
                disabled={actionLoading}
              >
                Annuler
              </button>
            </>
          )}

          {commande.statut === "confirmée" && (
            <>
              <button
                className="primary-button"
                onClick={() =>
                  handleStatusChange("expédiée")
                }
                disabled={actionLoading}
              >
                Marquer comme expédiée
              </button>

              <button
                className="danger-button"
                onClick={() =>
                  handleStatusChange("annulée")
                }
                disabled={actionLoading}
              >
                Annuler
              </button>
            </>
          )}

          {commande.statut === "expédiée" && (
            <button
              className="primary-button"
              onClick={() =>
                handleStatusChange("livrée")
              }
              disabled={actionLoading}
            >
              Marquer comme livrée
            </button>
          )}

          {(commande.statut === "livrée" ||
            commande.statut === "annulée") && (
            <p className="no-actions">
              Aucune action disponible pour cette commande.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default CommandeDetail;
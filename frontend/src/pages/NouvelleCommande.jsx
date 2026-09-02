import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createCommande, getClients } from "../services/api";

function NouvelleCommande() {
  const navigate = useNavigate();

  const [clients, setClients] = useState([]);
  const [clientId, setClientId] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadClients() {
      try {
        setLoading(true);
        setError(null);

        const data = await getClients(1, 100);
        setClients(data);
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadClients();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!clientId) {
      setError("Veuillez sélectionner un client.");
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const commande = await createCommande({
        client_id: Number(clientId),
      });

      navigate(`/commandes/${commande.id}`);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Chargement des clients...</div>;
  }

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <Link to="/commandes" className="back-link">
            ← Retour aux commandes
          </Link>
          <h1>Nouvelle commande</h1>
          <p>Créer une nouvelle commande pour un client.</p>
        </div>
      </div>

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="client_id">Client</label>

            <select
              id="client_id"
              name="client_id"
              value={clientId}
              onChange={(event) => setClientId(event.target.value)}
              required
            >
              <option value="">Sélectionner un client</option>

              {clients.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.nom} — {client.email}
                </option>
              ))}
            </select>
          </div>

          {error && (
            <div className="error-card form-error">
              {error}
            </div>
          )}

          <div className="form-actions">
            <Link to="/commandes" className="secondary-button">
              Annuler
            </Link>

            <button
              type="submit"
              className="primary-button"
              disabled={submitting}
            >
              {submitting ? "Création en cours..." : "Créer la commande"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default NouvelleCommande;
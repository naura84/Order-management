import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { createClient, getClients } from "../services/api";

function Clients() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState(null);

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

  const handleCreateClient = async (e) => {
  e.preventDefault();

  try {
    setCreating(true);
    setCreateError(null);

    const newClient = await createClient({
      nom,
      email,
    });

    setClients((currentClients) => [
      ...currentClients,
      newClient,
    ]);

    setNom("");
    setEmail("");
    setShowForm(false);
      } catch (err) {
        console.error(err);
        setCreateError(err.message);
      } finally {
        setCreating(false);
      }
    };
    
  const formatDate = (date) =>
    new Date(date).toLocaleDateString("fr-FR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });

  if (loading) {
    return <div className="loading">Chargement des clients...</div>;
  }

  if (error) {
    return (
      <div className="error-card">
        Impossible de charger les clients : {error}
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <h1>Clients</h1>
          <p>
            {clients.length} client(s) enregistré(s).
          </p>
        </div>
        
        <button
          className="primary-button"
          onClick={() => {
            setShowForm(!showForm);
            setCreateError(null);
          }}
        >
          {showForm ? "Annuler" : "+ Créer un client"}
        </button>
</div>
          {showForm && (
  <div className="orders-card create-client-card">
    <div className="orders-card-header">
      <h2>Créer un client</h2>
    </div>

    <form onSubmit={handleCreateClient} className="client-form">
      <div className="form-group">
        <label htmlFor="nom">Nom</label>
        <input
          id="nom"
          type="text"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          placeholder="Nom du client"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="client@example.com"
          required
        />
      </div>

      {createError && (
        <div className="error-card">
          {createError}
        </div>
      )}

      <button
        type="submit"
        className="primary-button"
        disabled={creating}
      >
        {creating ? "Création..." : "Créer le client"}
      </button>
    </form>
  </div>
)}
      <div className="orders-card">
        <div className="orders-card-header">
          <h2>Liste des clients</h2>
        </div>

        {clients.length === 0 ? (
          <div className="empty-state">
            Aucun client enregistré.
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nom</th>
                  <th>Email</th>
                  <th>Date de création</th>
                  <th></th>
                </tr>
              </thead>

              <tbody>
                {clients.map((client) => (
                  <tr key={client.id}>
                    <td>#{client.id}</td>
                    <td className="client-name">
                      {client.nom}
                    </td>
                    <td>{client.email}</td>
                    <td>
                      {formatDate(client.date_creation)}
                    </td>
                    <td>
                      <Link
                        to={`/clients/${client.id}`}
                        className="order-link"
                      >
                        Voir
                      </Link>
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

export default Clients;
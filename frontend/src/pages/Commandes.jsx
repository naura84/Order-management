import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import { getCommandes, getClients } from "../services/api";

function Commandes() {
  const [commandes, setCommandes] = useState([]);
  const [clients, setClients] = useState([]);

  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);

  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
  client_id: "",
  statut: "",
  montant_min: "",
  montant_max: "",
  });

  const [appliedFilters, setAppliedFilters] = useState({});

  useEffect(() => {
  async function loadData() {
    try {
      setLoading(true);
      setError(null);

      const [commandesData, clientsData] = await Promise.all([
        getCommandes(page, pageSize, appliedFilters),
        getClients(1, 100),
      ]);

      setCommandes(commandesData.items);
      setTotal(commandesData.total);
      setPages(commandesData.pages);
      setClients(clientsData);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

      loadData();
    }, [page, pageSize, appliedFilters]);

  const getClientName = (clientId) => {
    const client = clients.find((client) => client.id === clientId);

    return client ? client.nom : `Client #${clientId}`;
  };

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
  
    setFilters((current) => ({
      ...current,
      [name]: value,
    }));
  };
  
  const applyFilters = () => {
    setPage(1);
    setAppliedFilters(filters);
  };
  
  const resetFilters = () => {
    const emptyFilters = {
      client_id: "",
      statut: "",
      montant_min: "",
      montant_max: "",
    };
  
    setFilters(emptyFilters);
    setAppliedFilters({});
    setPage(1);
  };
  
  const formatAmount = (amount) =>
    new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: "EUR",
    }).format(Number(amount));

  if (loading) {
    return (
      <div className="dashboard">
        <div className="page-heading">
          <div>
            <h1>Commandes</h1>
            <p>Chargement des commandes...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="page-heading">
          <div>
            <h1>Commandes</h1>
            <p>Impossible de récupérer les commandes.</p>
          </div>
        </div>

        <div className="error-card">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <h1>Commandes</h1>
          <p>{total} commande(s) au total.</p>
        </div>

        <Link to="/commandes/nouvelle" className="primary-button">
          + Nouvelle commande
        </Link>
      </div>

      <div className="filters-card">
  <div className="filter-group">
    <label htmlFor="client_id">Client</label>
    <select
      id="client_id"
      name="client_id"
      value={filters.client_id}
      onChange={handleFilterChange}
    >
      <option value="">Tous les clients</option>

      {clients.map((client) => (
        <option key={client.id} value={client.id}>
          {client.nom}
        </option>
      ))}
    </select>
  </div>

  <div className="filter-group">
    <label htmlFor="statut">Statut</label>
    <select
      id="statut"
      name="statut"
      value={filters.statut}
      onChange={handleFilterChange}
    >
      <option value="">Tous les statuts</option>
      <option value="brouillon">Brouillon</option>
      <option value="confirmée">Confirmée</option>
      <option value="expédiée">Expédiée</option>
      <option value="livrée">Livrée</option>
      <option value="annulée">Annulée</option>
    </select>
  </div>

  <div className="filter-group">
    <label htmlFor="montant_min">Montant min.</label>
    <input
      id="montant_min"
      name="montant_min"
      type="number"
      min="0"
      step="0.01"
      value={filters.montant_min}
      onChange={handleFilterChange}
      placeholder="0.00"
    />
  </div>

  <div className="filter-group">
    <label htmlFor="montant_max">Montant max.</label>
    <input
      id="montant_max"
      name="montant_max"
      type="number"
      min="0"
      step="0.01"
      value={filters.montant_max}
      onChange={handleFilterChange}
      placeholder="0.00"
    />
  </div>

      <button
      type="button"
      className="primary-button"
      onClick={applyFilters}
    >
      Filtrer
    </button>
      
    <button
      type="button"
      className="secondary-button"
      onClick={resetFilters}
    >
      Réinitialiser
    </button>
</div>

      <div className="orders-card">
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Client</th>
                <th>Date</th>
                <th>Montant</th>
                <th>Statut</th>
              </tr>
            </thead>

            <tbody>
              {commandes.length === 0 ? (
                <tr>
                  <td colSpan="5" className="empty-state">
                    Aucune commande trouvée.
                  </td>
                </tr>
              ) : (
                commandes.map((commande) => (
                  <tr key={commande.id}>
                    <td>
                      <Link
                        to={`/commandes/${commande.id}`}
                        className="order-link"
                      >
                        #{commande.id}
                      </Link>
                    </td>

                    <td>{getClientName(commande.client_id)}</td>

                    <td>
                      {new Date(
                        commande.date_commande
                      ).toLocaleDateString("fr-FR")}
                    </td>

                    <td>
                      {formatAmount(commande.montant_total)}
                    </td>

                    <td>
                      <StatusBadge status={commande.statut} />
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {pages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setPage((current) => current - 1)}
            disabled={page === 1}
          >
            ← Précédent
          </button>

          <span>
            Page {page} sur {pages}
          </span>

          <button
            onClick={() => setPage((current) => current + 1)}
            disabled={page === pages}
          >
            Suivant →
          </button>
        </div>
      )}
    </div>
  );
}

export default Commandes;
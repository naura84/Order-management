import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import OrderTable from "../components/OrderTable";
import { getCommandes, getClients } from "../services/api";

function Dashboard() {
  const [clients, setClients] = useState([]);
  const [commandes, setCommandes] = useState([]);
  const [totalCommandes, setTotalCommandes] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  async function loadDashboard() {
    try {
      const commandesData = await getCommandes(1, 100);
      const clientsData = await getClients(1, 100);

      setCommandes(commandesData.items);
      setTotalCommandes(commandesData.total);
      setClients(clientsData);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

      loadDashboard();
    }, []);

  if (loading) {
    return (
      <div className="dashboard">
        <div className="page-heading">
          <div>
            <h1>Dashboard</h1>
            <p>Chargement des données...</p>
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
            <h1>Dashboard</h1>
            <p>Impossible de récupérer les données.</p>
          </div>
        </div>

        <div className="error-card">
          {error}
        </div>
      </div>
    );
  }

  const montantTotal = commandes.reduce(
    (total, commande) => total + Number(commande.montant_total),
    0
  );

  const panierMoyen =
    commandes.length > 0 ? montantTotal / commandes.length : 0;

  const formatAmount = (amount) =>
    new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: "EUR",
    }).format(amount);

  const getClientName = (clientId) => {
  const client = clients.find((client) => client.id === clientId);

  return client ? client.nom : `Client #${clientId}`;
    };

  const latestOrders = commandes.slice(0, 5);

  const ordersForTable = latestOrders.map((commande) => ({
    id: commande.id,
    client: getClientName(commande.client_id),
    date: new Date(commande.date_commande).toLocaleDateString("fr-FR"),
    amount: formatAmount(Number(commande.montant_total)),
    status: commande.statut,
  }));

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <h1>Dashboard</h1>
          <p>Vue d'ensemble de votre activité.</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Commandes"
          value={totalCommandes}
          description="Total des commandes"
        />

        <StatCard
          title="Chiffre d'affaires"
          value={formatAmount(montantTotal)}
          description="Montant total"
        />

        <StatCard
          title="Panier moyen"
          value={formatAmount(panierMoyen)}
          description="Moyenne par commande"
        />

        <StatCard
          title="Clients"
          value={clients.length}
          description="Clients enregistrés"
        />
      </div>

      <OrderTable orders={ordersForTable} />
    </div>
  );
}

export default Dashboard;
import StatusBadge from "./StatusBadge";

function OrderTable({ orders }) {
  return (
    <div className="orders-card">
      <div className="orders-card-header">
        <h2>Dernières commandes</h2>
      </div>

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
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{order.client}</td>
                <td>{order.date}</td>
                <td>{order.amount}</td>
                <td>
                  <StatusBadge status={order.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default OrderTable;
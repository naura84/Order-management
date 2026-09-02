import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>Order</h2>
        <span>Management</span>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/" end>
          Dashboard
        </NavLink>

        <NavLink to="/commandes">
          Commandes
        </NavLink>

        <NavLink to="/clients">
          Clients
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
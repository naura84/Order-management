import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Commandes from "./pages/Commandes";
import NouvelleCommande from "./pages/NouvelleCommande";
import CommandeDetail from "./pages/CommandeDetail";
import ClientDetail from "./pages/ClientDetail";
import Clients from "./pages/Clients";
import NouvelleLigne from "./pages/NouvelleLigne";

import Layout from "./components/Layout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/commandes" element={<Commandes />} />
          <Route path="/commandes/nouvelle" element={<NouvelleCommande />} />
          <Route path="/commandes/:id" element={<CommandeDetail />} />
          <Route path="/clients/:id" element={<ClientDetail />} />
          <Route path="/commandes/:id/lignes/nouvelle" element={<NouvelleLigne />} />
          <Route path="/clients" element={<Clients />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
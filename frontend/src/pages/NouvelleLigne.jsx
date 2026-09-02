import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { createLigneCommande } from "../services/api";

function NouvelleLigne() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    reference_article: "",
    libelle: "",
    quantite: 1,
    prix_unitaire: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setError(null);

      await createLigneCommande(id, {
        reference_article: formData.reference_article,
        libelle: formData.libelle,
        quantite: Number(formData.quantite),
        prix_unitaire: Number(formData.prix_unitaire),
      });

      navigate(`/commandes/${id}`);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="page-heading">
        <div>
          <Link to={`/commandes/${id}`} className="back-link">
            ← Retour à la commande
          </Link>

          <h1>Ajouter une ligne</h1>

          <p>
            Ajouter un article à la commande #{id}
          </p>
        </div>
      </div>

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="reference_article">
                Référence article
              </label>

              <input
                id="reference_article"
                name="reference_article"
                type="text"
                value={formData.reference_article}
                onChange={handleChange}
                placeholder="Ex. ART-001"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="libelle">
                Libellé
              </label>

              <input
                id="libelle"
                name="libelle"
                type="text"
                value={formData.libelle}
                onChange={handleChange}
                placeholder="Nom de l'article"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="quantite">
                Quantité
              </label>

              <input
                id="quantite"
                name="quantite"
                type="number"
                min="1"
                value={formData.quantite}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="prix_unitaire">
                Prix unitaire (€)
              </label>

              <input
                id="prix_unitaire"
                name="prix_unitaire"
                type="number"
                min="0"
                step="0.01"
                value={formData.prix_unitaire}
                onChange={handleChange}
                placeholder="0.00"
                required
              />
            </div>
          </div>

          {error && (
            <div className="error-card form-error">
              {error}
            </div>
          )}

          <div className="form-actions">
            <Link
              to={`/commandes/${id}`}
              className="secondary-button"
            >
              Annuler
            </Link>

            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading ? "Ajout en cours..." : "Ajouter la ligne"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default NouvelleLigne;
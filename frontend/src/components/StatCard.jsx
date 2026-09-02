function StatCard({ title, value, description }) {
  return (
    <div className="stat-card">
      <p className="stat-card-title">{title}</p>

      <p className="stat-card-value">
        {value}
      </p>

      {description && (
        <p className="stat-card-description">
          {description}
        </p>
      )}
    </div>
  );
}

export default StatCard;
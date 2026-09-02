function StatusBadge({ status }) {
  const statusClass = status
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "-");

  return (
    <span className={`status-badge status-${statusClass}`}>
      {status}
    </span>
  );
}

export default StatusBadge;
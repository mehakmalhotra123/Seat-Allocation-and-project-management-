const statusStyles = {
  ACTIVE:
    "bg-emerald-50 text-emerald-700 ring-emerald-600/20",

  INACTIVE:
    "bg-slate-100 text-slate-600 ring-slate-500/20",

  AVAILABLE:
    "bg-emerald-50 text-emerald-700 ring-emerald-600/20",

  OCCUPIED:
    "bg-indigo-50 text-indigo-700 ring-indigo-600/20",

  RESERVED:
    "bg-amber-50 text-amber-700 ring-amber-600/20",

  MAINTENANCE:
    "bg-red-50 text-red-700 ring-red-600/20",
};

function StatusBadge({
  status,
  label,
}) {
  const normalizedStatus =
    status?.toUpperCase();

  const style =
    statusStyles[normalizedStatus] ||
    "bg-slate-100 text-slate-600 ring-slate-500/20";

  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2.5 py-1",
        "text-xs font-semibold ring-1 ring-inset",
        style,
      ].join(" ")}
    >
      {label || status}
    </span>
  );
}

export default StatusBadge;
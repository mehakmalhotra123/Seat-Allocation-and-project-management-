import {
  ArrowUpRight,
} from "lucide-react";

function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
      <div className="flex items-start justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
          <Icon size={21} />
        </div>

        <div className="flex items-center gap-1 text-xs font-medium text-emerald-600">
          Live
          <ArrowUpRight size={14} />
        </div>
      </div>

      <div className="mt-5">
        <p className="text-sm font-medium text-slate-500">
          {title}
        </p>

        <p className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
          {value}
        </p>

        <p className="mt-2 text-xs text-slate-500">
          {subtitle}
        </p>
      </div>
    </div>
  );
}

export default StatCard;
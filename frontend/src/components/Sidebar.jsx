import {
  Bot,
  BriefcaseBusiness,
  Building2,
  LayoutDashboard,
  MapPinned,
  Users,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    name: "Overview",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Employees",
    path: "/employees",
    icon: Users,
  },
  {
    name: "Projects",
    path: "/projects",
    icon: BriefcaseBusiness,
  },
  {
    name: "Seats",
    path: "/seats",
    icon: Building2,
  },
  {
    name: "Allocation",
    path: "/allocation",
    icon: MapPinned,
  },
  {
    name: "AI Assistant",
    path: "/ai-assistant",
    icon: Bot,
  },
];

function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      <div className="flex h-20 items-center border-b border-slate-100 px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white shadow-sm">
            E
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-tight text-slate-900">
              Ethara
            </h1>

            <p className="text-xs text-slate-500">
              Workspace
            </p>
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-6">
        <p className="mb-3 px-3 text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-400">
          Workspace
        </p>

        {navigationItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
                  isActive
                    ? "bg-indigo-50 text-indigo-700"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900",
                ].join(" ")
              }
            >
              <Icon size={19} />

              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="border-t border-slate-100 p-4">
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-sm font-semibold text-slate-800">
            Ethara Operations
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Seat allocation and project mapping
            workspace.
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
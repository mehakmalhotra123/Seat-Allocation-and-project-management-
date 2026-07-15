import {
  Bell,
  Search,
} from "lucide-react";

function Header() {
  return (
    <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur lg:px-8">
      <div>
        <p className="text-sm text-slate-500">
          Workspace management
        </p>

        <h2 className="text-lg font-semibold text-slate-900">
          Ethara Seat Allocation
        </h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
          <Search
            size={17}
            className="text-slate-400"
          />

          <input
            type="text"
            placeholder="Search workspace"
            className="w-52 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />
        </div>

        <button
          type="button"
          className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-50"
        >
          <Bell size={18} />

          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-indigo-600" />
        </button>

        <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-3 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-700">
            HR
          </div>

          <div className="hidden sm:block">
            <p className="text-sm font-semibold text-slate-800">
              HR Admin
            </p>

            <p className="text-xs text-slate-500">
              Operations
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

const menuItems = [
  { name: "Dashboard", path: "/" },
  { name: "Employees", path: "/employees" },
  { name: "Projects", path: "/projects" },
  { name: "Seats", path: "/seats" },
  { name: "Allocation", path: "/allocation" },
  { name: "AI Assistant", path: "/ai-assistant" },
];

export default function MobileNavbar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Top Bar */}
      <div className="lg:hidden flex items-center justify-between px-5 py-4 bg-white shadow sticky top-0 z-50">

        <h1 className="font-bold text-xl text-indigo-600">
          Ethara
        </h1>

        <button
          onClick={() => setOpen(!open)}
          className="p-2 rounded-lg hover:bg-gray-100"
        >
          {open ? <X size={26} /> : <Menu size={26} />}
        </button>

      </div>

      {/* Overlay */}
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-40"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Drawer */}
      <div
        className={`fixed top-0 left-0 h-full w-72 bg-white shadow-2xl z-50 transform transition-transform duration-300

        ${open ? "translate-x-0" : "-translate-x-full"}`}
      >

        <div className="flex justify-between items-center p-5 border-b">

          <h2 className="text-2xl font-bold text-indigo-600">
            Ethara
          </h2>

          <button
            onClick={() => setOpen(false)}
          >
            <X />
          </button>

        </div>

        <div className="p-4 space-y-2">

          {menuItems.map((item) => (

            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block rounded-lg px-4 py-3 transition

                ${
                  isActive
                    ? "bg-indigo-600 text-white"
                    : "hover:bg-indigo-50"
                }`
              }
            >
              {item.name}
            </NavLink>

          ))}

        </div>

      </div>
    </>
  );
}
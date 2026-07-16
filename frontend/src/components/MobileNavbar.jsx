import { Menu, X } from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

const menus = [
  {
    title: "Dashboard",
    link: "/",
  },
  {
    title: "Employees",
    link: "/employees",
  },
  {
    title: "Projects",
    link: "/projects",
  },
  {
    title: "Seats",
    link: "/seats",
  },
  {
    title: "Allocation",
    link: "/allocation",
  },
  {
    title: "AI Assistant",
    link: "/ai-assistant",
  },
];

export default function MobileNavbar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Top Navbar */}

      <div className="lg:hidden bg-white shadow-md sticky top-0 z-50">

        <div className="flex justify-between items-center px-5 py-4">

          <h1 className="font-bold text-2xl text-indigo-600">
            Ethara
          </h1>

          <button
            onClick={() => setOpen(true)}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            <Menu size={26} />
          </button>

        </div>

      </div>

      {/* Overlay */}

      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 bg-black/40 z-40"
        />
      )}

      {/* Drawer */}

      <div
        className={`fixed top-0 left-0 h-screen w-72 bg-white shadow-xl z-50 transition-all duration-300

        ${
          open
            ? "translate-x-0"
            : "-translate-x-full"
        }`}
      >

        <div className="flex justify-between items-center p-5 border-b">

          <h2 className="text-2xl font-bold text-indigo-600">
            Ethara
          </h2>

          <button onClick={() => setOpen(false)}>
            <X />
          </button>

        </div>

        <div className="p-4 space-y-2">

          {menus.map((menu) => (

            <NavLink
              key={menu.link}
              to={menu.link}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block px-4 py-3 rounded-xl transition

                ${
                  isActive
                    ? "bg-indigo-600 text-white"
                    : "hover:bg-indigo-100"
                }`
              }
            >
              {menu.title}
            </NavLink>

          ))}

        </div>

      </div>

    </>
  );
}
import { Outlet } from "react-router-dom";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import MobileNavbar from "../components/MobileNavbar";

function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#f6f8fc]">

      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Mobile Navbar */}
      <MobileNavbar />

      <div className="lg:pl-64">

        {/* Hide desktop header on mobile */}
        <div className="hidden lg:block">
          <Header />
        </div>

        <main className="p-4 lg:p-8">
          <Outlet />
        </main>

      </div>

    </div>
  );
}

export default DashboardLayout;
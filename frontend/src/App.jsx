import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";
import AIAssistant from "./pages/AIAssistant";
import Allocation from "./pages/Allocation";
import Dashboard from "./pages/Dashboard";
import Employees from "./pages/Employees";
import Projects from "./pages/Projects";
import Seats from "./pages/Seats";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/employees"
            element={<Employees />}
          />

          <Route
            path="/projects"
            element={<Projects />}
          />

          <Route
            path="/seats"
            element={<Seats />}
          />

          <Route
            path="/allocation"
            element={<Allocation />}
          />

          <Route
            path="/ai-assistant"
            element={<AIAssistant />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
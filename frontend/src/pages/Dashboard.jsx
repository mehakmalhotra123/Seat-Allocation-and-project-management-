import {
  Armchair,
  Building2,
  Clock3,
  Users,
} from "lucide-react";
import {
  useEffect,
  useState,
} from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import api from "../api/api";
import LoadingState from "../components/LoadingState";
import StatCard from "../components/StatCard";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [
    projectUtilization,
    setProjectUtilization,
  ] = useState([]);
  const [
    floorUtilization,
    setFloorUtilization,
  ] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        summaryResponse,
        projectResponse,
        floorResponse,
      ] = await Promise.all([
        api.get("/dashboard/summary"),
        api.get(
          "/dashboard/project-utilization",
        ),
        api.get(
          "/dashboard/floor-utilization",
        ),
      ]);

      setSummary(summaryResponse.data);

      setProjectUtilization(
        projectResponse.data.items,
      );

      setFloorUtilization(
        floorResponse.data.items,
      );
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to load dashboard.",
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
        <h3 className="font-semibold text-red-800">
          Dashboard unavailable
        </h3>

        <p className="mt-2 text-sm text-red-600">
          {error}
        </p>

        <button
          type="button"
          onClick={fetchDashboardData}
          className="mt-4 rounded-xl bg-red-600 px-4 py-2 text-sm font-semibold text-white"
        >
          Try again
        </button>
      </div>
    );
  }

  const seatStatusData = [
    {
      name: "Occupied",
      value: summary.occupied_seats,
    },
    {
      name: "Available",
      value: summary.available_seats,
    },
    {
      name: "Reserved",
      value: summary.reserved_seats,
    },
    {
      name: "Maintenance",
      value: summary.maintenance_seats,
    },
  ];

  const pieColors = [
    "#4f46e5",
    "#10b981",
    "#f59e0b",
    "#94a3b8",
  ];

  return (
    <div>
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-medium text-indigo-600">
            Workspace overview
          </p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Seat allocation dashboard
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Monitor employee allocation, project
            seating and workspace utilization.
          </p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white px-4 py-3">
          <p className="text-xs font-medium text-slate-500">
            Seat utilization
          </p>

          <p className="mt-1 text-xl font-bold text-slate-900">
            {summary.seat_utilization_percentage}%
          </p>
        </div>
      </div>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Employees"
          value={summary.total_employees.toLocaleString()}
          subtitle={`${summary.active_employees.toLocaleString()} active employees`}
          icon={Users}
        />

        <StatCard
          title="Total Seats"
          value={summary.total_seats.toLocaleString()}
          subtitle="Across all workspace floors"
          icon={Building2}
        />

        <StatCard
          title="Occupied Seats"
          value={summary.occupied_seats.toLocaleString()}
          subtitle={`${summary.seat_utilization_percentage}% utilization`}
          icon={Armchair}
        />

        <StatCard
          title="Pending Allocation"
          value={summary.pending_allocations.toLocaleString()}
          subtitle="Active employees without seats"
          icon={Clock3}
        />
      </section>

      <section className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Project allocation
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Occupied seats by project
            </p>
          </div>

          <div className="mt-6 h-[340px]">
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <BarChart
                data={projectUtilization}
                margin={{
                  top: 10,
                  right: 10,
                  left: -10,
                  bottom: 30,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e2e8f0"
                />

                <XAxis
                  dataKey="project_name"
                  tick={{
                    fontSize: 11,
                    fill: "#64748b",
                  }}
                  angle={-30}
                  textAnchor="end"
                  interval={0}
                />

                <YAxis
                  tick={{
                    fontSize: 11,
                    fill: "#64748b",
                  }}
                />

                <Tooltip />

                <Bar
                  dataKey="occupied_seats"
                  fill="#4f46e5"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Seat status
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Current workspace distribution
            </p>
          </div>

          <div className="mt-4 h-[260px]">
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <PieChart>
                <Pie
                  data={seatStatusData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={65}
                  outerRadius={95}
                  paddingAngle={3}
                >
                  {seatStatusData.map(
                    (entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={
                          pieColors[
                            index % pieColors.length
                          ]
                        }
                      />
                    ),
                  )}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-3">
            {seatStatusData.map(
              (item, index) => (
                <div
                  key={item.name}
                  className="rounded-xl bg-slate-50 p-3"
                >
                  <div className="flex items-center gap-2">
                    <span
                      className="h-2.5 w-2.5 rounded-full"
                      style={{
                        backgroundColor:
                          pieColors[
                            index % pieColors.length
                          ],
                      }}
                    />

                    <span className="text-xs text-slate-500">
                      {item.name}
                    </span>
                  </div>

                  <p className="mt-2 text-lg font-bold text-slate-900">
                    {item.value.toLocaleString()}
                  </p>
                </div>
              ),
            )}
          </div>
        </div>
      </section>

      <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Floor occupancy
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Occupied and available seating by floor
          </p>
        </div>

        <div className="mt-6 h-[320px]">
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart data={floorUtilization}>
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#e2e8f0"
              />

              <XAxis
                dataKey="floor"
                tickFormatter={(value) =>
                  `Floor ${value}`
                }
                tick={{
                  fontSize: 12,
                  fill: "#64748b",
                }}
              />

              <YAxis
                tick={{
                  fontSize: 12,
                  fill: "#64748b",
                }}
              />

              <Tooltip
                labelFormatter={(value) =>
                  `Floor ${value}`
                }
              />

              <Bar
                dataKey="occupied_seats"
                name="Occupied"
                fill="#4f46e5"
                radius={[5, 5, 0, 0]}
              />

              <Bar
                dataKey="available_seats"
                name="Available"
                fill="#10b981"
                radius={[5, 5, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
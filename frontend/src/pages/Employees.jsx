import {
  ChevronLeft,
  ChevronRight,
  Filter,
  Plus,
  Search,
  UserRound,
} from "lucide-react";
import {
  useEffect,
  useState,
} from "react";

import api from "../api/api";
import AddEmployeeModal from "../components/AddEmployeeModal";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";

const PAGE_SIZE = 20;

function Employees() {
  const [employees, setEmployees] =
    useState([]);

  const [projects, setProjects] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] = useState("");

  const [search, setSearch] = useState("");

  const [projectId, setProjectId] =
    useState("");

  const [status, setStatus] =
    useState("");

  const [allocated, setAllocated] =
    useState("");

  const [page, setPage] = useState(1);

  const [total, setTotal] = useState(0);

  const [totalPages, setTotalPages] =
    useState(0);

  const [
    addEmployeeOpen,
    setAddEmployeeOpen,
  ] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchEmployees();
    }, 350);

    return () => clearTimeout(timer);
  }, [
    search,
    projectId,
    status,
    allocated,
    page,
  ]);

  const fetchProjects = async () => {
    try {
      const response = await api.get(
        "/projects",
      );

      setProjects(
        response.data.items ||
          response.data ||
          [],
      );
    } catch {
      setProjects([]);
    }
  };

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      setError("");

      const params = {
        page,
        page_size: PAGE_SIZE,
      };

      if (search.trim()) {
        params.search = search.trim();
      }

      if (projectId) {
        params.project_id = Number(projectId);
      }

      if (status) {
        params.status = status;
      }

      if (allocated !== "") {
        params.allocated =
          allocated === "true";
      }

      const response = await api.get(
        "/employees",
        {
          params,
        },
      );

      setEmployees(response.data.items);

      setTotal(response.data.total);

      setTotalPages(
        response.data.total_pages,
      );
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to load employees.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
    setPage(1);
  };

  const handleProjectChange = (event) => {
    setProjectId(event.target.value);
    setPage(1);
  };

  const handleStatusChange = (event) => {
    setStatus(event.target.value);
    setPage(1);
  };

  const handleAllocatedChange = (
    event,
  ) => {
    setAllocated(event.target.value);
    setPage(1);
  };

  const clearFilters = () => {
    setSearch("");
    setProjectId("");
    setStatus("");
    setAllocated("");
    setPage(1);
  };

  return (
    <div>
      <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-medium text-indigo-600">
            Workforce
          </p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Employees
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Search employees, review project
            mapping and monitor seat allocation.
          </p>
        </div>

        <button
          type="button"
          onClick={() =>
            setAddEmployeeOpen(true)
          }
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700"
        >
          <Plus size={18} />

          Add employee
        </button>
      </div>

      <section className="mt-7 rounded-2xl border border-slate-200 bg-white shadow-sm shadow-slate-200/40">
        <div className="border-b border-slate-200 p-5">
          <div className="grid gap-3 xl:grid-cols-[1.5fr_repeat(3,0.7fr)_auto]">
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3">
              <Search
                size={18}
                className="text-slate-400"
              />

              <input
                type="text"
                value={search}
                onChange={handleSearchChange}
                placeholder="Search name, employee ID or email"
                className="w-full bg-transparent py-2.5 text-sm text-slate-700 outline-none placeholder:text-slate-400"
              />
            </div>

            <select
              value={projectId}
              onChange={handleProjectChange}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All projects
              </option>

              {projects.map((project) => (
                <option
                  key={project.id}
                  value={project.id}
                >
                  {project.name}
                </option>
              ))}
            </select>

            <select
              value={status}
              onChange={handleStatusChange}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All statuses
              </option>

              <option value="ACTIVE">
                Active
              </option>

              <option value="INACTIVE">
                Inactive
              </option>
            </select>

            <select
              value={allocated}
              onChange={handleAllocatedChange}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All allocations
              </option>

              <option value="true">
                Seat allocated
              </option>

              <option value="false">
                Pending allocation
              </option>
            </select>

            <button
              type="button"
              onClick={clearFilters}
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
            >
              <Filter size={17} />

              Clear
            </button>
          </div>
        </div>

        {error ? (
          <div className="p-6">
            <div className="rounded-xl border border-red-200 bg-red-50 p-4">
              <p className="font-semibold text-red-800">
                Employees unavailable
              </p>

              <p className="mt-1 text-sm text-red-600">
                {error}
              </p>

              <button
                type="button"
                onClick={fetchEmployees}
                className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white"
              >
                Try again
              </button>
            </div>
          </div>
        ) : loading ? (
          <LoadingState message="Loading employees..." />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[1050px]">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/70">
                    <TableHeading>
                      Employee
                    </TableHeading>

                    <TableHeading>
                      Employee ID
                    </TableHeading>

                    <TableHeading>
                      Department
                    </TableHeading>

                    <TableHeading>
                      Role
                    </TableHeading>

                    <TableHeading>
                      Project
                    </TableHeading>

                    <TableHeading>
                      Status
                    </TableHeading>

                    <TableHeading>
                      Seat
                    </TableHeading>
                  </tr>
                </thead>

                <tbody>
                  {employees.map((employee) => (
                    <tr
                      key={employee.id}
                      className="border-b border-slate-100 transition last:border-b-0 hover:bg-slate-50/70"
                    >
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                            <UserRound size={18} />
                          </div>

                          <div>
                            <p className="font-semibold text-slate-800">
                              {employee.name}
                            </p>

                            <p className="mt-0.5 text-xs text-slate-500">
                              {employee.email}
                            </p>
                          </div>
                        </div>
                      </TableCell>

                      <TableCell>
                        <span className="font-medium text-slate-700">
                          {employee.employee_code}
                        </span>
                      </TableCell>

                      <TableCell>
                        {employee.department}
                      </TableCell>

                      <TableCell>
                        {employee.role}
                      </TableCell>

                      <TableCell>
                        {employee.project_name ||
                          "Unassigned"}
                      </TableCell>

                      <TableCell>
                        <StatusBadge
                          status={employee.status}
                        />
                      </TableCell>

                      <TableCell>
                        {employee.seat_number ? (
                          <span className="font-semibold text-indigo-600">
                            {employee.seat_number}
                          </span>
                        ) : (
                          <span className="text-sm font-medium text-amber-600">
                            Pending
                          </span>
                        )}
                      </TableCell>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {employees.length === 0 && (
              <div className="py-16 text-center">
                <UserRound
                  size={38}
                  className="mx-auto text-slate-300"
                />

                <h3 className="mt-4 font-semibold text-slate-800">
                  No employees found
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Try changing the search or filters.
                </p>
              </div>
            )}

            <div className="flex flex-col justify-between gap-4 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center">
              <p className="text-sm text-slate-500">
                Showing{" "}
                <span className="font-semibold text-slate-700">
                  {employees.length}
                </span>{" "}
                of{" "}
                <span className="font-semibold text-slate-700">
                  {total.toLocaleString()}
                </span>{" "}
                employees
              </p>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  disabled={page <= 1}
                  onClick={() =>
                    setPage((currentPage) =>
                      currentPage - 1
                    )
                  }
                  className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  <ChevronLeft size={17} />
                </button>

                <div className="rounded-lg bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-700">
                  Page {page}
                  {totalPages > 0 &&
                    ` of ${totalPages}`}
                </div>

                <button
                  type="button"
                  disabled={
                    totalPages === 0 ||
                    page >= totalPages
                  }
                  onClick={() =>
                    setPage((currentPage) =>
                      currentPage + 1
                    )
                  }
                  className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  <ChevronRight size={17} />
                </button>
              </div>
            </div>
          </>
        )}
      </section>

      <AddEmployeeModal
        open={addEmployeeOpen}
        onClose={() =>
          setAddEmployeeOpen(false)
        }
        onEmployeeCreated={() => {
          setPage(1);
          fetchEmployees();
        }}
      />
    </div>
  );
}


function TableHeading({
  children,
}) {
  return (
    <th className="px-5 py-3.5 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
      {children}
    </th>
  );
}


function TableCell({
  children,
}) {
  return (
    <td className="px-5 py-4 text-sm text-slate-600">
      {children}
    </td>
  );
}


export default Employees;
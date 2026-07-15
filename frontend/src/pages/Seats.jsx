import {
  Armchair,
  ChevronLeft,
  ChevronRight,
  Filter,
  Search,
} from "lucide-react";
import {
  useEffect,
  useState,
} from "react";

import api from "../api/api";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";

const PAGE_SIZE = 30;

const FLOORS = [1, 2, 3, 4, 5];

const ZONES = [
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
];

function Seats() {
  const [seats, setSeats] = useState([]);
  const [loading, setLoading] =
    useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [floor, setFloor] = useState("");
  const [zone, setZone] = useState("");
  const [status, setStatus] = useState("");

  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] =
    useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchSeats();
    }, 300);

    return () => clearTimeout(timer);
  }, [
    search,
    floor,
    zone,
    status,
    page,
  ]);

  const fetchSeats = async () => {
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

      if (floor) {
        params.floor = Number(floor);
      }

      if (zone) {
        params.zone = zone;
      }

      if (status) {
        params.status = status;
      }

      const response = await api.get(
        "/seats",
        {
          params,
        },
      );

      setSeats(response.data.items);
      setTotal(response.data.total);
      setTotalPages(
        response.data.total_pages,
      );
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to load seats.",
      );
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSearch("");
    setFloor("");
    setZone("");
    setStatus("");
    setPage(1);
  };

  return (
    <div>
      <div>
        <p className="text-sm font-medium text-indigo-600">
          Workspace inventory
        </p>

        <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
          Seats
        </h1>

        <p className="mt-2 text-sm text-slate-500">
          Search seat inventory and identify
          workspace availability by floor and zone.
        </p>
      </div>

      <section className="mt-7 rounded-2xl border border-slate-200 bg-white shadow-sm shadow-slate-200/40">
        <div className="border-b border-slate-200 p-5">
          <div className="grid gap-3 xl:grid-cols-[1.4fr_repeat(3,0.6fr)_auto]">
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3">
              <Search
                size={18}
                className="text-slate-400"
              />

              <input
                type="text"
                value={search}
                onChange={(event) => {
                  setSearch(
                    event.target.value,
                  );
                  setPage(1);
                }}
                placeholder="Search seat number or bay"
                className="w-full bg-transparent py-2.5 text-sm text-slate-700 outline-none placeholder:text-slate-400"
              />
            </div>

            <select
              value={floor}
              onChange={(event) => {
                setFloor(event.target.value);
                setPage(1);
              }}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All floors
              </option>

              {FLOORS.map((floorNumber) => (
                <option
                  key={floorNumber}
                  value={floorNumber}
                >
                  Floor {floorNumber}
                </option>
              ))}
            </select>

            <select
              value={zone}
              onChange={(event) => {
                setZone(event.target.value);
                setPage(1);
              }}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All zones
              </option>

              {ZONES.map((zoneName) => (
                <option
                  key={zoneName}
                  value={zoneName}
                >
                  Zone {zoneName}
                </option>
              ))}
            </select>

            <select
              value={status}
              onChange={(event) => {
                setStatus(event.target.value);
                setPage(1);
              }}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none focus:border-indigo-500"
            >
              <option value="">
                All statuses
              </option>

              <option value="AVAILABLE">
                Available
              </option>

              <option value="OCCUPIED">
                Occupied
              </option>

              <option value="RESERVED">
                Reserved
              </option>

              <option value="MAINTENANCE">
                Maintenance
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
                Seats unavailable
              </p>

              <p className="mt-1 text-sm text-red-600">
                {error}
              </p>

              <button
                type="button"
                onClick={fetchSeats}
                className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white"
              >
                Try again
              </button>
            </div>
          </div>
        ) : loading ? (
          <LoadingState message="Loading seat inventory..." />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[950px]">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/70">
                    <TableHeading>
                      Seat
                    </TableHeading>

                    <TableHeading>
                      Floor
                    </TableHeading>

                    <TableHeading>
                      Zone
                    </TableHeading>

                    <TableHeading>
                      Bay
                    </TableHeading>

                    <TableHeading>
                      Status
                    </TableHeading>

                    <TableHeading>
                      Employee
                    </TableHeading>

                    <TableHeading>
                      Project
                    </TableHeading>
                  </tr>
                </thead>

                <tbody>
                  {seats.map((seat) => (
                    <tr
                      key={seat.id}
                      className="border-b border-slate-100 transition last:border-b-0 hover:bg-slate-50/70"
                    >
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                            <Armchair size={18} />
                          </div>

                          <span className="font-bold text-slate-800">
                            {seat.seat_number}
                          </span>
                        </div>
                      </TableCell>

                      <TableCell>
                        Floor {seat.floor}
                      </TableCell>

                      <TableCell>
                        Zone {seat.zone}
                      </TableCell>

                      <TableCell>
                        {seat.bay}
                      </TableCell>

                      <TableCell>
                        <StatusBadge
                          status={seat.status}
                        />
                      </TableCell>

                      <TableCell>
                        {seat.employee_name ||
                          "—"}
                      </TableCell>

                      <TableCell>
                        {seat.project_name ||
                          "—"}
                      </TableCell>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {seats.length === 0 && (
              <div className="py-16 text-center">
                <Armchair
                  size={40}
                  className="mx-auto text-slate-300"
                />

                <h3 className="mt-4 font-semibold text-slate-800">
                  No seats found
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Try changing the seat filters.
                </p>
              </div>
            )}

            <div className="flex flex-col justify-between gap-4 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center">
              <p className="text-sm text-slate-500">
                Showing{" "}
                <span className="font-semibold text-slate-700">
                  {seats.length}
                </span>{" "}
                of{" "}
                <span className="font-semibold text-slate-700">
                  {total.toLocaleString()}
                </span>{" "}
                seats
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
    </div>
  );
}

function TableHeading({ children }) {
  return (
    <th className="px-5 py-3.5 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">
      {children}
    </th>
  );
}

function TableCell({ children }) {
  return (
    <td className="px-5 py-4 text-sm text-slate-600">
      {children}
    </td>
  );
}

export default Seats;
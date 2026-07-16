import {
  AlertCircle,
  ArrowRight,
  Armchair,
  BriefcaseBusiness,
  Building2,
  Check,
  CheckCircle2,
  Lightbulb,
  LoaderCircle,
  MapPin,
  Search,
  Sparkles,
  UserRound,
  Users,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import api from "../api/api";
import LoadingState from "../components/LoadingState";

function getErrorMessage(
  error,
  fallbackMessage,
) {
  if (
    typeof error?.message === "string" &&
    error.message.trim()
  ) {
    return error.message;
  }

  return fallbackMessage;
}

function normalizeCollection(data) {
  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data?.items)) {
    return data.items;
  }

  return [];
}

function Allocation() {
  const [employees, setEmployees] =
    useState([]);

  const [selectedEmployee, setSelectedEmployee] =
    useState(null);

  const [selectedSeat, setSelectedSeat] =
    useState(null);

  const [recommendations, setRecommendations] =
    useState([]);

  const [
    recommendationsLoading,
    setRecommendationsLoading,
  ] = useState(false);

  const [search, setSearch] = useState("");

  const [loading, setLoading] =
    useState(true);

  const [allocating, setAllocating] =
    useState(false);

  const [error, setError] = useState("");

  const [success, setSuccess] =
    useState("");

  useEffect(() => {
    fetchAllocationData();
  }, []);

  const fetchAllocationData = async () => {
    try {
      setLoading(true);
      setError("");

      const employeesResponse = await api.get(
        "/employees",
        {
          params: {
            allocated: false,
            page: 1,
            page_size: 100,
          },
        },
      );

      const employeeItems = normalizeCollection(
        employeesResponse.data,
      );

      setEmployees(employeeItems);
    } catch (requestError) {
      console.error(
        "Allocation data error:",
        requestError?.data ||
          requestError,
      );

      setError(
        getErrorMessage(
          requestError,
          "Unable to load pending employees.",
        ),
      );
    } finally {
      setLoading(false);
    }
  };

  const filteredEmployees = useMemo(() => {
    const query = search
      .trim()
      .toLowerCase();

    if (!query) {
      return employees;
    }

    return employees.filter((employee) => {
      const name = String(
        employee?.name || "",
      ).toLowerCase();

      const employeeCode = String(
        employee?.employee_code || "",
      ).toLowerCase();

      const email = String(
        employee?.email || "",
      ).toLowerCase();

      return (
        name.includes(query) ||
        employeeCode.includes(query) ||
        email.includes(query)
      );
    });
  }, [employees, search]);

  const handleSelectEmployee = async (
    employee,
  ) => {
    try {
      setSelectedEmployee(employee);
      setSelectedSeat(null);
      setRecommendations([]);
      setRecommendationsLoading(true);
      setSuccess("");
      setError("");

      const response = await api.get(
        `/seats/recommendations/${employee.id}`,
        {
          params: {
            limit: 6,
          },
        },
      );

      const seatItems = normalizeCollection(
        response.data,
      );

      const normalizedRecommendations =
        seatItems.map((seat) => ({
          ...seat,

          recommendationScore: Number(
            seat?.score ??
              seat?.recommendationScore ??
              0,
          ),

          reasons: Array.isArray(seat?.reasons)
            ? seat.reasons
            : [
                "Available alternate workspace",
              ],
        }));

      setRecommendations(
        normalizedRecommendations,
      );
    } catch (requestError) {
      console.error(
        "Recommendation error:",
        requestError?.data ||
          requestError,
      );

      setError(
        getErrorMessage(
          requestError,
          "Unable to load seat recommendations.",
        ),
      );
    } finally {
      setRecommendationsLoading(false);
    }
  };

  const handleAllocate = async () => {
    if (
      !selectedEmployee ||
      !selectedSeat
    ) {
      setError(
        "Please select an employee and a seat.",
      );

      return;
    }

    try {
      setAllocating(true);
      setError("");
      setSuccess("");

      const requestBody = {
        employee_id: selectedEmployee.id,
        seat_id: selectedSeat.id,
      };

      console.log(
        "Allocation request:",
        requestBody,
      );

      await api.post(
        "/seats/allocate",
        requestBody,
      );

      const employeeName =
        selectedEmployee.name ||
        selectedEmployee.employee_code ||
        "Employee";

      const seatNumber =
        selectedSeat.seat_number ||
        `Seat ${selectedSeat.id}`;

      setSuccess(
        `${seatNumber} has been allocated to ${employeeName}.`,
      );

      setEmployees((currentEmployees) =>
        currentEmployees.filter(
          (employee) =>
            employee.id !==
            selectedEmployee.id,
        ),
      );

      setSelectedEmployee(null);
      setSelectedSeat(null);
      setRecommendations([]);
    } catch (requestError) {
      console.error(
        "Seat allocation error:",
        requestError?.data ||
          requestError,
      );

      setError(
        getErrorMessage(
          requestError,
          "Unable to allocate seat.",
        ),
      );
    } finally {
      setAllocating(false);
    }
  };

  if (loading) {
    return (
      <LoadingState message="Preparing smart seat allocation..." />
    );
  }

  return (
    <div>
      <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-end">
        <div>
          <div className="flex items-center gap-2 text-sm font-medium text-indigo-600">
            <Sparkles size={17} />

            Smart allocation
          </div>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
            Seat Allocation
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
            Allocate pending employees to
            available workspace seats using
            project and team proximity
            recommendations.
          </p>
        </div>

        <div className="rounded-2xl border border-indigo-100 bg-indigo-50 px-5 py-3">
          <p className="text-xs font-semibold uppercase tracking-wider text-indigo-500">
            Pending allocation
          </p>

          <p className="mt-1 text-2xl font-bold text-indigo-700">
            {employees.length.toLocaleString()}
          </p>
        </div>
      </div>

      {success && (
        <div className="mt-6 flex items-start gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
          <CheckCircle2
            size={21}
            className="mt-0.5 shrink-0 text-emerald-600"
          />

          <div>
            <p className="font-semibold text-emerald-800">
              Seat allocated successfully
            </p>

            <p className="mt-1 text-sm text-emerald-700">
              {String(success)}
            </p>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 p-4">
          <AlertCircle
            size={21}
            className="mt-0.5 shrink-0 text-red-600"
          />

          <div>
            <p className="font-semibold text-red-800">
              Allocation error
            </p>

            <p className="mt-1 text-sm text-red-600">
              {String(error)}
            </p>
          </div>
        </div>
      )}

      <section className="mt-7 grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm shadow-slate-200/40">
          <div className="border-b border-slate-200 p-5">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold text-slate-900">
                  Select employee
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Active employees pending seat
                  allocation
                </p>
              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
                <Users size={19} />
              </div>
            </div>

            <div className="mt-5 flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3">
              <Search
                size={17}
                className="text-slate-400"
              />

              <input
                type="text"
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
                placeholder="Search pending employee"
                className="w-full bg-transparent py-2.5 text-sm text-slate-700 outline-none placeholder:text-slate-400"
              />
            </div>
          </div>

          <div className="max-h-[610px] overflow-y-auto p-3">
            {filteredEmployees.map(
              (employee) => {
                const selected =
                  selectedEmployee?.id ===
                  employee.id;

                return (
                  <button
                    key={employee.id}
                    type="button"
                    onClick={() =>
                      handleSelectEmployee(
                        employee,
                      )
                    }
                    className={[
                      "mb-2 flex w-full items-center justify-between rounded-xl border p-4 text-left transition",
                      selected
                        ? "border-indigo-300 bg-indigo-50 ring-2 ring-indigo-100"
                        : "border-transparent hover:border-slate-200 hover:bg-slate-50",
                    ].join(" ")}
                  >
                    <div className="flex min-w-0 items-center gap-3">
                      <div
                        className={[
                          "flex h-11 w-11 shrink-0 items-center justify-center rounded-xl",
                          selected
                            ? "bg-indigo-600 text-white"
                            : "bg-slate-100 text-slate-500",
                        ].join(" ")}
                      >
                        <UserRound size={19} />
                      </div>

                      <div className="min-w-0">
                        <p className="truncate font-semibold text-slate-800">
                          {employee.name ||
                            "Unnamed employee"}
                        </p>

                        <p className="mt-1 truncate text-xs text-slate-500">
                          {employee.employee_code ||
                            "No employee code"}

                          {" • "}

                          {employee.project_name ||
                            "No project"}
                        </p>
                      </div>
                    </div>

                    <ArrowRight
                      size={17}
                      className={
                        selected
                          ? "text-indigo-600"
                          : "text-slate-300"
                      }
                    />
                  </button>
                );
              },
            )}

            {filteredEmployees.length ===
              0 && (
              <div className="py-16 text-center">
                <UserRound
                  size={36}
                  className="mx-auto text-slate-300"
                />

                <p className="mt-4 font-semibold text-slate-700">
                  No pending employees found
                </p>

                <p className="mt-1 text-sm text-slate-500">
                  Try another employee search.
                </p>
              </div>
            )}
          </div>
        </div>

        <div>
          {!selectedEmployee ? (
            <EmptyRecommendationState />
          ) : (
            <div>
              <SelectedEmployeeCard
                employee={selectedEmployee}
              />

              <div className="mt-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
                <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                  <div>
                    <div className="flex items-center gap-2">
                      <Sparkles
                        size={18}
                        className="text-indigo-600"
                      />

                      <h2 className="font-bold text-slate-900">
                        Recommended seats
                      </h2>
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      Ranked using project team
                      proximity
                    </p>
                  </div>

                  <span className="rounded-full bg-indigo-50 px-3 py-1.5 text-xs font-semibold text-indigo-700">
                    Smart ranking
                  </span>
                </div>

                {recommendationsLoading ? (
                  <div className="flex min-h-[300px] items-center justify-center">
                    <div className="text-center">
                      <LoaderCircle
                        size={32}
                        className="mx-auto animate-spin text-indigo-600"
                      />

                      <p className="mt-4 text-sm font-medium text-slate-600">
                        Analysing project team
                        proximity...
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        Ranking available workspace
                        seats
                      </p>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="mt-5 space-y-3">
                      {recommendations.map(
                        (seat, index) => (
                          <SeatRecommendation
                            key={seat.id}
                            seat={seat}
                            rank={index + 1}
                            selected={
                              selectedSeat?.id ===
                              seat.id
                            }
                            onSelect={() =>
                              setSelectedSeat(seat)
                            }
                          />
                        ),
                      )}
                    </div>

                    {recommendations.length ===
                      0 && (
                      <div className="py-12 text-center">
                        <Armchair
                          size={38}
                          className="mx-auto text-slate-300"
                        />

                        <p className="mt-4 font-semibold text-slate-700">
                          No available seat
                          recommendations
                        </p>

                        <p className="mt-1 text-sm text-slate-500">
                          No suitable workspace is
                          currently available.
                        </p>
                      </div>
                    )}
                  </>
                )}

                {selectedSeat &&
                  !recommendationsLoading && (
                  <div className="mt-6 rounded-2xl border border-indigo-200 bg-indigo-50 p-5">
                    <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-wider text-indigo-500">
                          Allocation ready
                        </p>

                        <p className="mt-1 font-bold text-slate-900">
                          {selectedEmployee.name ||
                            selectedEmployee.employee_code}

                          {" → "}

                          {selectedSeat.seat_number}
                        </p>

                        <p className="mt-1 text-sm text-slate-600">
                          Floor{" "}
                          {selectedSeat.floor}, Zone{" "}
                          {selectedSeat.zone}, Bay{" "}
                          {selectedSeat.bay}
                        </p>
                      </div>

                      <button
                        type="button"
                        disabled={allocating}
                        onClick={handleAllocate}
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
                      >
                        {allocating ? (
                          <>
                            <LoaderCircle
                              size={18}
                              className="animate-spin"
                            />

                            Allocating...
                          </>
                        ) : (
                          <>
                            <Check size={18} />

                            Allocate seat
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function SelectedEmployeeCard({
  employee,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40">
      <div className="flex items-start gap-4">
        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-indigo-600 text-white">
          <UserRound size={24} />
        </div>

        <div className="min-w-0 flex-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-indigo-500">
            Selected employee
          </p>

          <h2 className="mt-1 text-xl font-bold text-slate-900">
            {employee.name ||
              "Unnamed employee"}
          </h2>

          <p className="mt-1 break-all text-sm text-slate-500">
            {employee.employee_code ||
              "No employee code"}

            {" • "}

            {employee.email || "No email"}
          </p>

          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <EmployeeDetail
              icon={BriefcaseBusiness}
              label="Project"
              value={
                employee.project_name ||
                "Not assigned"
              }
            />

            <EmployeeDetail
              icon={Building2}
              label="Department"
              value={
                employee.department ||
                "Not assigned"
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function EmployeeDetail({
  icon: Icon,
  label,
  value,
}) {
  return (
    <div className="flex items-center gap-3 rounded-xl bg-slate-50 p-3">
      <Icon
        size={17}
        className="text-slate-400"
      />

      <div>
        <p className="text-xs text-slate-400">
          {label}
        </p>

        <p className="mt-0.5 text-sm font-semibold text-slate-700">
          {String(value || "—")}
        </p>
      </div>
    </div>
  );
}

function SeatRecommendation({
  seat,
  rank,
  selected,
  onSelect,
}) {
  const score = Number(
    seat.recommendationScore || 0,
  );

  const reasons = Array.isArray(
    seat.reasons,
  )
    ? seat.reasons
    : [];

  return (
    <button
      type="button"
      onClick={onSelect}
      className={[
        "w-full rounded-2xl border p-4 text-left transition",
        selected
          ? "border-indigo-400 bg-indigo-50 ring-2 ring-indigo-100"
          : "border-slate-200 hover:border-indigo-200 hover:bg-slate-50",
      ].join(" ")}
    >
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div className="flex items-start gap-4">
          <div
            className={[
              "flex h-11 w-11 shrink-0 items-center justify-center rounded-xl font-bold",
              rank === 1
                ? "bg-indigo-600 text-white"
                : "bg-slate-100 text-slate-600",
            ].join(" ")}
          >
            #{rank}
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-bold text-slate-900">
                {seat.seat_number ||
                  `Seat ${seat.id}`}
              </h3>

              {rank === 1 && (
                <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-bold text-emerald-700">
                  BEST MATCH
                </span>
              )}
            </div>

            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-500">
              <span className="flex items-center gap-1.5">
                <Building2 size={14} />

                Floor {seat.floor}
              </span>

              <span className="flex items-center gap-1.5">
                <MapPin size={14} />

                Zone {seat.zone}
              </span>

              <span className="flex items-center gap-1.5">
                <Armchair size={14} />

                Bay {seat.bay}
              </span>
            </div>

            <div className="mt-3 flex items-start gap-2">
              <Lightbulb
                size={14}
                className="mt-0.5 shrink-0 text-amber-500"
              />

              <p className="text-xs text-slate-500">
                {reasons.length > 0
                  ? reasons.join(" • ")
                  : "Available workspace seat"}
              </p>
            </div>
          </div>
        </div>

        <div className="sm:text-right">
          <p className="text-2xl font-bold text-indigo-600">
            {score}
          </p>

          <p className="text-xs font-medium text-slate-400">
            match score
          </p>
        </div>
      </div>
    </button>
  );
}

function EmptyRecommendationState() {
  return (
    <div className="flex min-h-[500px] items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white p-8">
      <div className="max-w-sm text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
          <Sparkles size={27} />
        </div>

        <h2 className="mt-5 text-xl font-bold text-slate-900">
          Smart seat recommendations
        </h2>

        <p className="mt-2 text-sm leading-6 text-slate-500">
          Select an employee pending allocation.
          The system will rank available seats
          based on project and workspace
          proximity.
        </p>
      </div>
    </div>
  );
}

export default Allocation;
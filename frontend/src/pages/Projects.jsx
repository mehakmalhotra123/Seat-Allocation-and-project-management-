import {
  BriefcaseBusiness,
  Search,
  Users,
  Armchair,
  TrendingUp,
} from "lucide-react";
import {
  useEffect,
  useMemo,
  useState,
} from "react";

import api from "../api/api";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";

function Projects() {
  const [projects, setProjects] = useState([]);
  const [utilization, setUtilization] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError("");

      const [
        projectsResponse,
        utilizationResponse,
      ] = await Promise.all([
        api.get("/projects"),
        api.get("/dashboard/project-utilization"),
      ]);

      setProjects(
        projectsResponse.data.items ||
          projectsResponse.data ||
          [],
      );

      setUtilization(
        utilizationResponse.data.items ||
          utilizationResponse.data ||
          [],
      );
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to load projects.",
      );
    } finally {
      setLoading(false);
    }
  };

  const projectCards = useMemo(() => {
    return projects.map((project) => {
      const utilizationData = utilization.find(
        (item) =>
          item.project_id === project.id ||
          item.project_name === project.name,
      );

      return {
        ...project,
        employee_count:
          utilizationData?.employee_count ??
          utilizationData?.total_employees ??
          0,
        occupied_seats:
          utilizationData?.occupied_seats ?? 0,
        utilization_percentage:
          utilizationData?.utilization_percentage ??
          utilizationData?.seat_utilization_percentage ??
          0,
      };
    });
  }, [projects, utilization]);

  const filteredProjects = projectCards.filter(
    (project) => {
      const query = search
        .trim()
        .toLowerCase();

      if (!query) {
        return true;
      }

      return (
        project.name
          ?.toLowerCase()
          .includes(query) ||
        project.manager_name
          ?.toLowerCase()
          .includes(query) ||
        project.description
          ?.toLowerCase()
          .includes(query)
      );
    },
  );

  if (loading) {
    return (
      <LoadingState message="Loading projects..." />
    );
  }

  return (
    <div>
      <div>
        <p className="text-sm font-medium text-indigo-600">
          Project mapping
        </p>

        <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
          Projects
        </h1>

        <p className="mt-2 text-sm text-slate-500">
          Review project teams and workspace
          allocation across Ethara.
        </p>
      </div>

      <section className="mt-7">
        <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 shadow-sm md:max-w-md">
          <Search
            size={18}
            className="text-slate-400"
          />

          <input
            type="text"
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            placeholder="Search projects or managers"
            className="w-full bg-transparent py-3 text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />
        </div>
      </section>

      {error && (
        <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-5">
          <p className="font-semibold text-red-800">
            Projects unavailable
          </p>

          <p className="mt-1 text-sm text-red-600">
            {error}
          </p>

          <button
            type="button"
            onClick={fetchProjects}
            className="mt-4 rounded-xl bg-red-600 px-4 py-2 text-sm font-semibold text-white"
          >
            Try again
          </button>
        </div>
      )}

      {!error && (
        <section className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
            />
          ))}
        </section>
      )}

      {!error &&
        filteredProjects.length === 0 && (
          <div className="mt-6 rounded-2xl border border-slate-200 bg-white py-16 text-center">
            <BriefcaseBusiness
              size={40}
              className="mx-auto text-slate-300"
            />

            <h3 className="mt-4 font-semibold text-slate-800">
              No projects found
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Try another project or manager name.
            </p>
          </div>
        )}
    </div>
  );
}

function ProjectCard({ project }) {
  const percentage = Number(
    project.utilization_percentage || 0,
  );

  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/40 transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-start justify-between gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
          <BriefcaseBusiness size={22} />
        </div>

        <StatusBadge
          status={project.status}
        />
      </div>

      <div className="mt-5">
        <h2 className="text-xl font-bold text-slate-900">
          {project.name}
        </h2>

        <p className="mt-2 min-h-10 text-sm leading-5 text-slate-500">
          {project.description ||
            "Ethara active project workspace."}
        </p>
      </div>

      <div className="mt-5 rounded-xl bg-slate-50 p-4">
        <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
          Project manager
        </p>

        <p className="mt-1 text-sm font-semibold text-slate-700">
          {project.manager_name ||
            "Not assigned"}
        </p>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <ProjectMetric
          icon={Users}
          label="Employees"
          value={project.employee_count}
        />

        <ProjectMetric
          icon={Armchair}
          label="Occupied seats"
          value={project.occupied_seats}
        />
      </div>

      <div className="mt-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm font-medium text-slate-600">
            <TrendingUp size={16} />

            Seat utilization
          </div>

          <span className="text-sm font-bold text-slate-900">
            {percentage.toFixed(1)}%
          </span>
        </div>

        <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-indigo-600 transition-all"
            style={{
              width: `${Math.min(
                percentage,
                100,
              )}%`,
            }}
          />
        </div>
      </div>
    </article>
  );
}

function ProjectMetric({
  icon: Icon,
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-slate-100 p-3">
      <div className="flex items-center gap-2 text-slate-400">
        <Icon size={15} />

        <span className="text-xs">
          {label}
        </span>
      </div>

      <p className="mt-2 text-lg font-bold text-slate-800">
        {Number(value || 0).toLocaleString()}
      </p>
    </div>
  );
}

export default Projects;
import {
  useEffect,
  useState,
} from "react";

import api from "../api/api";

const initialFormData = {
  employee_code: "",
  name: "",
  email: "",
  department: "",
  role: "",
  joining_date: "",
  status: "ACTIVE",
  project_id: "",
};

function AddEmployeeModal({
  open,
  onClose,
  onEmployeeCreated,
}) {
  const [formData, setFormData] =
    useState(initialFormData);

  const [projects, setProjects] =
    useState([]);

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    if (open) {
      fetchProjects();
    }
  }, [open]);

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

  const handleChange = (event) => {
    const {
      name,
      value,
    } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setSubmitting(true);
      setError("");

      const payload = {
        ...formData,
        project_id: formData.project_id
          ? Number(formData.project_id)
          : null,
      };

      await api.post(
        "/employees",
        payload,
      );

      setFormData(initialFormData);

      onEmployeeCreated();

      onClose();
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to create employee.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
          <div>
            <h2 className="text-xl font-bold text-slate-900">
              Add employee
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Add a new joiner to the Ethara
              workspace.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-3 py-2 text-sm font-semibold text-slate-500 hover:bg-slate-100"
          >
            Close
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="p-6"
        >
          {error && (
            <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="grid gap-5 md:grid-cols-2">
            <FormField
              label="Employee ID"
              name="employee_code"
              value={formData.employee_code}
              onChange={handleChange}
              placeholder="EMP5001"
              required
            />

            <FormField
              label="Employee name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Amit Sharma"
              required
            />

            <FormField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="amit@ethara.ai"
              required
            />

            <FormField
              label="Department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              placeholder="Engineering"
              required
            />

            <FormField
              label="Role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              placeholder="Software Engineer"
              required
            />

            <FormField
              label="Joining date"
              name="joining_date"
              type="date"
              value={formData.joining_date}
              onChange={handleChange}
              required
            />

            <div>
              <label className="text-sm font-semibold text-slate-700">
                Project
              </label>

              <select
                name="project_id"
                value={formData.project_id}
                onChange={handleChange}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              >
                <option value="">
                  No project
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
            </div>

            <div>
              <label className="text-sm font-semibold text-slate-700">
                Employment status
              </label>

              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              >
                <option value="ACTIVE">
                  Active
                </option>

                <option value="INACTIVE">
                  Inactive
                </option>
              </select>
            </div>
          </div>

          <div className="mt-7 flex justify-end gap-3 border-t border-slate-100 pt-5">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={submitting}
              className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting
                ? "Adding employee..."
                : "Add employee"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


function FormField({
  label,
  name,
  value,
  onChange,
  type = "text",
  placeholder,
  required = false,
}) {
  return (
    <div>
      <label className="text-sm font-semibold text-slate-700">
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-700 outline-none placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
      />
    </div>
  );
}


export default AddEmployeeModal;
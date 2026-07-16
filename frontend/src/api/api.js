import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000",

  headers: {
    "Content-Type": "application/json",
  },

  timeout: 15000,
});

function extractErrorMessage(error) {
  const detail = error?.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        const location = Array.isArray(item?.loc)
          ? item.loc.join(" → ")
          : "";

        const message =
          item?.msg || "Validation error";

        if (location) {
          return `${location}: ${message}`;
        }

        return message;
      })
      .join(", ");
  }

  if (detail && typeof detail === "object") {
    if (typeof detail.msg === "string") {
      return detail.msg;
    }

    try {
      return JSON.stringify(detail);
    } catch {
      return "The server returned an invalid response.";
    }
  }

  const serverMessage =
    error?.response?.data?.message;

  if (typeof serverMessage === "string") {
    return serverMessage;
  }

  if (typeof error?.message === "string") {
    return error.message;
  }

  return "Unable to complete the request.";
}

api.interceptors.response.use(
  (response) => response,

  (error) => {
    const apiError = new Error(
      extractErrorMessage(error),
    );

    apiError.status =
      error?.response?.status || null;

    apiError.data =
      error?.response?.data || null;

    apiError.originalError = error;

    return Promise.reject(apiError);
  },
);

export default api;
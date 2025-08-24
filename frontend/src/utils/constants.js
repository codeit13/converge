const isLocalhost =
  window?.location?.href.includes("localhost") ||
  window?.location?.href.includes("127.0.0.0");

export const BACKEND_URL = isLocalhost
  ? "http://localhost:8001"
  : "https://converge-backend.sleebit.com";

export const PAYMENTS_AUTH_URL = isLocalhost
  ? "https://payments.sleebit.com/v1"
  : "https://payments.sleebit.com/v1";

export const PROJECT_ID = isLocalhost
  ? "68aa76141f3a2d001c93e576"
  : "68aa76141f3a2d001c93e576";

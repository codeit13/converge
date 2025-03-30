const isLocalhost =
  window?.location?.href.includes("localhost") ||
  window?.location?.href.includes("127.0.0.0");

export const BACKEND_URL = isLocalhost
  ? "http://localhost:8000"
  : "https://converge-backend.sleebit.com";

export const PAYMENTS_AUTH_URL = isLocalhost
  ? "http://localhost:3000/v1"
  : "https://payments.sleebit.com/v1";

export const PROJECT_ID = isLocalhost
  ? "67e45b67cd2f9d001b6ec778"
  : "67e45b67cd2f9d001b6ec778";

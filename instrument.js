const Sentry = require("@sentry/node");

const DSN = "https://d21115d9c71acb4ba224be1fe334460f@o4511932881502208.ingest.de.sentry.io/4511947440259152";
const isProduction = process.env.VERCEL_ENV === "production" || process.env.NODE_ENV === "production";

Sentry.init({
  dsn: process.env.SENTRY_DSN || DSN,
  environment: process.env.VERCEL_ENV || process.env.NODE_ENV || "development",
  release: process.env.VERCEL_GIT_COMMIT_SHA || undefined,
  enableLogs: true,
  tracesSampleRate: isProduction ? 0.1 : 1.0,
  sendDefaultPii: false,
  dataCollection: {
    userInfo: false,
    httpBodies: [],
  },
});

module.exports = Sentry;

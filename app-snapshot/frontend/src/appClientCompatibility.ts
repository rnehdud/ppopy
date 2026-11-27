export const APP_COMPATIBILITY_CONTRACT = "skinanalysis.app-client-compatibility.v1" as const;

export type AppPlatform = "ios" | "android";
export type AppReleaseChannel = "test" | "production";

export type AppClientIdentity = {
  platform: AppPlatform;
  releaseChannel: AppReleaseChannel;
  version: string;
  build: number;
};

export type AppCompatibilityEnvelope = {
  contract: typeof APP_COMPATIBILITY_CONTRACT;
  platform: AppPlatform;
  release_channel: AppReleaseChannel;
  minimum_supported_version: string;
  minimum_supported_build: number;
  latest_version: string;
  latest_build: number;
};

export type AppCompatibilityState =
  | "supported"
  | "update_available"
  | "update_required"
  | "verification_unavailable";

export type AppOperation =
  | "admission"
  | "intake"
  | "purchase"
  | "catalog_read"
  | "draft_read"
  | "result_read"
  | "logout"
  | "account_deletion"
  | "support"
  | "manage_subscription"
  | "purchase_settlement";

const guardedOperations = new Set<AppOperation>(["admission", "intake", "purchase"]);
const exactSemver = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

function validVersion(value: unknown): value is string {
  return typeof value === "string" && exactSemver.test(value);
}

function validBuild(value: unknown): value is number {
  return typeof value === "number" && Number.isSafeInteger(value) && value > 0;
}

function isEnvelope(value: unknown): value is AppCompatibilityEnvelope {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const candidate = value as Record<string, unknown>;
  const exactKeys = new Set([
    "contract", "platform", "release_channel", "minimum_supported_version",
    "minimum_supported_build", "latest_version", "latest_build",
  ]);
  if (Object.keys(candidate).length !== exactKeys.size || Object.keys(candidate).some(key => !exactKeys.has(key))) return false;
  return candidate.contract === APP_COMPATIBILITY_CONTRACT
    && (candidate.platform === "ios" || candidate.platform === "android")
    && (candidate.release_channel === "test" || candidate.release_channel === "production")
    && validVersion(candidate.minimum_supported_version)
    && validBuild(candidate.minimum_supported_build)
    && validVersion(candidate.latest_version)
    && validBuild(candidate.latest_build)
    && candidate.minimum_supported_build <= candidate.latest_build;
}

export function evaluateAppCompatibility({
  serverVerified,
  client,
  response,
}: {
  serverVerified: boolean;
  client: AppClientIdentity;
  response: unknown;
}): AppCompatibilityState {
  if (!serverVerified || !validVersion(client.version) || !validBuild(client.build) || !isEnvelope(response)) {
    return "verification_unavailable";
  }
  if (response.platform !== client.platform || response.release_channel !== client.releaseChannel) {
    return "verification_unavailable";
  }
  if (client.build < response.minimum_supported_build) return "update_required";
  if (client.build < response.latest_build) return "update_available";
  return "supported";
}

export function appOperationAllowed(state: AppCompatibilityState, operation: AppOperation): boolean {
  if (state === "supported" || state === "update_available") return true;
  return !guardedOperations.has(operation);
}

export async function loadAppCompatibilityState({
  client,
  read,
}: {
  client: AppClientIdentity;
  read: (platform: AppPlatform, releaseChannel: AppReleaseChannel) => Promise<unknown>;
}): Promise<AppCompatibilityState> {
  try {
    const response = await read(client.platform, client.releaseChannel);
    return evaluateAppCompatibility({serverVerified:true, client, response});
  } catch {
    return "verification_unavailable";
  }
}

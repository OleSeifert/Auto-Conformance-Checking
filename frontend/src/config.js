/**
 * @fileoverview This file contains the configuration for the API endpoints.
 * It defines the base URL and specific endpoints for various functionalities.
 * It is used here to avoid hardcoding the URLs in multiple places, making it easier
 * to manage and update them in the future.
 */

export const API_BASE= "http://localhost:8000";
export const CELONIS_CONNECTION = `${API_BASE}/api/setup/celonis-credentials`;
export const CELONIS_LOG_UPLOAD = `${API_BASE}/api/logs/upload-log`;
export const GET_COLUMN_NAMES = `${API_BASE}/api/setup/get-column-names`;
export const COMMIT_LOG_TO_CELONIS = `${API_BASE}/api/logs/commit-log-to-celonis`;

// Log Skeleton Endpoints
export const COMPUTE_SKELETON = `${API_BASE}/api/log-skeleton/compute-skeleton`;
export const GET_EQUVALENCE = `${API_BASE}/api/log-skeleton/get_equivalence`;
export const GET_ALWAYS_BEFORE = `${API_BASE}/api/log-skeleton/get_always_before`;
export const GET_ALWAYS_AFTER = `${API_BASE}/api/log-skeleton/get_always_after`;
export const GET_NEVER_TOGETHER = `${API_BASE}/api/log-skeleton/get_never_together`;
export const GET_DIRECTLY_FOLLOWS = `${API_BASE}/api/log-skeleton/get_directly_follows`;
export const GET_ACTIVITY_FREQUENCIES = `${API_BASE}/api/log-skeleton/get_activity_frequencies`;

//Declerative Constraints Endpoints

// Temporal Profile Endpoints
export const TEMPORAL_PROFILE = `${API_BASE}/api/temporal-profile/compute-result`;
export const GET_RESULT_TEMPORAL_PROFILE = `${API_BASE}/api/temporal-profile/get-result`;

//Resource-Based Endpoints
export const RESOURCE_BASED = `${API_BASE}/api/resource-based/compute`;
export const HANDOVER_OF_WORK = `${API_BASE}/api/resource-based/sna/handover-of-work`;
export const SUBCONTRACTING= `${API_BASE}/api/resource-based/sna/subcontracting`;
export const WORKING_TOGETHER= `${API_BASE}/api/resource-based/sna/working-together`;
export const SIMILAR_ACTIVITIES = `${API_BASE}/api/resource-based/sna/similar-activities`;
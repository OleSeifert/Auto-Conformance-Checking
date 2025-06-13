/**
 * @fileoverview This file contains the configuration for the API endpoints.
 * It defines the base URL and specific endpoints for various functionalities.
 * It is used here to avoid hardcoding the URLs in multiple places, making it easier
 * to manage and update them in the future.
 */

//Configuration to celonis endpoints
export const API_BASE = "http://localhost:8000";
// export const API_BASE = "http://backend:8000/api";
export const CELONIS_CONNECTION = `${API_BASE}/api/setup/celonis-credentials`;
export const CELONIS_LOG_UPLOAD = `${API_BASE}/api/logs/upload-log`;
export const GET_COLUMN_NAMES = `${API_BASE}/api/setup/get-column-names`;
export const COMMIT_LOG_TO_CELONIS = `${API_BASE}/api/logs/commit-log-to-celonis`;
export const GET_GENERAL_INSIGHTS = `${API_BASE}/api/general/get-general-information`;

// Log Skeleton Endpoints
export const COMPUTE_SKELETON = `${API_BASE}/api/log-skeleton/compute-skeleton`;
export const GET_EQUIVALENCE = `${API_BASE}/api/log-skeleton/old/get_equivalence`;
export const GET_EQUIVALENCE_PQL = `${API_BASE}/api/log-skeleton/get_equivalence`;
export const GET_ALWAYS_BEFORE = `${API_BASE}/api/log-skeleton/old/get_always_before`;
export const GET_ALWAYS_BEFORE_PQL = `${API_BASE}/api/log-skeleton/get_always_before`;
export const GET_ALWAYS_AFTER = `${API_BASE}/api/log-skeleton/old/get_always_after`;
export const GET_ALWAYS_AFTER_PQL = `${API_BASE}/api/log-skeleton/get_always_after`;
export const GET_NEVER_TOGETHER = `${API_BASE}/api/log-skeleton/old/get_never_together`;
export const GET_NEVER_TOGETHER_PQL = `${API_BASE}/api/log-skeleton/get_never_together`;
export const GET_DIRECTLY_FOLLOWS = `${API_BASE}/api/log-skeleton/old/get_directly_follows`;
export const GET_ACTIVITY_FREQUENCIES = `${API_BASE}/api/log-skeleton/old/get_activity_frequencies`;
export const GET_DIRECTLY_FOLLOWS_AND_COUNT_PQL = `${API_BASE}/api/log-skeleton/get_directly_follows_and_count`;

//Declerative Constraints Endpoints

// Temporal Profile Endpoints
export const TEMPORAL_PROFILE = `${API_BASE}/api/temporal-profile/compute-result`;
export const GET_RESULT_TEMPORAL_PROFILE = `${API_BASE}/api/temporal-profile/get-result`;

//Resource-Based Endpoints
//# **************** SNA Endpoints ****************
export const RESOURCE_BASED = `${API_BASE}/api/resource-based/compute`;
export const HANDOVER_OF_WORK = `${API_BASE}/api/resource-based/sna/handover-of-work`;
export const SUBCONTRACTING = `${API_BASE}/api/resource-based/sna/subcontracting`;
export const WORKING_TOGETHER = `${API_BASE}/api/resource-based/sna/working-together`;
export const SIMILAR_ACTIVITIES = `${API_BASE}/api/resource-based/sna/similar-activities`;

// **************** Role Discovery Endpoints ****************
export const ROLE_DISCOVERY = `${API_BASE}/api/resource-based/role-discovery`;

// **************** Resource Profile Endpoints ****************
export const DISTINCT_ACTIVITIES = `${API_BASE}/api/resource-based/resource-profile/distinct-activities`;
export const DISTINCT_ACTIVITIES_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/distinct-activities`;
export const ACTIVITY_FREQUENCY = `${API_BASE}/api/resource-based/resource-profile/activity-frequency`;
export const ACTIVITY_FREQUENCY_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/activity-frequency`;
export const ACTIVITY_COMPLETIONS = `${API_BASE}/api/resource-based/resource-profile/activity-completions`;
export const ACTIVITY_COMPLETIONS_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/activity-completions`;
export const CASE_COMPLETIONS = `${API_BASE}/api/resource-based/resource-profile/case-completions`;
export const CASE_COMPLETIONS_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/case-completions`;
export const FRACTION_CASE_COMPLETIONS = `${API_BASE}/api/resource-based/resource-profile/fraction-case-completions`;
export const FRACTION_CASE_COMPLETIONS_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/fraction-case-completions`;
export const AVERAGE_WORKLOAD = `${API_BASE}/api/resource-based/resource-profile/average-workload`;
export const AVERAGE_WORKLOAD_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/average-workload`;
export const MULTITASKING = `${API_BASE}/api/resource-based/resource-profile/multitasking`;
export const AVERAGE_ACTIVITY_DURATION = `${API_BASE}/api/resource-based/resource-profile/average-activity-duration`;
export const AVERAGE_CASE_DURATION = `${API_BASE}/api/resource-based/resource-profile/average-case-duration`;
export const INTERACTION_TWO_RESOURCES = `${API_BASE}/api/resource-based/resource-profile/interaction-two-resources`;
export const INTERACTION_TWO_RESOURCES_PQL = `${API_BASE}/api/resource-based/pql/resource-profile/interaction-two-resources`;
export const SOCIAL_POSITION = `${API_BASE}/api/resource-based/resource-profile/social-position`;

// **************** Organizational Mining Endpoints****************
export const GROUP_RELATIVE_FOCUS = `${API_BASE}/api/resource-based/organizational-mining/group-relative-focus`;
export const GROUP_RELATIVE_STATE = `${API_BASE}/api/resource-based/organizational-mining/group-relative-stake`;
export const GROUP_COVERAGE = `${API_BASE}/api/resource-based/organizational-mining/group-coverage`;
export const GROUP_MEMBER_CONTRIBUTION = `${API_BASE}/api/resource-based/organizational-mining/group-member-contribution`;

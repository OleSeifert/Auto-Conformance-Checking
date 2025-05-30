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
export const MAPPING_COLUMNS = `${API_BASE}/api/setup/map-columns`;
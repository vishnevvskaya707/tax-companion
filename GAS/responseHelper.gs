const JSON_MIME = ContentService.MimeType.JSON;

/**
 * Creates a standardized success response
 * @param {Object} data - Additional data to include in the response
 * @return {ContentService.TextOutput} Formatted success response
 */
function successResponse(data) {
  return createResponse({ success : true, ...data });
}

/**
 * Creates a standardized error response
 * @param {string|Error} [message="Unknown error"] - Error message or Error object
 * @return {ContentService.TextOutput} Formatted error response
 */
function errorResponse(message = "Unknown error") {
  return createResponse({ 
    success : false, 
    error : message instanceof Error ? message.message : message
  });
}

/**
 * Creates a formatted HTTP JSON response
 * @param {Object} data - Data to be stringified
 * @return {ContentService.TextOutput} Response with JSON MIME type
 */
function createResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(JSON_MIME);
}
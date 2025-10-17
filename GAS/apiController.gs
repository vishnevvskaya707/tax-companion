/**
 * Main entry point for all POST requests. Routes requests based on action parameter
 * @param {Object} e - Event object containing the POST request data
 * @return {ContentService.TextOutput} JSON response with success/error
 */
function doPost(e) {
  try {
    const request = JSON.parse(e.postData.contents);
    let result;

    // Route request based on action type
    switch (request.action) {
      case "check_user":
        result = checkUserExists(request);
        break;
      case "activate":
        result = handleActivation(request);
        break;
      case "deactivate":
        result = handleDeactivation(request);
        break;
      case "update_income":
        result = handleIncomeUpdate(request);
        break;
      case "payment_details":
        result = handleGetPaymentDetails(request);
        break;
      default:
        return errorResponse("Invalid action");
    }

    return result.success
      ? successResponse(result.user || result.payment || null)
      : errorResponse(e.message);

  } catch(e) {
    return errorResponse(e.message);
  }
}

/**
 * Checks if a user exists in the system
 * @param {string} telegramId - User's Telegram ID
 * @return {Object} Result object with: success, user, error
 */
function checkUserExists({telegramId}) {
  const user_id = findUserByTelegramId(telegramId);
  if (!user_id) return { success : false, error : "User not found" };
  
  return { success : true, user_id};
}

/**
 * Handles user account activation
 * @param {Object} params - Activation parameters
 *    @param {string} params.telegramId - User's Telegram ID
 *    @param {string} params.accessCode - User's access code
 * @return {Object} Result object with operation status
 */
function handleActivation({telegramId, accessCode}) {
  const user_id = findUserByCredentials(telegramId, accessCode);
  if (!user_id) return { success : false, error : "Invalid credentials" };

  updateUserStatus(user_id, "Активен");
  return { success : true, user : getUserInfo(user_id) };
}

/**
 * Handles user account deactivation
 * @param {Object} params - Deactivation parameters
 *    @param {string} params.telegramId - User's Telegram ID
 * @return {Object} Result object with operation status
 */
function handleDeactivation({telegramId}) {
  const user_id = findUserByTelegramId(telegramId);
  if (!user_id) return { success : false, error : "User not found" };

  updateUserStatus(user_id, 'Неактивен');
  return { success : true, user : getUserInfo(user_id) };
}

/**
 * Updates user income for specified period
 * @param {Object} params - Request parameters
 *    @param {string} params.telegramId
 *    @param {string} params.period (format: MM_YYYY)
 *    @param {number} params.amount
 * @return {Object} Result object
 */
function handleIncomeUpdate({telegramId, period, amount}) {
  const user_id = findUserByTelegramId(telegramId);
  if (!user_id) return { success : false, error : "User not found" };

  updateReportIncome(user_id, period, amount);
  return { success : true, user : getUserInfo(user_id)};
}


function handleGetPaymentDetails({telegramId}) {
  const user_id = findUserByTelegramId(telegramId);
  if (!user_id) return { success : false, error : "User not fonud" };

  const paymentDetails = getUserPaymentDetails(user_id);
  return { success : true, payment : paymentDetails };
}
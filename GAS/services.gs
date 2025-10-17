/**
 * Finds a user by Telegram ID and access code with input normalization
 * @param {string|number} telegramId - User's Telegram ID
 * @param {string} accessCode - User's access code
 * @return {Object|null} User object if found, null otherwise
 */
function findUserByCredentials(telegramId, accessCode) {
  const cleanTgId = String(telegramId).trim();
  const cleanCode = String(accessCode).trim().toUpperCase();

  return findUser((user, row) =>
    cleanTgId === String(user.telegramId).trim() &&
    cleanCode === String(row[4]).trim().toUpperCase()
  );
}

/**
 * Finds a user by Telegram ID with input sanitization
 * @param {string|number} telegramId - User's Telegram ID
 * @return {Object|null} User object if found, null otherwise
 */
function findUserByTelegramId(telegramId) {
  return findUser(user =>
    String(telegramId).trim() === String(user.telegramId).trim()
  );
}

/**
 * Updates the user's income report
 * @param {string} userId - User ID
 * @param {string} period - Report period (month/year)
 * @param {number} amount - Income amount
 * @returns {Object|Promise} The object with the error or the result of updateIncome()
 */
function updateReportIncome(userId, period, amount) {
  typeof amount !== 'number' || amount <= 0 ? 
  { success : false, error : "Amount must be positive integer"} 
  : updateIncome(userId, period, amount);
}

function getUserPaymentDetails(userId) {
  const [tax, accounting] = [getTaxTotalAmount(userId), getAccountingServices(userId)];
  if (!tax && !accounting) return null;

  const tariffAmount = accounting?.tariff?.amount || 0
  const serviceAmount = accounting?.additionalService?.amount || 0

  return {
    ...(tax && { taxAmount : tax.taxAmount }),
    ...(accounting && {
      accountingAmount: {
        ...accounting.tariff && { tariff : accounting.tariff },
        ...accounting.additionalService && { additionalService : accounting.additionalService}
      }
    }),
    totalAmount: (tax?.taxAmount || 0) + tariffAmount + serviceAmount 
  };
} 
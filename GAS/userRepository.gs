const USER_SHEET_NAME = "Клиенты";

/**
 * Retrieves the user data sheet by name
 * @return {GoogleAppsScript.Spreadsheet.Sheet} The sheet object
 */
function getUserSheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(USER_SHEET_NAME);
}

/**
 * Finds a user matching specific conditions
 * @param {Function} conditionFn - Callback function that tests each user
 *    @param {Object} conditionFn.user - Mapped user object
 *    @param {Array} conditionFn.rawRow - Original row data
 *    @return {boolean} Whether user matches condition
 * @return {Object|null} Found user object or null if not found
 */
function findUser(conditionFn) {
  const data = getUserSheet().getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const user = mapRowToUser(data[i]);
    if (conditionFn(user, data[i])) {
      return user.id;
    }
  }
  return null;
}

/**
 * Updates user status in the sheet
 * @param {string|number} userId - ID from column A
 * @param {string} newStatus - New status value
 * @return {boolean} True if update succeeded, false if user not found
 */
function updateUserStatus(userId, newStatus) {
  const sheet = getUserSheet();
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (String(data[i][0]) === String(userId)) {
      sheet.getRange(i + 1, 8).setValue(newStatus);
      return true;
    }
  }
  return false;
}

/**
 * Maps spreadsheet row to user object
 * @param {Array} row - Spreadsheet row data
 * @return {Object|null} User object with named properties
 */
function mapRowToUser(row) {
  return row ? {
    id: row[0],
    fullName: row[1],
    telegramId: row[2],
    email: row[3],
    accessCode: row[4],
    registrationDate: row[5],
    birthDate: row[6],
    status: row[7],
    inn: row[8]
  } : null;
}

/**
 * Retrieves complete user information including last payment details
 * @param {string|number} userId - The user ID to look up
 * @return {Object} Returns an object containing
 */
function getUserInfo(userId) {
  try {
    const [client, payment] = [getUserSheet(), getPaymentSheets(PAYMENT_SHEET_NAME)].map(sheet => sheet.getDataRange().getValues());
    const findRow = (data, offset) => data.slice(offset).findIndex(row => String(row[0]) === String(userId)) + offset;

    const clientRow = findRow(client, 3);
    if (clientRow < 3) return { success : false, error : "User not found" };
    const paymentRow = findRow(payment, 4);

    return {
      success: true,
      user: {
        fullName: client[clientRow][1],
        birthDate: client[clientRow][6],
        email: client[clientRow][3]
      },
      lastPayment: paymentRow >= 4 ? {
        amount: payment[paymentRow][14],
        date: payment[paymentRow][15]
      } : null
    };

  } catch(e) {
    return { success : false, error : e.message };
  }
}
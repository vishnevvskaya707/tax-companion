const PAYMENT_SHEET_NAME = "Платежи";
const TAX_SHEET_NAME = "Налоги";
const ACCOUNTING_SHEET_NAME = "Тарифы";
const PAYMENT_ROW = 3;
const TOTAL_TAX_COL = 7;

/**
 * Retrieves the payment data sheet by name
 * @return {GoogleAppsScript.Spreadsheet.Sheet} The sheet object
 */
function getPaymentSheets(sheetName) {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
}

/**
 * Updates the income amount for the specified user and period
 * @param {string} userId - user ID
 * @param {string} targetPeriod - Target period in the format
 * @param {number} amount - Amount to write
 * @returns {boolean} - Returns true on successful update, false if data not found
 */
function updateIncome(userId, targetPeriod, amount) {
  const sheet = getPaymentSheets(PAYMENT_SHEET_NAME);
  const data = sheet.getDataRange().getValues();

  const periodCol = data[PAYMENT_ROW].slice(1).findIndex(p => String(p) === String(targetPeriod)) + 1;
  if (periodCol < 1) return false;

  const userRow = data.slice(4).findIndex(row => String(row[0]) === String(userId)) + 4;
  if (userRow < 4) return false;

  sheet.getRange(userRow + 1, periodCol + 1).setValue(amount);

  sheet.getRange(userRow + 1, 15).setValue(amount);
  sheet.getRange(userRow + 1, 16).setValue(new Date());
  return true;
}

/**
 * Gets tax total amount for user from Налоги sheet
 * @param {string} userId - User ID
 * @return {number|null} Tax amount or null if not found
 */
function getTaxTotalAmount(userId) {
  const data = getPaymentSheets(TAX_SHEET_NAME).getDataRange().getValues();

  const userRow = data.find(row => String(row[0]) === String(userId));
  return userRow ? { taxAmount : userRow[TOTAL_TAX_COL] } : null;
}

function getAccountingServices(userId) {
  const data = getPaymentSheets(ACCOUNTING_SHEET_NAME).getDataRange().getValues();
  const userRow = data.find(row => String(row[0]) === String(userId));

  const isUnpaid = status => String(status).trim().toLowerCase() === 'не оплачен';
  const payment = mapRowToPayment(userRow)
  const result = {};

  if (isUnpaid(payment.tariffStatus)) {
    result.tariff = {
      name: payment.tariffName,
      amount: payment.tariffAmount,
    };
  }
  if (isUnpaid(payment.serviceStatus)) {
    result.additionalService = {
      name: payment.serviceName,
      amount: payment.serviceAmount
    }
  }

  return Object.keys(result).length ? result : null;
}

function mapRowToPayment(row) {
  return row ? {
    tariffName: row[2],
    tariffAmount: row[3],
    tariffStatus: row[4],
    serviceName: row[6],
    serviceAmount: row[7],
    serviceStatus: row[8]
  } : null;
}
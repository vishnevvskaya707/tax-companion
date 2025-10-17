/**
 * Weekly saving of the table in Google Drive (logging)
 */
function weeklyBackUp() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const folder = DriveApp.getFolderById("");

  const date = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd");
  const backupName = `Backup_${sheet.getName()}_${date}`;

  DriveApp.getFileById(sheet.getId()).makeCopy(backupName, folder)
}

/**
 * Sheets.gs
 * Generic helpers for reading/writing sheet data as arrays of plain objects,
 * keyed by the header row. Every other file talks to the spreadsheet through
 * these functions rather than touching Range/Sheet objects directly, so the
 * schema only has to be described once (see SHEET_NAMES / headers below).
 */

const SHEET_NAMES = {
  BUILDINGS: 'Buildings',
  STAFF: 'Staff',
  STUDENTS: 'Students',
  REFERRAL_TYPES: 'Referral_Types',
  LOCATIONS: 'Locations',
  PERIODS: 'Periods',
  REFERRALS: 'Referrals',
  AUDIT_LOG: 'Audit_Log'
};

/**
 * IMPORTANT: appendRow_/updateRow_ address columns by POSITION (this array's
 * order), not by re-reading the sheet's actual header row. So a header row
 * created before some field existed only has the columns that existed at the
 * time. getOrCreateSheet_ migrates that gap automatically by appending any
 * newly-added headers to the END of row 1 the next time the sheet is opened —
 * which only works if new fields are always ADDED AT THE END of a sheet's
 * array here, never inserted in the middle or reordered. Do that and existing
 * spreadsheets (with existing data) upgrade themselves with no manual step.
 */
const HEADERS = {
  Buildings: ['building_id', 'building_name', 'principal_email'],
  Staff: ['email', 'name', 'role', 'building_id'],
  Students: ['student_id', 'first_name', 'last_name', 'building_id', 'grade'],
  Referral_Types: ['code', 'label', 'tier'],
  Locations: ['code', 'label'],
  Periods: ['code', 'label'],
  Referrals: [
    'referral_id', 'student_id', 'referring_staff_email', 'building_id',
    'referral_type_code', 'date_time', 'description', 'status',
    'assigned_to_email', 'resolution_notes', 'closed_date',
    // Added later — see the migration note above.
    'incident_time', 'location_code', 'period_code'
  ],
  Audit_Log: ['referral_id', 'changed_by', 'timestamp', 'change']
};

/**
 * Returns the spreadsheet this app stores its data in — whichever one it
 * already created (its ID is remembered in Script Properties), or the bound
 * spreadsheet if this script happens to live inside one, or a brand new one
 * created on first run.
 */
function getSpreadsheet_() {
  const props = PropertiesService.getScriptProperties();
  const storedId = props.getProperty('DATA_SPREADSHEET_ID');
  if (storedId) {
    return SpreadsheetApp.openById(storedId);
  }
  const bound = SpreadsheetApp.getActiveSpreadsheet();
  if (bound) {
    props.setProperty('DATA_SPREADSHEET_ID', bound.getId());
    return bound;
  }
  const created = SpreadsheetApp.create('Behavior Tracker Data');
  props.setProperty('DATA_SPREADSHEET_ID', created.getId());
  return created;
}

/**
 * Returns (creating if necessary) the data spreadsheet's sheet by name.
 * Also migrates an existing sheet whose header row predates fields that have
 * since been added to HEADERS above — it appends the missing header cells to
 * the end of row 1, so existing data and columns are never disturbed and you
 * never have to manually edit column headers after an update.
 */
function getOrCreateSheet_(name) {
  const ss = getSpreadsheet_();
  let sheet = ss.getSheetByName(name);
  const expectedHeaders = HEADERS[name];
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(expectedHeaders);
    sheet.setFrozenRows(1);
    return sheet;
  }
  const lastCol = sheet.getLastColumn();
  const currentHeaderCount = lastCol > 0 ? sheet.getRange(1, 1, 1, lastCol).getValues()[0].length : 0;
  const missing = expectedHeaders.slice(currentHeaderCount);
  if (missing.length > 0) {
    sheet.getRange(1, currentHeaderCount + 1, 1, missing.length).setValues([missing]);
  }
  return sheet;
}

/** Reads a whole sheet into an array of plain objects keyed by its header row. */
function readSheet_(name) {
  const sheet = getOrCreateSheet_(name);
  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return [];
  const headers = values[0];
  const rows = values.slice(1);
  return rows
    .filter(row => row.some(cell => cell !== '' && cell !== null))
    .map((row, i) => {
      const obj = { _row: i + 2 }; // 1-indexed sheet row, header is row 1
      headers.forEach((h, idx) => { obj[h] = row[idx]; });
      return obj;
    });
}

/**
 * Appends one row, built from an object, to the named sheet. Returns the row number.
 * Holds a script-wide lock while writing so two staff submitting/updating at
 * the same instant can't collide (Sheets append is not atomic on its own).
 */
function appendRow_(name, record) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sheet = getOrCreateSheet_(name);
    const headers = HEADERS[name];
    const row = headers.map(h => (record[h] !== undefined ? record[h] : ''));
    sheet.appendRow(row);
    return sheet.getLastRow();
  } finally {
    lock.releaseLock();
  }
}

/** Updates specific fields on an existing row (1-indexed, as returned in `_row`). */
function updateRow_(name, rowNumber, fields) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sheet = getOrCreateSheet_(name);
    const headers = HEADERS[name];
    Object.keys(fields).forEach(key => {
      const col = headers.indexOf(key);
      if (col === -1) return;
      sheet.getRange(rowNumber, col + 1).setValue(fields[key]);
    });
  } finally {
    lock.releaseLock();
  }
}

/** Finds a single record by an exact match on one field, or null if not found. */
function findRecord_(name, field, value) {
  const records = readSheet_(name);
  return records.find(r => String(r[field]) === String(value)) || null;
}

/**
 * Converts a sheet cell's value to a plain ISO date string, or '' if empty/invalid.
 * Server functions must use this on any date-typed field before returning it
 * to the browser — google.script.run doesn't reliably deliver raw Date
 * objects across the bridge (some payloads silently arrive as `null` on the
 * client instead of an error), so dates are sent as strings and re-parsed
 * with `new Date(...)` on the client for display.
 */
function toIsoOrEmpty_(value) {
  if (!value) return '';
  const dt = (value instanceof Date) ? value : new Date(value);
  return isNaN(dt.getTime()) ? '' : dt.toISOString();
}

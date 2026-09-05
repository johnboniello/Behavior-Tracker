/**
 * Reports.gs
 * Standard (non-demographic) rollups, plus the full Analytics breakdown used
 * by the Analytics tab (location, period/activity, time of day, day of week,
 * grade, referral type — with optional filters and an optional live
 * demographic join). Demographic data is NEVER stored in this project's own
 * sheets — it's read live from a separate sheet you point at (e.g. an SIS
 * export you keep in your own Drive), joined in memory for one report, and
 * discarded. Nothing demographic gets written back anywhere.
 */

/** Basic counts any building_admin or district_admin can pull, no demographics involved. */
function getStandardReport(ctx) {
  requireRole_(ctx, ['building_admin', 'district_admin']);
  const referrals = readSheet_(SHEET_NAMES.REFERRALS)
    .filter(r => ctx.role === 'district_admin' || sameBuilding_(r.building_id, ctx.buildingId));
  const types = indexBy_(readSheet_(SHEET_NAMES.REFERRAL_TYPES), 'code');

  const byBuilding = {}, byType = {}, byStatus = {};
  referrals.forEach(r => {
    byBuilding[r.building_id] = (byBuilding[r.building_id] || 0) + 1;
    const typeLabel = (types[r.referral_type_code] || {}).label || r.referral_type_code;
    byType[typeLabel] = (byType[typeLabel] || 0) + 1;
    byStatus[r.status] = (byStatus[r.status] || 0) + 1;
  });

  return { totalReferrals: referrals.length, byBuilding, byType, byStatus };
}

/**
 * The full Analytics breakdown behind the Analytics tab: filterable counts by
 * location, period/activity, time of day, day of week, grade, referral type,
 * and building — plus an optional live demographic breakdown/filter.
 *
 * filters (all optional; omit/empty a field to mean "all"):
 *   buildingId, referralTypeCode, locationCode, periodCode, grade,
 *   dayOfWeek ('Monday'…), timeBlock ('Before 9am' etc, see timeBlockFor_),
 *   dateFrom, dateTo (yyyy-mm-dd),
 *   demographicsSheetId, demographicField, demographicValue
 *     — demographicsSheetId is required to use the other two; restricted to
 *       district_admin, same as the old equity report.
 */
function getAnalyticsReport(filters, ctx) {
  requireRole_(ctx, ['building_admin', 'district_admin']);
  filters = filters || {};

  const students = indexBy_(readSheet_(SHEET_NAMES.STUDENTS), 'student_id');
  const types = indexBy_(readSheet_(SHEET_NAMES.REFERRAL_TYPES), 'code');
  const locations = indexBy_(readSheet_(SHEET_NAMES.LOCATIONS), 'code');
  const periods = indexBy_(readSheet_(SHEET_NAMES.PERIODS), 'code');

  let referrals = readSheet_(SHEET_NAMES.REFERRALS);
  if (ctx.role !== 'district_admin') {
    referrals = referrals.filter(r => sameBuilding_(r.building_id, ctx.buildingId));
  }
  if (filters.buildingId) {
    referrals = referrals.filter(r => sameBuilding_(r.building_id, filters.buildingId));
  }
  if (filters.referralTypeCode) {
    referrals = referrals.filter(r => r.referral_type_code === filters.referralTypeCode);
  }
  if (filters.locationCode) {
    referrals = referrals.filter(r => r.location_code === filters.locationCode);
  }
  if (filters.periodCode) {
    referrals = referrals.filter(r => r.period_code === filters.periodCode);
  }
  if (filters.grade) {
    referrals = referrals.filter(r => sameValue_((students[r.student_id] || {}).grade, filters.grade));
  }
  if (filters.dateFrom) {
    const from = new Date(filters.dateFrom);
    referrals = referrals.filter(r => new Date(r.date_time) >= from);
  }
  if (filters.dateTo) {
    const to = new Date(filters.dateTo);
    to.setHours(23, 59, 59, 999);
    referrals = referrals.filter(r => new Date(r.date_time) <= to);
  }
  if (filters.dayOfWeek) {
    referrals = referrals.filter(r => dayOfWeekName_(r.date_time) === filters.dayOfWeek);
  }
  if (filters.timeBlock) {
    referrals = referrals.filter(r => timeBlockFor_(r.incident_time) === filters.timeBlock);
  }

  // Optional live demographic join — never stored, restricted to district_admin.
  let demoByStudent = null;
  if (filters.demographicsSheetId) {
    requireRole_(ctx, ['district_admin']);
    demoByStudent = loadDemographics_(filters.demographicsSheetId);
    if (filters.demographicField && filters.demographicValue) {
      referrals = referrals.filter(r => {
        const demo = demoByStudent[r.student_id];
        const value = demo ? (demo[filters.demographicField] || '(unspecified)') : '(not matched)';
        return value === filters.demographicValue;
      });
    }
  }

  const byLocation = {}, byPeriod = {}, byTimeBlock = {}, byDayOfWeek = {}, byGrade = {}, byType = {}, byBuilding = {};
  referrals.forEach(r => {
    const student = students[r.student_id] || {};
    bump_(byLocation, (locations[r.location_code] || {}).label || r.location_code || '(unspecified)');
    bump_(byPeriod, (periods[r.period_code] || {}).label || r.period_code || '(unspecified)');
    bump_(byTimeBlock, timeBlockFor_(r.incident_time));
    bump_(byDayOfWeek, dayOfWeekName_(r.date_time));
    bump_(byGrade, student.grade != null && student.grade !== '' ? ('Grade ' + String(student.grade).toUpperCase()) : '(unspecified)');
    bump_(byType, (types[r.referral_type_code] || {}).label || r.referral_type_code);
    bump_(byBuilding, r.building_id);
  });

  let demographics = null;
  if (demoByStudent && filters.demographicField) {
    demographics = {};
    referrals.forEach(r => {
      const demo = demoByStudent[r.student_id];
      const value = demo ? (demo[filters.demographicField] || '(unspecified)') : '(not matched)';
      bump_(demographics, value);
    });
  }

  return { totalReferrals: referrals.length, byLocation, byPeriod, byTimeBlock, byDayOfWeek, byGrade, byType, byBuilding, demographics };
}

/** Column names (other than student_id) available in a demographics sheet, for the field picker. */
function getDemographicFields(demographicsSheetId, ctx) {
  requireRole_(ctx, ['district_admin']);
  const demoSheet = SpreadsheetApp.openById(demographicsSheetId).getSheets()[0];
  const headers = demoSheet.getRange(1, 1, 1, demoSheet.getLastColumn()).getValues()[0];
  if (headers.indexOf('student_id') === -1) {
    throw new Error('The demographics sheet must have a "student_id" column.');
  }
  return headers.filter(h => h !== 'student_id');
}

/** Builds a student_id -> {field: value} lookup from an external sheet, live, in memory only. */
function loadDemographics_(demographicsSheetId) {
  const demoSheet = SpreadsheetApp.openById(demographicsSheetId).getSheets()[0];
  const values = demoSheet.getDataRange().getValues();
  const headers = values[0];
  const studentIdCol = headers.indexOf('student_id');
  if (studentIdCol === -1) {
    throw new Error('The demographics sheet must have a "student_id" column.');
  }
  const demoByStudent = {};
  values.slice(1).forEach(row => {
    const id = row[studentIdCol];
    if (!id) return;
    const record = {};
    headers.forEach((h, i) => { if (h !== 'student_id') record[h] = row[i]; });
    demoByStudent[id] = record;
  });
  return demoByStudent;
}

function bump_(map, key) {
  map[key] = (map[key] || 0) + 1;
}

function dayOfWeekName_(dateValue) {
  if (!dateValue) return '(unspecified)';
  const dt = new Date(dateValue);
  if (isNaN(dt.getTime())) return '(unspecified)';
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dt.getDay()];
}

/** Buckets a "HH:MM" incident time into a school-day block for charting. */
function timeBlockFor_(timeStr) {
  if (!timeStr) return '(unspecified)';
  const hour = parseInt(String(timeStr).split(':')[0], 10);
  if (isNaN(hour)) return '(unspecified)';
  if (hour < 9) return 'Before 9am';
  if (hour < 11) return '9–11am';
  if (hour < 13) return '11am–1pm';
  if (hour < 15) return '1–3pm';
  return 'After 3pm';
}

/**
 * Referrals.gs
 * Core case-management logic: create, list (role-filtered), assign, close.
 * No demographic data is ever read or written here — see Reports.gs for the
 * report-time-only join.
 */

/** Creates a new referral from a submitted form. Returns the new referral_id. */
function createReferral(formData, ctx) {
  if (!formData.student_id || !formData.referral_type_code) {
    throw new Error('Student and referral type are required.');
  }
  if (!formData.location_code) throw new Error('Location is required.');
  if (!formData.period_code) throw new Error('Period/activity is required.');
  const student = findRecord_(SHEET_NAMES.STUDENTS, 'student_id', formData.student_id);
  if (!student) throw new Error('Unknown student_id: ' + formData.student_id);

  const referralId = Utilities.getUuid();
  appendRow_(SHEET_NAMES.REFERRALS, {
    referral_id: referralId,
    student_id: formData.student_id,
    referring_staff_email: ctx.email,
    building_id: student.building_id,
    referral_type_code: formData.referral_type_code,
    date_time: new Date(),
    description: formData.description || '',
    status: 'open',
    assigned_to_email: '',
    resolution_notes: '',
    closed_date: '',
    incident_time: formData.incident_time || '',
    location_code: formData.location_code,
    period_code: formData.period_code
  });

  logAudit_(referralId, ctx.email, 'created (status: open)');
  notifyBuildingAdmin_(student.building_id, referralId, student);
  return referralId;
}

/** Returns referrals visible to this user, role-filtered, with display fields joined in. */
/** Case/whitespace-insensitive match, since these are typed by hand into a sheet. */
function sameValue_(a, b) {
  return String(a).trim().toUpperCase() === String(b).trim().toUpperCase();
}
/** Alias kept for readability at building-comparison call sites. */
function sameBuilding_(a, b) {
  return sameValue_(a, b);
}

function getReferralsForUser(ctx) {
  const referrals = readSheet_(SHEET_NAMES.REFERRALS);
  const students = indexBy_(readSheet_(SHEET_NAMES.STUDENTS), 'student_id');
  const types = indexBy_(readSheet_(SHEET_NAMES.REFERRAL_TYPES), 'code');
  const locations = indexBy_(readSheet_(SHEET_NAMES.LOCATIONS), 'code');
  const periods = indexBy_(readSheet_(SHEET_NAMES.PERIODS), 'code');

  let visible;
  if (ctx.role === 'district_admin') {
    visible = referrals;
  } else if (ctx.role === 'building_admin') {
    visible = referrals.filter(r => sameBuilding_(r.building_id, ctx.buildingId));
  } else if (ctx.role === 'counselor') {
    visible = referrals.filter(r => r.assigned_to_email === ctx.email && sameBuilding_(r.building_id, ctx.buildingId));
  } else { // teacher
    visible = referrals.filter(r => r.referring_staff_email === ctx.email);
  }

  return visible
    .map(r => {
      const student = students[r.student_id] || {};
      const type = types[r.referral_type_code] || {};
      const location = locations[r.location_code] || {};
      const period = periods[r.period_code] || {};
      return {
        referral_id: r.referral_id,
        student_name: (student.first_name || '?') + ' ' + (student.last_name || ''),
        grade: student.grade || '',
        building_id: r.building_id,
        referral_type: type.label || r.referral_type_code,
        location: location.label || r.location_code || '',
        period: period.label || r.period_code || '',
        incident_time: r.incident_time || '',
        date_time: toIsoOrEmpty_(r.date_time),
        description: r.description,
        status: r.status,
        assigned_to_email: r.assigned_to_email,
        resolution_notes: r.resolution_notes,
        closed_date: toIsoOrEmpty_(r.closed_date),
        referring_staff_email: r.referring_staff_email
      };
    })
    .sort((a, b) => new Date(b.date_time) - new Date(a.date_time));
}

/** Assigns an open referral to a counselor/admin. Only admins may assign. */
function assignReferral(referralId, assigneeEmail, ctx) {
  requireRole_(ctx, ['building_admin', 'district_admin']);
  const record = findRecord_(SHEET_NAMES.REFERRALS, 'referral_id', referralId);
  if (!record) throw new Error('Referral not found.');
  if (ctx.role === 'building_admin' && !sameBuilding_(record.building_id, ctx.buildingId)) {
    throw new Error('You can only assign referrals within your own building.');
  }

  updateRow_(SHEET_NAMES.REFERRALS, record._row, {
    status: 'assigned',
    assigned_to_email: assigneeEmail
  });
  logAudit_(referralId, ctx.email, 'status: open -> assigned (' + assigneeEmail + ')');
  notifyAssignee_(assigneeEmail, referralId, record);
}

/** Closes a referral. Assignee, building admin, or district admin may close it. */
function closeReferral(referralId, resolutionNotes, ctx) {
  const record = findRecord_(SHEET_NAMES.REFERRALS, 'referral_id', referralId);
  if (!record) throw new Error('Referral not found.');

  const canClose =
    ctx.role === 'district_admin' ||
    (ctx.role === 'building_admin' && sameBuilding_(record.building_id, ctx.buildingId)) ||
    (ctx.role === 'counselor' && record.assigned_to_email === ctx.email);
  if (!canClose) throw new Error('You do not have permission to close this referral.');

  updateRow_(SHEET_NAMES.REFERRALS, record._row, {
    status: 'closed',
    resolution_notes: resolutionNotes || '',
    closed_date: new Date()
  });
  logAudit_(referralId, ctx.email, 'status: ' + record.status + ' -> closed');
  notifyReferringTeacher_(record.referring_staff_email, referralId, record, resolutionNotes);
}

/** Staff a referral can be assigned to: counselors/admins in the same building (or all, for district_admin). */
function getAssignableStaff(ctx) {
  const staff = readSheet_(SHEET_NAMES.STAFF);
  return staff.filter(s => {
    const assignableRole = s.role === 'counselor' || s.role === 'building_admin';
    if (!assignableRole) return false;
    if (ctx.role === 'district_admin') return true;
    return sameBuilding_(s.building_id, ctx.buildingId);
  });
}

function getReferralTypes() {
  return readSheet_(SHEET_NAMES.REFERRAL_TYPES);
}

function getLocations() {
  return readSheet_(SHEET_NAMES.LOCATIONS);
}

function getPeriods() {
  return readSheet_(SHEET_NAMES.PERIODS);
}

function getBuildings() {
  return readSheet_(SHEET_NAMES.BUILDINGS);
}

/**
 * Students a teacher can file a referral for: their own building only.
 * District admins (buildingId 'ALL') can file for any building — otherwise
 * they'd be filtered against a building_id that matches no student rows.
 */
function getStudentsForBuilding(buildingId) {
  const students = readSheet_(SHEET_NAMES.STUDENTS);
  if (sameBuilding_(buildingId, 'ALL')) return students;
  return students.filter(s => sameBuilding_(s.building_id, buildingId));
}

function logAudit_(referralId, changedBy, change) {
  appendRow_(SHEET_NAMES.AUDIT_LOG, {
    referral_id: referralId,
    changed_by: changedBy,
    timestamp: new Date(),
    change: change
  });
}

function requireRole_(ctx, allowedRoles) {
  if (allowedRoles.indexOf(ctx.role) === -1) {
    throw new Error('This action requires one of these roles: ' + allowedRoles.join(', '));
  }
}

function indexBy_(records, key) {
  const out = {};
  records.forEach(r => { out[r[key]] = r; });
  return out;
}

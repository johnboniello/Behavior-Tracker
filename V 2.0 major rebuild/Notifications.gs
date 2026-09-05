/**
 * Notifications.gs
 * All outbound email. Uses MailApp (free, sends as the script owner) rather
 * than GmailApp, so it works the same regardless of whose account is
 * currently logged in.
 */

function appUrl_() {
  try {
    return ScriptApp.getService().getUrl();
  } catch (e) {
    return ''; // not yet deployed as a web app
  }
}

function notifyBuildingAdmin_(buildingId, referralId, student) {
  // Case/whitespace-insensitive match (see sameBuilding_ in Referrals.gs) — a
  // Buildings row typed as "WLB" must still match a student in "wLB".
  const building = readSheet_(SHEET_NAMES.BUILDINGS).find(b => sameBuilding_(b.building_id, buildingId));
  if (!building) {
    Logger.log('notifyBuildingAdmin_: no Buildings row matches building_id "' + buildingId + '" — no email sent.');
    return;
  }
  if (!building.principal_email) {
    Logger.log('notifyBuildingAdmin_: Buildings row for "' + buildingId + '" has no principal_email — no email sent.');
    return;
  }
  MailApp.sendEmail({
    to: building.principal_email,
    subject: 'New behavior referral: ' + student.first_name + ' ' + student.last_name,
    body:
      'A new referral was submitted for ' + student.first_name + ' ' + student.last_name +
      ' (' + student.student_id + ').\n\n' +
      'Open it here: ' + appUrl_() + '\n\n' +
      'Referral ID: ' + referralId
  });
}

function notifyAssignee_(assigneeEmail, referralId, referral) {
  MailApp.sendEmail({
    to: assigneeEmail,
    subject: 'Referral assigned to you',
    body:
      'A behavior referral has been assigned to you.\n\n' +
      'Open it here: ' + appUrl_() + '\n\n' +
      'Referral ID: ' + referralId
  });
}

function notifyReferringTeacher_(teacherEmail, referralId, referral, resolutionNotes) {
  if (!teacherEmail) return;
  MailApp.sendEmail({
    to: teacherEmail,
    subject: 'Update on your referral',
    body:
      'The referral you submitted has been closed.\n\n' +
      (resolutionNotes ? ('Resolution notes: ' + resolutionNotes + '\n\n') : '') +
      'View it here: ' + appUrl_() + '\n\n' +
      'Referral ID: ' + referralId
  });
}

/**
 * Optional: set this up as a daily time-based trigger (Triggers > Add Trigger
 * in the Apps Script editor) to nudge building admins about referrals that
 * have sat open too long.
 */
function sendStaleReferralReminders() {
  const DAYS_THRESHOLD = 3;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - DAYS_THRESHOLD);

  const referrals = readSheet_(SHEET_NAMES.REFERRALS)
    .filter(r => r.status !== 'closed' && new Date(r.date_time) < cutoff);
  if (referrals.length === 0) return;

  const byBuilding = {};
  referrals.forEach(r => {
    byBuilding[r.building_id] = byBuilding[r.building_id] || [];
    byBuilding[r.building_id].push(r);
  });

  Object.keys(byBuilding).forEach(buildingId => {
    const building = readSheet_(SHEET_NAMES.BUILDINGS).find(b => sameBuilding_(b.building_id, buildingId));
    if (!building || !building.principal_email) return;
    MailApp.sendEmail({
      to: building.principal_email,
      subject: byBuilding[buildingId].length + ' referral(s) open more than ' + DAYS_THRESHOLD + ' days',
      body:
        'The following referrals have been open for more than ' + DAYS_THRESHOLD + ' days:\n\n' +
        byBuilding[buildingId].map(r => '- ' + r.referral_id + ' (status: ' + r.status + ')').join('\n') +
        '\n\nReview them here: ' + appUrl_()
    });
  });
}

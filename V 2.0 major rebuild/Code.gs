/**
 * Code.gs
 * Entry point (doGet) and the ONLY functions the browser is allowed to call
 * directly via google.script.run. Every api_* function below derives the
 * current user's role/building itself from the logged-in session — it never
 * trusts a role or email passed up from the client. That's the actual
 * security boundary of this app: don't add a client-callable function that
 * accepts ctx/role/email as an argument from the page.
 */

function doGet(e) {
  try {
    getCurrentUserContext_(); // throws if the visitor isn't logged in / isn't in Staff
  } catch (err) {
    return HtmlService.createHtmlOutput(
      '<div style="font-family:sans-serif;max-width:32rem;margin:3rem auto;padding:1rem;">' +
      '<h2>Can\'t open this app</h2><p>' + err.message + '</p></div>'
    );
  }
  // Single-page app: everything lives in App.html, which switches views with
  // JS instead of query-string navigation (Apps Script's sandboxed frame
  // doesn't reliably support <a href="?page=..."> style links).
  const template = HtmlService.createTemplateFromFile('App');
  return template.evaluate()
    .setTitle('Behavior Referral Tracker')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** Lets HTML files pull in shared partials: <?!= include('Styles'); ?> */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * Resolves the logged-in visitor against the Staff sheet. This is the only
 * place role/building gets decided, and it's always derived from
 * Session.getActiveUser() — never from anything the client sends.
 */
function getCurrentUserContext_() {
  const email = Session.getActiveUser().getEmail();
  if (!email) {
    throw new Error('Could not determine your identity. Make sure you are logged into your district Google account.');
  }
  // Emails are typed into the Staff sheet by hand, so match case-insensitively.
  const staff = readSheet_(SHEET_NAMES.STAFF).find(s => sameEmail_(s.email, email));
  if (!staff) {
    throw new Error(
      email + ' is not registered in the Staff sheet yet. Ask your district admin to add you before you can use this app.'
    );
  }
  return { email: email.trim().toLowerCase(), role: staff.role, buildingId: staff.building_id, name: staff.name };
}

/* ---------------- Client-callable API (google.script.run targets) ---------------- */

function api_getDashboardData() {
  const ctx = getCurrentUserContext_();
  return {
    ctx: ctx,
    referrals: getReferralsForUser(ctx),
    assignableStaff: (ctx.role === 'building_admin' || ctx.role === 'district_admin') ? getAssignableStaff(ctx) : []
  };
}

function api_getSubmitFormData() {
  const ctx = getCurrentUserContext_();
  return {
    ctx: ctx,
    students: getStudentsForBuilding(ctx.buildingId),
    referralTypes: getReferralTypes(),
    locations: getLocations(),
    periods: getPeriods()
  };
}

function api_createReferral(formData) {
  const ctx = getCurrentUserContext_();
  return createReferral(formData, ctx);
}

function api_assignReferral(referralId, assigneeEmail) {
  const ctx = getCurrentUserContext_();
  return assignReferral(referralId, assigneeEmail, ctx);
}

function api_closeReferral(referralId, resolutionNotes) {
  const ctx = getCurrentUserContext_();
  return closeReferral(referralId, resolutionNotes, ctx);
}

function api_getStandardReport() {
  const ctx = getCurrentUserContext_();
  return getStandardReport(ctx);
}

/** Filter-bar options for the Analytics tab: reference lists plus, for a district admin, all buildings. */
function api_getAnalyticsFilters() {
  const ctx = getCurrentUserContext_();
  requireRole_(ctx, ['building_admin', 'district_admin']);
  return {
    ctx: ctx,
    referralTypes: getReferralTypes(),
    locations: getLocations(),
    periods: getPeriods(),
    buildings: ctx.role === 'district_admin' ? getBuildings() : []
  };
}

function api_getAnalyticsReport(filters) {
  const ctx = getCurrentUserContext_();
  return getAnalyticsReport(filters, ctx);
}

/** Column names available in a pasted demographics sheet, for the Analytics "breakdown by" picker. */
function api_getDemographicFields(demographicsSheetId) {
  const ctx = getCurrentUserContext_();
  return getDemographicFields(demographicsSheetId, ctx);
}

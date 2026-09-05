/**
 * Setup.gs
 * Run runInitialSetup() ONCE, manually, from the Apps Script editor after
 * pasting all the files in. It creates every sheet with the right headers
 * and registers whoever runs it as a district_admin, so you're not locked
 * out of your own app on the first load.
 *
 * Safe to run more than once — it won't duplicate sheets or overwrite data
 * that's already there.
 */
function runInitialSetup() {
  Object.values(SHEET_NAMES).forEach(name => getOrCreateSheet_(name));

  // Register whoever is running Setup as a district_admin, if not already staff.
  const me = Session.getActiveUser().getEmail();
  const existing = findRecord_(SHEET_NAMES.STAFF, 'email', me);
  if (!existing) {
    appendRow_(SHEET_NAMES.STAFF, {
      email: me,
      name: me.split('@')[0],
      role: 'district_admin',
      building_id: 'ALL'
    });
  }

  // Seed a couple of example referral types so the submission form isn't empty.
  const types = readSheet_(SHEET_NAMES.REFERRAL_TYPES);
  if (types.length === 0) {
    [
      { code: 'DISRUPT', label: 'Classroom disruption', tier: '1' },
      { code: 'PHYS', label: 'Physical aggression', tier: '2' },
      { code: 'PROPERTY', label: 'Property damage', tier: '2' },
      { code: 'DEFY', label: 'Defiance / non-compliance', tier: '1' }
    ].forEach(t => appendRow_(SHEET_NAMES.REFERRAL_TYPES, t));
  }

  // Seed default locations and periods — edit/add/remove rows in these sheets
  // any time; the submit form and Analytics tab always read them live.
  const locations = readSheet_(SHEET_NAMES.LOCATIONS);
  if (locations.length === 0) {
    [
      { code: 'CLASSROOM', label: 'Classroom' },
      { code: 'CAFETERIA', label: 'Cafeteria' },
      { code: 'HALLWAY', label: 'Hallway' },
      { code: 'BUS', label: 'Bus' },
      { code: 'RESTROOM', label: 'Restroom' },
      { code: 'GYM', label: 'Gym' },
      { code: 'LIBRARY', label: 'Library' },
      { code: 'PLAYGROUND', label: 'Playground / recess' },
      { code: 'ART', label: 'Art room' },
      { code: 'MUSIC', label: 'Music room' },
      { code: 'OFFICE', label: 'Main office' },
      { code: 'OTHER', label: 'Other' }
    ].forEach(l => appendRow_(SHEET_NAMES.LOCATIONS, l));
  }

  const periods = readSheet_(SHEET_NAMES.PERIODS);
  if (periods.length === 0) {
    [
      { code: 'ARRIVAL', label: 'Arrival / morning meeting' },
      { code: 'P1', label: 'Period 1' },
      { code: 'P2', label: 'Period 2' },
      { code: 'P3', label: 'Period 3' },
      { code: 'P4', label: 'Period 4' },
      { code: 'P5', label: 'Period 5' },
      { code: 'P6', label: 'Period 6' },
      { code: 'LUNCH', label: 'Lunch' },
      { code: 'RECESS', label: 'Recess' },
      { code: 'TRANSITION', label: 'Transition' },
      { code: 'SPECIALS', label: 'Specials (art/music/PE)' },
      { code: 'DISMISSAL', label: 'Dismissal' },
      { code: 'OTHER', label: 'Other' }
    ].forEach(p => appendRow_(SHEET_NAMES.PERIODS, p));
  }

  const ss = getSpreadsheet_();
  Logger.log(
    'Setup complete.\n' +
    'Data spreadsheet: ' + ss.getUrl() + '\n' +
    'Sheets created: ' + Object.values(SHEET_NAMES).join(', ') + '\n' +
    'Registered ' + me + ' as district_admin.\n' +
    'Next: open the data spreadsheet above and add rows to Buildings, Staff, and Students, ' +
    'then deploy as a web app (see README).'
  );
}

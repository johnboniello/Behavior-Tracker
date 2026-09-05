# Behavior Referral Tracker v2 — Apps Script Web App

A from-scratch rebuild: a proper multi-user web app with role-based access, instead of a shared
spreadsheet + dashboard. Free, runs entirely inside Google (no new vendor), customizable.

Demographic data is never stored here — see `Reports.gs`. Equity reports join live against a
separate sheet you point at, at report time, and nothing from it is written back anywhere.

## Updating an existing deployment

Whenever this project's files change (a bug fix, or a new feature like Analytics below), the same
routine applies:

1. In the Apps Script editor, replace each changed file's contents with the new version from this
   folder (paste over the old contents — don't just add alongside it).
2. If a file is new (doesn't exist in your project yet), add it: **+ → Script** for `.gs` files or
   **+ → HTML** for `.html` files, name it exactly as shown (no extension — the editor adds that),
   then paste in the contents.
3. Save (Ctrl+S / Cmd+S).
4. **Deploy → Manage deployments → edit (pencil icon) → New version → Deploy.** Saving alone never
   updates the live web app — it always needs a new deployment version.
5. If the update added new sheets or columns (like the one that added Locations/Periods), run
   **`runInitialSetup`** once more from the function dropdown — it's safe to re-run any time, it
   only fills in what's missing and never touches existing data.

Nothing about your data spreadsheet, roles, or existing referrals is ever affected by an update —
only the app's code changes.

## What's in this folder

| File | Purpose |
|---|---|
| `appsscript.json` | Web app manifest (access rules, permissions) |
| `Sheets.gs` | Generic read/write helpers + the schema (sheet names & headers) |
| `Setup.gs` | Run once to create all the sheets and register yourself as admin |
| `Referrals.gs` | Create / list / assign / close referrals, role-filtered |
| `Notifications.gs` | Email on submit, assign, and close |
| `Reports.gs` | Standard counts + the report-time demographic join |
| `Code.gs` | Web app entry point (`doGet`) and the only functions the browser can call |
| `App.html` | The whole app — dashboard, submit form, reports — as one single-page app that switches views with JavaScript |
| `Styles.html` | Shared CSS |

## Deploying it (about 15 minutes, no coding required)

**1. Create the project.**
- Go to [script.google.com](https://script.google.com), click **New project**.
- Rename it (top left) to something like "Behavior Tracker."

**2. Add the files.**
- You'll see one file, `Code.gs`, already there. Open it and replace its contents with this
  project's `Code.gs`.
- For each of the other `.gs` files (`Sheets.gs`, `Setup.gs`, `Referrals.gs`, `Notifications.gs`,
  `Reports.gs`): click the **+** next to "Files" → **Script**, name it exactly as shown (without
  the `.gs`, the editor adds that automatically), and paste in that file's contents.
- For each `.html` file (`App.html`, `Styles.html`): click **+** → **HTML**, name it exactly as
  shown, and paste in the contents.
- Click the gear icon (**Project Settings**) → check **"Show appsscript.json manifest file in
  editor"** → a new `appsscript.json` file appears → replace its contents with this project's
  `appsscript.json`.
- Save everything (Ctrl+S / Cmd+S, or the save icon).

**3. Run setup once.**
- In the toolbar dropdown that lists functions, select **`runInitialSetup`**, then click **Run**.
- The first time, Google will ask you to authorize the script — click through **Review
  permissions → [your account] → Advanced → Go to (project name) → Allow**. This is normal for
  any script that reads/writes your own Sheets and sends email.
- Check **View → Logs** (or Ctrl+Enter) — it'll say "Setup complete" and give you a direct link
  to the spreadsheet it created to hold your data (named "Behavior Tracker Data" in your Drive).
  Click that link.

**4. Fill in real data.**
- In the spreadsheet from the link above, add rows to **Buildings** (one per school), **Staff**
  (everyone who'll use the app, with their
  district Google email, role, and building), and **Students** (roster: student_id, name,
  building, grade — no demographic columns, on purpose).
- **Locations** and **Periods** come pre-seeded with a reasonable K-6 default list (Cafeteria, Bus,
  Hallway… / Period 1, Lunch, Recess, Transition…). Edit, add, or remove rows in either sheet any
  time to match your building — no code change or redeployment needed, it's just data the submit
  form and Analytics tab both read live.
- **Important:** do not share this spreadsheet with teachers/staff. The whole point of the
  role-based security is that only the web app enforces who sees what — if people can open the
  Sheet directly, they can see everything. Keep the Sheet itself restricted to you (and any
  co-admins), and only ever share the web app URL from step 5.

**5. Deploy as a web app.**
- Back in the Apps Script editor: **Deploy → New deployment**.
- Click the gear next to "Select type" → **Web app**.
- Description: anything. **Execute as: Me**. **Who has access: Anyone within [your district
  domain]** (this restricts it to district Google accounts — nobody outside your organization can
  reach it).
- Click **Deploy**, then **Authorize access** again if prompted.
- Copy the web app URL it gives you — that's the link you share with staff.

**6. Test it.**
- Open the URL yourself first (you're already registered as district_admin from step 3).
- Add a second Staff row for a test teacher account if you have one, and confirm they only see
  what a teacher should see.

## Updating it later

Whenever you want to change something, edit the file(s) in the Apps Script editor, save, then
**Deploy → Manage deployments → edit (pencil icon) → New version → Deploy**. Just saving isn't
enough to update the live web app — it needs a new deployment version.

## The Analytics tab

Building admins and district admins get an **Analytics** button on the dashboard. It's a
filterable set of charts — by location, period/activity, time of day, day of week, grade, and
referral type (plus building, for a district admin) — built entirely from this project's own data.
Pick any combination of filters and click **Update charts**; "Reset filters" clears them back to
"all."

**Where the location/period/time fields come from:** every new referral now asks the reporting
staff member where it happened (from your Locations sheet), what period or activity it was during
(from your Periods sheet), and, optionally, the time of day. Referrals submitted before this
update won't have those fields — they'll show up in charts as "(unspecified)," which is normal and
not a bug.

**The demographic join, in practice:** a district admin can also check "Include demographics" in
Analytics. Get the Sheet ID of your demographics export (the long string in its URL between `/d/`
and `/edit`), make sure the account you deployed as (step 5, "Execute as: Me") has at least view
access to it, paste it in, and click "Load fields" to pick which column to break down by (gender,
ethnicity, economically-disadvantaged, ENL level, IEP status — whatever columns that sheet has).
It reads that sheet live, matches rows to your Referrals data by `student_id`, shows aggregated
counts alongside the other charts, and — same as always — doesn't save anything from it back into
this project. This is restricted to district admins only.

## Known limits (so nothing here surprises you)

- No live SIS integration — student rosters are entered/updated by hand in the Students sheet.
- `Session.getActiveUser()` (used to identify who's logged in) only works reliably for accounts
  inside the same Google Workspace domain as the deploying account — which is the normal case
  for a district tool, but worth knowing if you ever try to add someone with a personal Gmail.
- This hasn't been through a formal security review. Treat it the same as any other homegrown
  tool before rolling it out district-wide — see the data privacy notes from earlier.

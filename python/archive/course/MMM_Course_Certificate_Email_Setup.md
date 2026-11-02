# MMM Mastery Course: certificate email setup (maxmaserati.com)

Live in the site repo (MaxMaseratii/mmmpro-journal, commit d7210bf):
- Course: www.maxmaserati.com/journal/?course=1 → /journal/course/
- Proof page: www.maxmaserati.com/certificate/?id=MMM-XXXX-XXXX
- Email switch: /assets/mmm-config.js → `window.MMM_CERT_MAIL_URL = '...'`

Why no Firebase extension: Firebase Extensions shut down on 31 March 2027. The email now goes through a free Google Apps Script web app. You don't need the Blaze plan, Cloud Functions or the command line.

## How it works
1. The student types a name and presses "Email it to me". They must be logged in with their MMM account.
2. The course saves `certificates/MMM-XXXX-XXXX` in Firestore. This is the public proof record. It never holds the email.
3. The course sends the certificate picture and the student's log-in token to the Apps Script.
4. The Apps Script then:
   - checks the log-in with Google;
   - checks the certificate belongs to that student;
   - sends 1 email per student per day, only to that student's own account address.

## Step A: Firestore rules (Firebase console → Firestore → Rules → Publish)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    match /{path=**}/accounts/{accountId} {
      allow read: if request.auth != null;
    }
    match /{path=**}/entries/{entryId} {
      allow read: if request.auth != null;
    }

    match /leaderboard/{uid} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == uid;
    }

    // Course certificates: public proof record, created only by the logged-in student, never edited
    match /certificates/{certId} {
      allow get: if true;
      allow list: if false;
      allow create: if request.auth != null
        && certId.matches('MMM-[A-Z0-9]{4}-[A-Z0-9]{4}')
        && request.resource.data.uid == request.auth.uid
        && request.resource.data.keys().hasOnly(['uid','name','lang','issued','phases','createdAt','v'])
        && request.resource.data.name is string
        && request.resource.data.name.size() > 0
        && request.resource.data.name.size() <= 60
        && request.resource.data.phases is list
        && request.resource.data.phases.size() <= 20;
      allow update, delete: if false;
    }
  }
}
```

## Step B: the Apps Script mailer
1. Log in to the Google account that should send the emails. Go to script.google.com and click **New project**. Name it "MMM Certificate Mailer".
2. Delete what is in Code.gs. Paste in all of `MMM_Certificate_Mailer.gs` and save.
3. In the function menu at the top, pick **authorizeOnce**, then click **Run**. Allow the permissions it asks for (send email as you, connect to external services). It sends nothing.
4. Click **Deploy → New deployment**. Click the gear and pick **Web app**. Set Execute as: **Me** and Who has access: **Anyone**. Click **Deploy**. Copy the **Web app URL** (it ends in `/exec`).
5. Check it works: open the URL in your browser. It should show `{"ok":true,"service":"MMM certificate mailer"}`.
6. On GitHub, edit `assets/mmm-config.js` in the mmmpro-journal repo and paste the URL between the quotes. Or send the URL to Claude to do it.

Limits:
- A free Gmail account can send about 100 emails a day. A Google Workspace account can send about 1,500.
- After you edit the script, use **Deploy → Manage deployments → Edit → New version**, so the URL stays the same.

## Where to see completions
Firestore → `certificates`: one record per certificate (name, date, language).

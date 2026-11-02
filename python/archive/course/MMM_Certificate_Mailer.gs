/**
 * MMM Mastery Course — certificate emails (Google Apps Script web app)
 *
 * What it does, step by step:
 *  1. Checks the student's MMM log-in with Google (Firebase Auth). No log-in = no email.
 *  2. Reads the certificate from Firestore and checks it belongs to that student.
 *  3. Sends ONE email per student per day, ONLY to the address of their own account,
 *     with the certificate picture inside the email and attached as a PNG.
 *
 * Setup: paste this whole file in script.google.com > New project > Deploy > New deployment
 *        > Web app > Execute as: Me > Who has access: Anyone > Deploy. Copy the web app URL.
 * Emails go out from the Google account that deploys this script.
 */

var CFG = {
  FIREBASE_API_KEY: 'AIzaSyDcrEEhcY6kHLQxZ7RQ37KmAcCDPgol0gg', // public web key (same as the website)
  PROJECT_ID: 'mmm-pro-journal',
  SITE: 'https://www.maxmaserati.com',
  SENDER_NAME: 'MMM Trading',
  MAX_PNG_BYTES: 1500000
};

var TXT = {
  en: {
    subject: 'Your MMM Mastery Course certificate',
    hi: 'Congratulations {n}!',
    body: 'You finished the MMM Mastery Course: The Order Flow Bible. Your certificate is attached to this email.',
    proof: 'Anyone can check it is real here:',
    sign: 'Keep reading the flow. Max Maserati',
    alt: 'Certificate of Completion'
  },
  fr: {
    subject: 'Votre certificat du Cours MMM Maîtrise',
    hi: 'Félicitations {n} !',
    body: "Vous avez terminé le Cours MMM Maîtrise : La Bible du Flux d'Ordres. Votre certificat est joint à cet email.",
    proof: "Tout le monde peut vérifier qu'il est vrai ici :",
    sign: 'Continuez à lire le flux. Max Maserati',
    alt: 'Certificat de Fin de Cours'
  }
};

function doPost(e) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(15000)) return out_({ ok: false, code: 'busy' });
  try {
    var req = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    // 1) who is asking? Google checks the log-in token for us.
    var user = lookupUser_(String(req.idToken || ''));
    if (!user || !user.email) return out_({ ok: false, code: 'auth' });

    // 2) the certificate must exist and belong to this student
    var certId = String(req.certId || '');
    if (!/^MMM-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(certId)) return out_({ ok: false, code: 'cert' });
    var cert = getCert_(certId);
    if (!cert || cert.uid !== user.uid) return out_({ ok: false, code: 'cert' });

    // 3) one email per student per day
    var props = PropertiesService.getScriptProperties();
    var today = Utilities.formatDate(new Date(), 'Etc/UTC', 'yyyyMMdd');
    var key = 'u_' + user.uid;
    if (props.getProperty(key) === today) return out_({ ok: false, code: 'already' });
    if (MailApp.getRemainingDailyQuota() < 1) return out_({ ok: false, code: 'quota' });

    // 4) the certificate picture (must really be a PNG)
    var b64 = String(req.png || '');
    if (!b64 || b64.length > CFG.MAX_PNG_BYTES * 1.4 || !/^[A-Za-z0-9+\/=]+$/.test(b64)) return out_({ ok: false, code: 'image' });
    var bytes = Utilities.base64Decode(b64);
    if (bytes.length < 8 || bytes[0] !== -119 || bytes[1] !== 80 || bytes[2] !== 78 || bytes[3] !== 71) return out_({ ok: false, code: 'image' });

    var L = TXT[cert.lang === 'fr' ? 'fr' : 'en'];
    var name = cert.name || 'MMM Trader';
    var url = CFG.SITE + '/certificate/?id=' + encodeURIComponent(certId);
    var inline = Utilities.newBlob(bytes, 'image/png', 'certificate.png');
    var file = Utilities.newBlob(bytes, 'image/png', 'MMM-Mastery-Certificate-' + certId + '.png');

    MailApp.sendEmail({
      to: user.email,
      subject: L.subject,
      name: CFG.SENDER_NAME,
      body: L.hi.replace('{n}', name) + '\n\n' + L.body + '\n\n' + L.proof + ' ' + url + '\n\n' + L.sign,
      htmlBody: html_(L, name, url),
      inlineImages: { mmmcert: inline },
      attachments: [file]
    });
    props.setProperty(key, today);
    return out_({ ok: true });
  } catch (err) {
    console.error(err);
    return out_({ ok: false, code: 'error' });
  } finally {
    lock.releaseLock();
  }
}

// Opening the URL in a browser shows this, so you can check the script is live.
function doGet() {
  return out_({ ok: true, service: 'MMM certificate mailer' });
}

function lookupUser_(idToken) {
  if (!idToken) return null;
  var res = UrlFetchApp.fetch('https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + CFG.FIREBASE_API_KEY, {
    method: 'post', contentType: 'application/json', payload: JSON.stringify({ idToken: idToken }), muteHttpExceptions: true
  });
  if (res.getResponseCode() !== 200) return null;
  var u = (JSON.parse(res.getContentText()).users || [])[0];
  if (!u || u.disabled) return null;
  return { uid: u.localId, email: u.email || '' };
}

function getCert_(id) {
  var res = UrlFetchApp.fetch('https://firestore.googleapis.com/v1/projects/' + CFG.PROJECT_ID +
    '/databases/(default)/documents/certificates/' + encodeURIComponent(id) + '?key=' + CFG.FIREBASE_API_KEY, { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) return null;
  var f = JSON.parse(res.getContentText()).fields || {};
  var s = function (k) { return f[k] && f[k].stringValue ? f[k].stringValue : ''; };
  return { uid: s('uid'), name: s('name'), lang: s('lang'), issued: s('issued') };
}

function esc_(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

function html_(L, name, url) {
  var gold = '#D6B15E';
  return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>' +
    '<body style="margin:0;background:#0E1114;font-family:Arial,Helvetica,sans-serif;color:#ECE5D3">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0E1114"><tr><td align="center" style="padding:28px 12px">' +
    '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#151A1F;border:1px solid #27303A;border-radius:14px">' +
    '<tr><td style="padding:28px 28px 8px;text-align:center;color:' + gold + ';font-size:12px;letter-spacing:3px;font-weight:bold">MAX MASERATI MODEL</td></tr>' +
    '<tr><td style="padding:4px 28px;text-align:center;font-size:26px;font-weight:bold;color:#ECE5D3">' + esc_(L.hi.replace('{n}', name)) + '</td></tr>' +
    '<tr><td style="padding:10px 28px 18px;text-align:center;font-size:15px;line-height:1.6;color:#A9AFB5">' + esc_(L.body) + '</td></tr>' +
    '<tr><td style="padding:0 20px"><img src="cid:mmmcert" width="560" alt="' + esc_(L.alt) + '" style="display:block;width:100%;max-width:560px;height:auto;border-radius:8px;border:1px solid #27303A"></td></tr>' +
    '<tr><td style="padding:20px 28px 6px;text-align:center;font-size:14px;color:#A9AFB5">' + esc_(L.proof) + '</td></tr>' +
    '<tr><td style="padding:0 28px 24px;text-align:center"><a href="' + esc_(url) + '" style="color:' + gold + ';font-size:14px;word-break:break-all">' + esc_(url) + '</a></td></tr>' +
    '<tr><td style="padding:16px 28px 26px;text-align:center;font-size:13px;color:#7A838D;border-top:1px solid #27303A">' + esc_(L.sign) +
    ' &middot; <a href="' + CFG.SITE + '" style="color:#7A838D">maxmaserati.com</a></td></tr>' +
    '</table></td></tr></table></body></html>';
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/** Run this once from the editor (select "authorizeOnce" > Run) to give the script permission
 *  to send email and fetch URLs before you deploy. It sends nothing. */
function authorizeOnce() {
  Logger.log('Emails left today: ' + MailApp.getRemainingDailyQuota());
  UrlFetchApp.fetch('https://www.google.com', { muteHttpExceptions: true });
}

# Firebase Integration Setup (MANDATORY)

⚠️ **Firebase is now MANDATORY for SPAMURAI to function.** The application will not start without proper Firebase credentials configured.

This guide will help you set up Firebase Firestore logging for SPAMURAI message events.

## Why Firebase?

Firebase Firestore provides:
- ✅ **Cloud-based logging** - Access logs from anywhere
- ✅ **Queryable data** - Filter by date, recipient, tags, status
- ✅ **Real-time monitoring** - See events as they happen
- ✅ **Scalable** - Free tier includes 50K reads, 20K writes per day
- ✅ **Export capabilities** - Download data anytime

## Setup Steps

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **Add Project** (or use existing project)
3. Enter project name (e.g., "SPAMURAI Logs")
4. Disable Google Analytics (optional for logging)
5. Click **Create Project**

### 2. Enable Firestore Database

1. In Firebase Console, click **Firestore Database** in left sidebar
2. Click **Create Database**
3. Choose **Production mode** (recommended)
4. Select your **Cloud Firestore location** (choose closest region)
5. Click **Enable**

### 3. Create Service Account

1. In Firebase Console, click the ⚙️ gear icon → **Project Settings**
2. Go to **Service Accounts** tab
3. Click **Generate New Private Key**
4. Click **Generate Key** - this downloads a JSON file
5. **Important**: Keep this file secure! It provides admin access to your Firebase project

### 4. Configure SPAMURAI

**Recommended: Environment Variable Method** ✅

Use the automated setup script (works for all installations on this machine):

**macOS/Linux:**
```bash
./setup_firebase.sh ~/Downloads/your-project-xxxxx.json
```

**Windows:**
```cmd
setup_firebase.bat C:\Users\YourName\Downloads\your-project-xxxxx.json
```

The script will:
- Validate your credentials file
- Add `FIREBASE_CREDENTIALS` environment variable to your shell config
- Test the connection
- Provide next steps

**Manual Environment Variable Setup:**

If you prefer manual setup:

```bash
# macOS/Linux - Add to ~/.zshrc or ~/.bashrc
export FIREBASE_CREDENTIALS='{"type":"service_account","project_id":"...paste full JSON here..."}'

# Windows - Run in Command Prompt (Admin)
setx FIREBASE_CREDENTIALS "{\"type\":\"service_account\",\"project_id\":\"...\"}"
```

**Alternative: File-Based Method** (Not recommended for multiple installations)

1. Move the downloaded JSON file to your SPAMURAI config directory:
   ```bash
   mv ~/Downloads/your-project-xxxxx.json config/firebase-credentials.json
   ```

2. Update your `config.json`:
   ```json
   {
     "firebase_config": {
       "enabled": true,
       "credentials_path": "config/firebase-credentials.json",
       "collection_name": "message_events"
     }
   }
   ```

3. Make sure to add credentials file to `.gitignore`:
   ```bash
   echo "config/firebase-credentials.json" >> .gitignore
   ```

**Enable Firebase:**

Regardless of method, enable Firebase in your `config.json`:
```json
{
  "firebase_config": {
    "enabled": true,
    "collection_name": "message_events"
  }
}
```

Note: With environment variables, you don't need `credentials_path` in config!

### 5. Set Firestore Security Rules (Optional but Recommended)

1. In Firebase Console → **Firestore Database** → **Rules**
2. Update rules to restrict access:
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /message_events/{document=**} {
         allow read, write: if false;  // Only service account can write
       }
     }
   }
   ```
3. Click **Publish**

## Event Schema

Events are logged with this structure:

```json
{
  "event_type": "message_sent",
  "timestamp": "2025-11-17T10:30:00.123Z",
  "recipient": {
    "name": "John Doe",
    "phone": "+1234567890"
  },
  "message": {
    "variant_info": "First 1/5",
    "content_hash": "abc123...",
    "type": "text"
  },
  "tags": {
    "campaign_name": "Holiday Promo",
    "segment": "premium",
    "batch_id": "001"
  },
  "session_id": "uuid-xxx"
}
```

## Custom Tags

You can add custom tags to categorize and filter your messages. Common tags:

- `campaign_name`: Name of your campaign
- `segment`: User segment (premium, trial, etc.)
- `batch_id`: Batch identifier
- `source`: Where contacts came from
- `region`: Geographic region
- `environment`: production, staging, test

Tags are passed when calling the tracker methods (see code examples below).

## Querying Your Data

### Firebase Console
1. Go to **Firestore Database** → **Data**
2. Click on `message_events` collection
3. View all events, filter, and export

### Using Firebase CLI
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Export data
firebase firestore:export gs://your-bucket/exports
```

## Cost Estimation

Firebase Firestore free tier:
- **50,000 reads/day** - Free
- **20,000 writes/day** - Free
- **1 GB storage** - Free

For 20,000 messages/day, you'll stay within free tier limits.

## Sharing Credentials Across Multiple Installations

**The Environment Variable Advantage:**

With environment variables, all installations log to the **same Firebase project**:

1. **Download credentials once** from Firebase Console (one JSON file)
2. **Share securely** with your team:
   - Via password manager (1Password, LastPass)
   - Encrypted email/chat
   - Secure file sharing service
3. **Each machine runs setup script** once:
   ```bash
   ./setup_firebase.sh /path/to/shared-credentials.json
   ```
4. **All installations on that machine** automatically use the same credentials

**Benefits:**
- ✅ Centralized logging - all messages in one Firebase project
- ✅ No file management - credentials stored in environment
- ✅ Not in git history - secure by default
- ✅ Easy to update - re-run setup script with new credentials
- ✅ Works across different SPAMURAI installations on same machine

**Security Best Practices:**
- Share credentials via encrypted channels only
- Use different Firebase projects for production vs testing
- Rotate credentials periodically (generate new key, re-run setup)
- Never commit credentials to git

## Troubleshooting

### Firebase initialization failed
**Using environment variable:**
- Verify variable is set: `echo $FIREBASE_CREDENTIALS` (macOS/Linux) or `echo %FIREBASE_CREDENTIALS%` (Windows)
- Check JSON is valid: `python3 -c "import json,os; json.loads(os.getenv('FIREBASE_CREDENTIALS'))"`
- Restart terminal after setup
- Re-run setup script if needed

**Using credentials file:**
- Check that `credentials_path` points to correct JSON file
- Verify JSON file is valid service account key
- Check file permissions

### Events not appearing
- Confirm `enabled: true` in config
- Check console for error messages
- Verify Firestore is enabled in Firebase Console
- Run `python3 test_firebase.py` to test connection

### "Permission denied" errors
- Check Firestore security rules
- Verify service account has proper permissions
- Ensure credentials haven't been revoked in Firebase Console

### Environment variable not working
- Make sure you restarted terminal after running setup script
- Check shell config file has the export line:
  ```bash
  cat ~/.zshrc | grep FIREBASE_CREDENTIALS
  ```
- Try manual setup if script failed

## Disabling Firebase

To disable Firebase logging (keeps local logging):

```json
{
  "firebase_config": {
    "enabled": false
  }
}
```

## Need Help?

- [Firebase Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Support](https://firebase.google.com/support)

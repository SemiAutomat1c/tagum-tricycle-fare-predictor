# Deployment Instructions for Firebase

This project is now configured for Firebase Hosting (frontend) and Cloud Functions (backend).

## Prerequisites
1.  **Firebase CLI**: Ensure you have the Firebase CLI installed.
    ```bash
    npm install -g firebase-tools
    ```
2.  **Login**: Log in to your Firebase account.
    ```bash
    firebase login
    ```
3.  **Blaze Plan**: Your Firebase project **MUST** be on the Blaze (pay-as-you-go) plan to use Python Cloud Functions.

## Deployment Steps

1.  **Set your Project ID**:
    Edit `.firebaserc` and replace `tagum-tricycle-fare-predictor` with your actual Firebase project ID.
    ```json
    {
      "projects": {
        "default": "your-project-id-here"
      }
    }
    ```
    Alternatively, run:
    ```bash
    firebase use --add
    ```

2.  **Deploy**:
    Run the following command to deploy both hosting and functions:
    ```bash
    firebase deploy
    ```

## Troubleshooting

-   **Billing Error**: If you see an error about billing, please upgrade your project to the Blaze plan in the Firebase Console.
-   **Missing Permissions**: Ensure you have the necessary permissions (Editor or Owner) on the Firebase project.
-   **Python Version**: Cloud Functions for Firebase supports Python 3.10+. The deployment will automatically handle the runtime.

## Local Testing (Optional)
To test locally, you can use the Firebase Emulator Suite (requires setup):
```bash
firebase emulators:start
```
*Note: Python Cloud Functions emulation might require additional setup.*

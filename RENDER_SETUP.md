# Deploying to Render - Setup Instructions

To ensure your application runs correctly on Render and can access your encrypted data, you must configure the environment variables correctly.

## 1. Set the Encryption Key

The application uses an `ENCRYPTION_KEY` to decrypt your Excel files. Since the `.env` file is not uploaded to GitHub (and shouldn't be for security), you need to manually add it to Render.

### Steps:
1. Log in to your **Render Dashboard**.
2. Select your Web Service (e.g., `flaks-app-87av`).
3. Go to the **Environment** tab on the left sidebar.
4. Click **Add Environment Variable**.
5. Set the **Key** as: `ENCRYPTION_KEY`
6. Set the **Value** as: `6quESesfWmdFwmCDOWSBa-EHkBiuNYNLqbP3apAv-Y8=`
   *(Note: This matches your local key to ensure it can decrypt the files you've already pushed)*.
7. Click **Save Changes**.

## 2. Automatic Redeploy

Once you save the changes, Render will automatically redeploy your application. After the deployment is finished, the dashboard should be able to decrypt and display the Excel data.

## 3. Persistent Data Note
Render's disk is ephemeral by default. Any changes you make to the Excel file via the website will be lost when the service restarts unless you use a persistent disk. For basic usage and viewing, the above steps are sufficient.

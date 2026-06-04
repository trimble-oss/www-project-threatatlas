## Trimble IDAS SSO integration (SSO only)

Quick checklist to configure Trimble IDAS as an OIDC provider for ThreatAtlas (SSO only).

1. Register a confidential client in Trimble IDAS
   - Redirect URI: `https://<your-backend>/api/auth/oidc/idas/callback`
   - Grant types: `authorization_code` (no PKCE required for confidential clients)
   - Scopes: `openid email profile`
   - Note the `client_id` and `client_secret`.

2. Create the provider in ThreatAtlas (admin)
   - Option A: Admin UI — Sign in as an admin and create a new provider with these fields:
     - `name`: `idas` (lowercase, URL-safe slug)
     - `display_name`: e.g. `Trimble IDAS`
     - `issuer`: the IDAS issuer URL (e.g. `https://id.trimble.com`)
     - `metadata_url` (optional): a discovery URL if the issuer is not reachable from the backend host
     - `client_id` and `client_secret`
     - `scopes`: `openid email profile`

   - Option B: HTTP API (admin token required). Example `curl` to create provider:

```bash
curl -X POST "https://<your-backend>/api/sso/providers" \
  -H "Authorization: Bearer <ADMIN_JWT>" \
  -H "Content-Type: application/json" \
  -d @threatatlas-app/docs/idas-provider-example.json
```

3. Test a login from the frontend
   - Open the frontend login page. The provider should appear.
   - Click the `Trimble IDAS` button → you'll be redirected to IDAS, authenticate, then returned to the app.
   - The app will receive an internal ThreatAtlas JWT and sign you in.

Notes and troubleshooting
 - If the backend cannot reach the IDAS discovery URL, set `metadata_url` to a value reachable from the backend.
 - ThreatAtlas expects the user `email` claim to be present in userinfo or ID token for upserting users.
 - Secrets are encrypted using the app `SECRET_KEY`; rotating that key will require re-entering provider secrets.

Advanced: seeding the provider
 - See `/threatatlas-app/backend/scripts/seed_idas_provider.py` for a script that can create the provider from environment variables.

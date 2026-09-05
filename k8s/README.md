# Secrets required by this stack (create before first deploy)

kubectl create secret generic portal-secrets \
  --from-literal=DB_PASSWORD='<from password manager>' \
  --from-literal=API_TOKEN='<from password manager>'

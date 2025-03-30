#!/bin/bash
set -e

# --- Configuration ---
NGINX_SOURCE_DIR="$(pwd)/nginx"
NGINX_DEST_DIR="/etc/nginx/conf.d"
EMAIL="thesleebit@gmail.com"

# Certificate configuration
CERTS=(
  "sleebit-main:ai.sleebit.com blog.sleebit.com converge-backend.sleebit.com"
)

# --- Deploy Nginx Configuration ---
echo "Copying Nginx configuration files..."
sudo cp ${NGINX_SOURCE_DIR}/*.conf ${NGINX_DEST_DIR}/
sudo nginx -t

# --- Process Certificates ---
for CERT in "${CERTS[@]}"; do
  IFS=":" read -r CERT_NAME DOMAINS <<< "$CERT"
  
  DOMAIN_ARGS=""
  for DOMAIN in ${DOMAINS}; do
    DOMAIN_ARGS+=" -d ${DOMAIN}"
  done

  # Issue or renew certificate
  if [ ! -d "/etc/letsencrypt/live/${CERT_NAME}" ]; then
    echo "Requesting new certificate for ${CERT_NAME}..."
    sudo certbot --nginx ${DOMAIN_ARGS} --non-interactive --agree-tos --email ${EMAIL} --cert-name ${CERT_NAME}
  else
    echo "Renewing certificate for ${CERT_NAME}..."
    sudo certbot renew --cert-name ${CERT_NAME}
  fi
done

# --- Reload Nginx ---
echo "Reloading Nginx..."
sudo systemctl reload nginx
echo "Deployment completed successfully."

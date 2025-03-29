#!/bin/bash
set -e

# --- Configuration ---

# Directory paths for Nginx configuration files
NGINX_SOURCE_DIR="$(pwd)/nginx"
NGINX_DEST_DIR="/etc/nginx/conf.d"

# Email to be used by Certbot
EMAIL="thesleebit@gmail.com"

# Certificate configurations: Each entry is "CERT_NAME:domain1 domain2 ..."
CERTS=(
  "sleebit.com:ai.sleebit.com blog.sleebit.com converge-backend.sleebit.com"
)

# --- Deploy Nginx Configuration ---

echo "Copying Nginx configuration files from ${NGINX_SOURCE_DIR} to ${NGINX_DEST_DIR}..."
sudo cp ${NGINX_SOURCE_DIR}/*.conf ${NGINX_DEST_DIR}/

echo "Testing Nginx configuration..."
sudo nginx -t

# --- Process Certificates with Certbot ---

for CERT in "${CERTS[@]}"; do
  # Split the string into certificate name and its domains
  IFS=":" read -r CERT_NAME DOMAINS <<< "$CERT"
  echo "Processing certificate for ${CERT_NAME} with domains: ${DOMAINS}"
  
  # Build domain arguments for certbot
  DOMAIN_ARGS=""
  for DOMAIN in ${DOMAINS}; do
    DOMAIN_ARGS+=" -d ${DOMAIN}"
  done
  
  # Check if the certificate for this primary domain exists
  if [ ! -d "/etc/letsencrypt/live/${CERT_NAME}" ]; then
    echo "Certificate for ${CERT_NAME} not found. Requesting a new certificate..."
    sudo certbot --nginx ${DOMAIN_ARGS} --non-interactive --agree-tos --email ${EMAIL} --cert-name ${CERT_NAME}
  else
    echo "Certificate for ${CERT_NAME} found. Renewing certificate if needed..."
    sudo certbot renew --cert-name ${CERT_NAME}
  fi
done

# --- Reload Nginx to Apply New Configurations and Certificates ---

echo "Reloading Nginx..."
sudo systemctl reload nginx

echo "Deployment completed successfully."

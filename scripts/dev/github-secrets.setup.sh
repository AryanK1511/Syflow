#!/bin/bash

SECRETS_FILE=".env.github"

REPOSITORIES=(
  "AryanK1511/Syflow"
)

for REPO in "${REPOSITORIES[@]}"; do
  echo "Updating secrets in repository: $REPO"

  while IFS= read -r LINE; do
    [[ -z "$LINE" || "$LINE" =~ ^# ]] && continue

    SECRET_NAME=$(echo $LINE | cut -d'=' -f1)
    SECRET_VALUE=$(echo $LINE | cut -d'=' -f2-)

    echo "  Setting secret: $SECRET_NAME"
    gh secret set "$SECRET_NAME" -b"$SECRET_VALUE" --repo "$REPO"
  done < "$SECRETS_FILE"
done

echo "Secrets updated successfully."

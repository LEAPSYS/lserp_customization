#!/bin/bash
# LSERP Customization App Installation Script
# Usage: ./install_lserp_app.sh <site_name>

SITE_NAME=$1

if [ -z "$SITE_NAME" ]; then
    echo "Error: Please provide your Frappe site name."
    echo "Usage: ./install_lserp_app.sh <site_name>"
    exit 1
fi

echo "Starting installation for LSERP Customization App on site: $SITE_NAME"

# 1. cd to frappe-bench (Assumes this script is run from within the bench directory, or user navigates there first)
# cd /path/to/your/frappe-bench

# 2. Get the app from the GitHub repository
echo "Fetching app from GitHub (https://github.com/LEAPSYS/lserp_customization)..."
bench get-app https://github.com/LEAPSYS/lserp_customization

# 3. Install the app on the specified site
echo "Installing LSERP Customization on $SITE_NAME..."
bench --site $SITE_NAME install-app lserp_customization

# 4. Migrate the database to register DocTypes
echo "Migrating database..."
bench --site $SITE_NAME migrate

# 5. Clear cache and build
echo "Clearing cache..."
bench clear-cache
bench clear-website-cache

# Optional: Restart bench (might require supervisorctl/systemctl depending on setup)
# echo "Restarting bench (if applicable)..."
# bench restart

echo "Installation complete! You can now configure 'LSERP Theme Settings' in Frappe."

# Exit if there's an error
set -e


########################
# Start of configuration

# Name - This is the bit after edp- - e.g. for edp-dev, PAAS_ENV_SHORTNAME would just be 'dev'
if [ -z "${PAAS_ENV_SHORTNAME+set}" ] || [ "${#PAAS_ENV_SHORTNAME}" -eq "0" ]; then
  read -p "What name do you want to give the environment (e.g. 'dev', 'staging', 'prod'):" PAAS_ENV_SHORTNAME
fi
if [ "${#PAAS_ENV_SHORTNAME}" -eq "0" ]; then
  exit 1
fi
echo "Your space will be called: edp-$PAAS_ENV_SHORTNAME"

# App memory - we normally use '256M' for testing and '1G' for production
if [ -z "${APP_MEMORY+set}" ] || [ "${#APP_MEMORY}" -eq "0" ]; then
  read -p "How much memory do you want to give each app (normally '256M' for test environments, '1G' for production):" APP_MEMORY
fi
if [ "${#APP_MEMORY}" -eq "0" ]; then
  exit 1
fi
echo "Your app's memory allocation will be: $APP_MEMORY"

# Fixed app scale settings
APP_INSTANCES=2
APP_DISK="1G"


#################
# Start of script

#-----------------
echo "# Target the EDP organisation"
cf target -o co-equality-data-platform

#-----------------
echo "# Check if the space already exists - exit if it does"
set +e
RESULT=$(cf space "edp-${PAAS_ENV_SHORTNAME}")
set -e
if [[ "$RESULT" == *"FAILED"* ]]; then
  echo "Space doesn't already exist - we can continue and create the space."
else
  echo "Space already exists. Exiting."
  exit 1
fi

#-----------------
echo "# Create the space"
cf create-space "edp-${PAAS_ENV_SHORTNAME}" -o co-equality-data-platform

echo "# - Target future commands at this space"
cf target -s "edp-${PAAS_ENV_SHORTNAME}"


#---------------------------
echo "# Add AWS S3 backing service for the 'Enterprise Taskforce data pack'"
echo "# - Create the service"
cf create-service aws-s3-bucket default "edp-${PAAS_ENV_SHORTNAME}-filestorage-enterprise-taskforce"

echo "# - Create a key to access the service"
#   Note: this is only needed to access the S3 bucket from outside of Gov.UK PaaS (e.g. from GitHub Actions)
cf create-service-key "edp-${PAAS_ENV_SHORTNAME}-filestorage-enterprise-taskforce" "edp-${PAAS_ENV_SHORTNAME}-filestorage-enterprise-taskforce-key" -c '{"allow_external_access": true}'


#-----------
echo "# Create App"
echo "# - Create the App itself"
cf create-app "equality-data-platform-${PAAS_ENV_SHORTNAME}"

echo "# - Scale to the right size"
set +e
cf scale "equality-data-platform-${PAAS_ENV_SHORTNAME}" -i ${APP_INSTANCES} -k ${APP_DISK} -m ${APP_MEMORY} -f
set -e
echo "This will say FAILED, but it has probably worked (it failed to START the app because there isn't currently an app deployed)"

echo "# - Bind app to file storage"
cf bind-service "equality-data-platform-${PAAS_ENV_SHORTNAME}" "edp-${PAAS_ENV_SHORTNAME}-filestorage-enterprise-taskforce"

echo "# - Add health check"
cf set-health-check "equality-data-platform-${PAAS_ENV_SHORTNAME}" http --endpoint "/health-check"

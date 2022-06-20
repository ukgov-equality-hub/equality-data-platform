
[Equality Data Platform](../README.md) >
[Developer documentation](README.md) >
HTTP Basic Authentication

# HTTP Basic Authentication

Our non-production environments are protected with HTTP Basic Authentication.

## Why do we use HTTP Basic Authentication?

It's important that members of the public can't access our non-productions environments, because:
* they could easily mistake a non-production environment for the live services.
* they could access the live service before it "goes live", whilst we're still making breaking changes to the service.

## How does HTTP Basic Authentication help?

If HTTP Basic Authentication is enabled, when a user tries to access the service, their browser will show a popup.  
The popup looks like this in Firefox:  
<img src="screenshot-of-http-basic-auth-firefox.png" width="400">  
The popup looks like this in Google Chrome:  
<img src="screenshot-of-http-basic-auth-chrome.png" width="400">  

## What is the password?

Ask a member of the team for the password.

## How to enable / disable HTTP Basic Authentication on an environment

* Follow the instructions on the [Hosting](Hosting.md) page to connect to the hosting environments

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the EDP organisation and the *sandbox* space:

* Target the space containing the app you want to put into HTTP Basic Authentication  
  e.g. one of:
  ```
  cf target -s "edp-dev"
  cf target -s "edp-staging"
  cf target -s "edp-production"
  ```

* HTTP Basic Authentication is set using an environment variable.  
  You can check the current status of HTTP Basic Authentication using `cf env`  
  e.g. one of:
  ```
  cf env "equality-data-platform-dev"          // Dev environment
  cf env "equality-data-platform-staging"      // Stage environment
  cf env "equality-data-platform-production"   // Prod environment
  ```
  This will print out **all** the environment variables (and there are a lot of them!)
  ```
  Getting env variables for app equality-data-platform-dev in org co-equality-data-platform / space edp-dev as james@jwgsoftware.com...
  ...
  ... about 100 lines later ...
  ...
  BASIC_AUTH_USERNAME: 'the_basic_auth_username'
  BASIC_AUTH_PASSWORD: 'the_basic_auth_password'
  ```

* Use `cf set-env` to turn HTTP Basic Authentication on or off  
  e.g. one of:
  ```
  // Dev environment - ON
  cf set-env "equality-data-platform-dev" BASIC_AUTH_USERNAME "the_basic_auth_username"
  cf set-env "equality-data-platform-dev" BASIC_AUTH_PASSWORD "the_basic_auth_password"
  
  // Stage environment - ON
  cf set-env "equality-data-platform-staging" BASIC_AUTH_USERNAME "the_basic_auth_username"
  cf set-env "equality-data-platform-staging" BASIC_AUTH_PASSWORD "the_basic_auth_password"
  
  // Prod environment - ON
  cf set-env "equality-data-platform-production" BASIC_AUTH_USERNAME "the_basic_auth_username"
  cf set-env "equality-data-platform-production" BASIC_AUTH_PASSWORD "the_basic_auth_password"
  
  // Dev environment - OFF
  cf unset-env "equality-data-platform-dev" BASIC_AUTH_USERNAME
  cf unset-env "equality-data-platform-dev" BASIC_AUTH_PASSWORD
  
  // Stage environment - OFF
  cf unset-env "equality-data-platform-staging" BASIC_AUTH_USERNAME
  cf unset-env "equality-data-platform-staging" BASIC_AUTH_PASSWORD
  
  // Prod environment - OFF
  cf unset-env "equality-data-platform-production" BASIC_AUTH_USERNAME
  cf unset-env "equality-data-platform-production" BASIC_AUTH_PASSWORD
  ```

* Restart the app  
  e.g. one of:
  ```
  // Dev environment
  cf restart "equality-data-platform-dev"
  
  // Stage environment
  cf restart "equality-data-platform-staging"
  
  // Prod environment
  cf restart "equality-data-platform-production"
  ```

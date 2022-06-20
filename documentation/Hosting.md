
[Equality Data Platform](../README.md) >
[Developer documentation](README.md) >
Hosting and live databases

# Hosting and live databases

Our code is hosted on [Gov.UK Platform as a Service (Gov.UK PaaS)](https://www.cloud.service.gov.uk/).  
See this link for the [EDP organisation on Gov.Uk PaaS](https://admin.london.cloud.service.gov.uk/organisations/17e173e9-7d92-4a06-8510-0719e1c0e51a).

## Connect to Gov.UK PaaS using the CloudFoundry CLI
You will need to connect to the hosting environments to do things like:
* make changes to the environments (e.g. change the scaling of the servers)
* to access databases

For regular deployments, you won't need to connect to Gov.UK PaaS directly.  
Instead, you should use our CI/CD server, GitHub Actions.  
See the [Deployments](Deployments.md) page for details.

Follow these instructions to connect to Gov.UK PaaS:
* First, ask a team member for access to the [EDP organisation on Gov.Uk PaaS](https://admin.london.cloud.service.gov.uk/organisations/17e173e9-7d92-4a06-8510-0719e1c0e51a).

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the EDP organisation and the *sandbox* space:  
  ```
  $ ./LoginToGovPaas.sh
  API endpoint: api.london.cloud.service.gov.uk
  Authenticating...
  OK
  Targeted org co-equality-data-platform.
  Targeted space sandbox.
  API endpoint:   https://api.london.cloud.service.gov.uk
  API version:    3.115.0
  user:           [your email address]
  org:            co-equality-data-platform
  space:          sandbox
  ```

## Change which space you are targeting within CloudFoundry
Each environment has its own *space* in CloudFoundry.  
We use `cf target` to change space  
e.g.:

```
cf target -s "edp-dev"
cf target -s "edp-staging"
cf target -s "edp-production"
```

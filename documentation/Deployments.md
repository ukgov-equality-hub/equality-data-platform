
[Equality Data Platform](../README.md) >
[Developer documentation](README.md) >
Deployments

# Deployments

We use [GitHub Actions](https://docs.github.com/en/actions) for our deployments.  
Here are the [GitHub Actions pipelines for the EDP service](https://github.com/cabinetoffice/equality-data-platform/actions).

## When are deployments run?
* Pushing to the `main` **branch** deploys to the `dev` environment  
  You can see the [dev deployments here](https://github.com/cabinetoffice/equality-data-platform/actions/workflows/deploy-dev.yml)

* Pushing a **tag** named `staging-*` deploys to the `staging` environment  
  You can see the [staging deployments here](https://github.com/cabinetoffice/equality-data-platform/actions/workflows/deploy-staging.yml)

* Pushing a **tag** named `v*` deploys to the `production` environment  
  You can see the [production deployments here](https://github.com/cabinetoffice/equality-data-platform/actions/workflows/deploy-production.yml)


## How to deploy to Gov.UK PaaS manually
Normally, it shouldn't be necessary to deploy to PaaS manually.

But, there might be cases where you want to test something quickly in the PaaS dev environment.  
To deploy to PaaS dev, follow these instructions:

* Follow the instructions on the [Hosting](Hosting.md) page to connect to the hosting environments

* Open a Bash terminal in the `hosting` folder

* Run `./LoginToGovPaas.sh`  
  This should log you in to Gov.UK PaaS. You will be targeting the EDP organisation and the *sandbox* space:

* Change to the `equality-data-website` folder:  
  `cd ../equality-data-website`

* Run this command  
  ```shell
  cf target -s edp-dev
  cf push equality-data-platform-dev --manifest manifest.yml --strategy rolling
  ```

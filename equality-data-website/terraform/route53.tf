
data "aws_route53_zone" "route_53_zone_for_our_domain" {
  name         = "equality-data.service.cabinetoffice.gov.uk."
}

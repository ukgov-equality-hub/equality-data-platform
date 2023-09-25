
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "main_app_iam_role_eb" {
  name               = "${var.service_name_hyphens}--${var.environment_hyphens}--EB-Role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_instance_profile" "main_app_iam_instance_profile_eb" {
  name = "${var.service_name_hyphens}--${var.environment_hyphens}--EB-InstanceProfile"
  role = aws_iam_role.main_app_iam_role_eb.name
}

data "aws_iam_policy_document" "enterprise_taskforce_s3_iam_policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = [
      aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.arn,             // The bucket itself (to enable listing of files)
      "${aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.arn}/*",      // The files within the bucket (to create / update / delete files)
      aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.arn,        // The bucket itself (to enable listing of files)
      "${aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.arn}/*"  // The files within the bucket (to create / update / delete files)
    ]
  }
}

resource "aws_iam_policy" "enterprise_taskforce_s3_iam_policy" {
  name        = "${var.service_name_hyphens}--${var.environment_hyphens}--EB-Enterprise-Taskforce-Policy"
  description = "Policy to allow Elastic Beanstalk instances to read S3 data from Enterprise Taskforce buckets"
  policy      = data.aws_iam_policy_document.enterprise_taskforce_s3_iam_policy_document.json
}

resource "aws_iam_role_policy_attachment" "attach_enterprise_taskforce_s3_iam_policy_attachment" {
  role       = aws_iam_role.main_app_iam_role_eb.name
  policy_arn = aws_iam_policy.enterprise_taskforce_s3_iam_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_AWSElasticBeanstalkWebTier" {
  role       = aws_iam_role.main_app_iam_role_eb.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
}

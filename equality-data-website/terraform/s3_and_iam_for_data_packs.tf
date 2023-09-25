
// An S3 bucket to store the "Enterprise Taskforce Data Pack"
resource "aws_s3_bucket" "enterprise_taskforce_data_pack_s3_bucket" {
  bucket_prefix = lower("${var.service_name_hyphens}--${var.environment_hyphens}--ET-Data-Pack")
}

resource "aws_s3_bucket_public_access_block" "enterprise_taskforce_data_pack_s3_bucket_public_access_block" {
  bucket = aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_user" "enterprise_taskforce_data_pack_iam_user" {
  name = "${var.service_name_hyphens}--${var.environment_hyphens}--ET-Data-Pack--User"
}

data "aws_iam_policy_document" "enterprise_taskforce_data_pack_s3_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_iam_user.enterprise_taskforce_data_pack_iam_user.arn]
    }
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = [
      aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.arn,        // The bucket itself (to enable listing of files)
      "${aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.arn}/*"  // The files within the bucket (to create / update / delete files)
    ]
  }
}

resource "aws_s3_bucket_policy" "enterprise_taskforce_data_pack_s3_bucket_policy" {
  bucket = aws_s3_bucket.enterprise_taskforce_data_pack_s3_bucket.id
  policy = data.aws_iam_policy_document.enterprise_taskforce_data_pack_s3_policy.json
}


// An S3 bucket to store the "Enterprise Taskforce No10 dashboard"
resource "aws_s3_bucket" "enterprise_taskforce_no10_dashboard_s3_bucket" {
  bucket_prefix = lower("${var.service_name_hyphens}--${var.environment_hyphens}--ET-No10-dashboard")
}

resource "aws_s3_bucket_public_access_block" "enterprise_taskforce_no10_dashboard_s3_bucket_public_access_block" {
  bucket = aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_user" "enterprise_taskforce_no10_dashboard_iam_user" {
  name = "${var.service_name_hyphens}--${var.environment_hyphens}--ET-No10-Dashboard--User"
}

data "aws_iam_policy_document" "enterprise_taskforce_no10_dashboard_s3_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_iam_user.enterprise_taskforce_no10_dashboard_iam_user.arn]
    }
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = [
      aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.arn,        // The bucket itself (to enable listing of files)
      "${aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.arn}/*"  // The files within the bucket (to create / update / delete files)
    ]
  }
}

resource "aws_s3_bucket_policy" "enterprise_taskforce_no10_dashboard_s3_bucket_policy" {
  bucket = aws_s3_bucket.enterprise_taskforce_no10_dashboard_s3_bucket.id
  policy = data.aws_iam_policy_document.enterprise_taskforce_no10_dashboard_s3_policy.json
}

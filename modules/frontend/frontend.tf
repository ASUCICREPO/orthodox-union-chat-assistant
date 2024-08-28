# S3 Bucket for Frontend
resource "aws_s3_bucket" "orthodox_union_chatbot_frontend_bucket_production" {
  bucket = "orthodox-union-chatbot-frontend-store-bucket-v1-production"
  force_destroy = true
}

# Upload the frontend store zip file to S3
resource "aws_s3_object" "orthodox_union_chatbot_frontend_upload_production" {
  bucket = aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id
  key    = "frontend_store_bucket.zip"
  source = "${path.root}/S3/deploy_zips/frontend_store_bucket.zip"
  etag   = filemd5("${path.root}/S3/deploy_zips/frontend_store_bucket.zip")

  depends_on = [aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production]

  content_type = "text/html"
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "orthodox_union_chatbot_frontend_public_access_block_production" {
  bucket = aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

##########

resource "aws_cloudfront_distribution" "orthodox_union_chatbot_frontend_distribution_production" {
  origin {
    domain_name = aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.orthodox_union_chatbot_oai_production.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Orthodox Union Chatbot Frontend Distribution"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id}"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # Add this to trigger updates when the S3 object changes
  depends_on = [aws_s3_object.orthodox_union_chatbot_frontend_upload_production]
}

resource "aws_cloudfront_origin_access_identity" "orthodox_union_chatbot_oai_production" {
  comment = "Origin Access Identity for Orthodox Union Chatbot S3 bucket"
}

# Update the S3 bucket policy to allow CloudFront access
resource "aws_s3_bucket_policy" "orthodox_union_chatbot_frontend_policy_production" {
  bucket = aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontAccess"
        Effect    = "Allow"
        Principal = {
          AWS = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ${aws_cloudfront_origin_access_identity.orthodox_union_chatbot_oai_production.id}"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.arn}/*"
      }
    ]
  })
}

# IAM Role for Lambda
resource "aws_iam_role" "orthodox_union_chatbot_lambda_exec_role_production" {
  name = "orthodox-union-chatbot-lambda-exec-role-production"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda to access S3
resource "aws_iam_role_policy" "orthodox_union_chatbot_lambda_s3_access_production" {
  name = "orthodox-union-chatbot-lambda-s3-access-production"
  role = aws_iam_role.orthodox_union_chatbot_lambda_exec_role_production.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.arn,
          "${aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.arn}/*"
        ]
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "orthodox_union_chatbot_inject_wss_production" {
  filename         = "${path.root}/lambdas/zips/inject_wss.zip"
  function_name    = "orthodox-union-chatbot-inject-wss-production"
  role             = aws_iam_role.orthodox_union_chatbot_lambda_exec_role_production.arn
  handler          = "inject_wss.lambda_handler"
  runtime          = "python3.12"
  timeout          = 60  # Set the maximum runtime to 60 seconds

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.orthodox_union_chatbot_frontend_bucket_production.id
      API_URL     = var.websocket_api_endpoint
    }
  }
}

# CloudWatch Logs policy for Lambda
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_lambda_logs_production" {
  role       = aws_iam_role.orthodox_union_chatbot_lambda_exec_role_production.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudformation_stack" "orthodox_union_chatbot_custom_resource_production" {
  name = "orthodox-union-chatbot-custom-resource-stack-production"
  
  template_body = jsonencode({
    AWSTemplateFormatVersion = "2010-09-09"
    Description = "Custom Resource for Orthodox Union Chatbot Lambda Invocation"
    
    Resources = {
      CustomResource = {
        Type = "Custom::LambdaResource"
        Properties = {
          ServiceToken = aws_lambda_function.orthodox_union_chatbot_inject_wss_production.arn
          ServiceTimeout = 60
        }
      }
    }
  })

  depends_on = [
    aws_lambda_function.orthodox_union_chatbot_inject_wss_production, 
    aws_s3_object.orthodox_union_chatbot_frontend_upload_production,
    aws_iam_role_policy.orthodox_union_chatbot_lambda_s3_access_production
  ]
}
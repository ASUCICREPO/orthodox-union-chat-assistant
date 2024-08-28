#This section defines the IAM policies and roles for the lambda functions
####################################################################################################

#Defines the basic execution policy for lambda functions
resource "aws_iam_policy" "orthodox_union_chatbot_lambda_basic_execution_production" {
  name        = "orthodox_union_chatbot_lambda_basic_execution_policy_production"
  description = "Orthodox Union Chatbot Lambda basic execution policy"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
  })
}

#Defines the bedrock access policy for lambda functions
resource "aws_iam_policy" "orthodox_union_chatbot_lambda_bedrock_access_production" {
  name        = "orthodox_union_chatbot_lambda_bedrock_access_policy_production"
  description = "Orthodox Union Chatbot Lambda bedrock access policy"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAll",
            "Effect": "Allow",
            "Action": [
                "bedrock:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DescribeKey",
            "Effect": "Allow",
            "Action": [
                "kms:DescribeKey"
            ],
            "Resource": "arn:*:kms:*:::*"
        },
        {
            "Sid": "APIsWithAllResourceAccess",
            "Effect": "Allow",
            "Action": [
                "iam:ListRoles",
                "ec2:DescribeVpcs",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PassRoleToBedrock",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::*:role/*AmazonBedrock*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": [
                        "bedrock.amazonaws.com"
                    ]
                }
            }
        }
    ]
  })
}

#Defines the S3 access policy for lambda functions
resource "aws_iam_policy" "orthodox_union_chatbot_lambda_S3_access_production" {
  name        = "orthodox_union_chatbot_lambda_S3_access_policy_production"
  description = "Orthodox Union Chatbot lambda S3 access policy"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "s3-object-lambda:*"
            ],
            "Resource": "*"
        }
    ]
  })
}

#Defines the Api gateway access policy for lambda functions
resource "aws_iam_policy" "orthodox_union_chatbot_lambda_api_gateway_access_production" {
  name        = "orthodox_union_chatbot_lambda_api_gateway_access_policy_production"
  description = "Orthodox Union Chatbot lambda api gateway access policy"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "execute-api:Invoke",
                "execute-api:ManageConnections"
            ],
            "Resource": "arn:aws:execute-api:*:*:*"
        }
    ]
  })
}

#Defines the lambda function execution access policy for lambda functions
resource "aws_iam_policy" "orthodox_union_chatbot_lambda_function_execution_access_production" {
  name        = "orthodox_union_chatbot_lambda_function_execution_access_policy_production"
  description = "Orthodox Union Chatbot lambda function execution access policy"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "lambda:InvokeFunction",
            "Resource": [
                aws_lambda_function.orthodox_union_chatbot_bedrock_orchestration_production.arn,
                "${aws_lambda_function.orthodox_union_chatbot_bedrock_orchestration_production.arn}:*"
            ],
            "Effect": "Allow"
        }
    ]
  })
}

#Defines the IAM roles, and attaches their policies, for the lambda functions
####################################################################################################

#Defines the IAM role for the bedrock orchestration lambda function
resource "aws_iam_role" "orthodox_union_chatbot_bedrock_orchestration_role_production" {
  name = "orthodox_union_chatbot_bedrock_orchestration_role_production"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}
# Attach the basic execution policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_bedrock_orchestration_basic_execution_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_bedrock_orchestration_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_basic_execution_production.arn
}
# Attach the bedrock access policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_bedrock_orchestration_bedrock_access_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_bedrock_orchestration_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_bedrock_access_production.arn
}
# Attach the S3 access policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_bedrock_orchestration_S3_access_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_bedrock_orchestration_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_S3_access_production.arn
}
# Attach the API gateway access policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_bedrock_orchestration_api_gateway_access_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_bedrock_orchestration_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_api_gateway_access_production.arn
}

#Defines the IAM role for the websocket opener lambda function
resource "aws_iam_role" "orthodox_union_chatbot_websocket_opener_role_production" {
  name = "orthodox_union_chatbot_websocket_opener_role_production"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}
# Attach the basic execution policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_websocket_opener_basic_execution_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_websocket_opener_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_basic_execution_production.arn
}
# Attach the lambda function access policy to the role
resource "aws_iam_role_policy_attachment" "orthodox_union_chatbot_websocket_opener_lambda_function_execution_access_policy_attachment_production" {
  role       = aws_iam_role.orthodox_union_chatbot_websocket_opener_role_production.name
  policy_arn = aws_iam_policy.orthodox_union_chatbot_lambda_function_execution_access_production.arn
}

#This section defines the lambda functions
####################################################################################################

#Defines the bedrock orchestration lambda function
resource "aws_lambda_function" "orthodox_union_chatbot_bedrock_orchestration_production" {
  function_name = "orthodox_union_chatbot_bedrock_orchestration_production"
  role = aws_iam_role.orthodox_union_chatbot_bedrock_orchestration_role_production.arn

  handler = "chatbot_main.lambda_handler"
  filename = "${path.module}/../../lambdas/zips/orchestration.zip"

  runtime = "python3.12"
  timeout = 60

  environment {
    variables = {
      KNOWLEDGE_BASE_ID = var.knowledge_base_id
      WEBSOCKET_URL = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.api_endpoint
      TEMPERATURE = var.TEMPERATURE
      ORCHESTRATION_MODEL_ID = var.ORCHESTRATION_MODEL_ID
      CLASSIFICATION_MODEL_ID = var.CLASSIFICATION_MODEL_ID
      NUM_KB_RESULTS = var.NUM_KB_RESULTS
      SOURCE_EXTRACTION_BOT_ID = var.SOURCE_EXTRACTION_BOT_ID
    }
  }

}

#Defines the websocket Opener lambda function
resource "aws_lambda_function" "orthodox_union_chatbot_websocket_opener_production" {
  function_name = "orthodox_union_chatbot_websocket_opener_production"
  role = aws_iam_role.orthodox_union_chatbot_websocket_opener_role_production.arn

  handler = "websocket_opener.lambda_handler"
  filename = "${path.module}/../../lambdas/zips/websocket_opener.zip"

  runtime = "python3.12"

  environment {
    variables = {
      BEDROCK_ORCHESTRATION_ARN = aws_lambda_function.orthodox_union_chatbot_bedrock_orchestration_production.arn
    }
  }

}

#This section defines the websocket API gateway
####################################################################################################

#Defines the websocket API gateway
resource "aws_apigatewayv2_api" "orthodox_union_chatbot_websocket_api_gateway_production" {
  name                       = "orthodox_union_chatbot_websocket_api_gateway_production"
  protocol_type              = "WEBSOCKET"
  route_selection_expression = "$request.body.action"

}

#Defines the websocket API gateway integration with the websocket opener lambda function
resource "aws_apigatewayv2_integration" "orthodox_union_chatbot_websocket_integration_production" {
  api_id           = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.orthodox_union_chatbot_websocket_opener_production.invoke_arn

}

#Defines the default route for the websocket API gateway
resource "aws_apigatewayv2_route" "orthodox_union_chatbot_default_route_production" {
  api_id    = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.id
  route_key = "sendMessage"
  target    = "integrations/${aws_apigatewayv2_integration.orthodox_union_chatbot_websocket_integration_production.id}"
  
}

#Defines the default route response for the websocket API gateway
resource "aws_apigatewayv2_route_response" "orthodox_union_chatbot_default_route_response_production" {
  api_id             = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.id
  route_id           = aws_apigatewayv2_route.orthodox_union_chatbot_default_route_production.id
  route_response_key = "$default"
}

#Defines the websocket api stage
resource "aws_apigatewayv2_stage" "orthodox_union_chatbot_websocket_api_gateway_stage_production" {
  api_id = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.id
  name   = "prod"
  auto_deploy = true
  
}

# Grant API Gateway permission to invoke the Lambda function
resource "aws_lambda_permission" "orthodox_union_chatbot_api_gateway_permission_production" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.orthodox_union_chatbot_websocket_opener_production.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.execution_arn}/*/*"
}
output "websocket_api_endpoint" {
  description = "The endpoint URL of the WebSocket API for productionuction"
  value = aws_apigatewayv2_api.orthodox_union_chatbot_websocket_api_gateway_production.api_endpoint
}
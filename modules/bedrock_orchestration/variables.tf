variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
}

variable "knowledge_base_id" {
  description = "The ID of the knowledge base to be used by the orchestration lambda function."
  type        = string
  
}

variable "TEMPERATURE" {
  description = "The temperature parameter to be used by the orchestration lambda function."
  type        = string
  
}

variable "ORCHESTRATION_MODEL_ID" {
  description = "The ID of the orchestration model to be used by the orchestration lambda function."
  type        = string
  
}   

variable "CLASSIFICATION_MODEL_ID" {
  description = "The ID of the classification model to be used by the orchestration lambda function."
  type        = string
  
}

variable "NUM_KB_RESULTS" {
  description = "The number of knowledge base results to be used by the orchestration lambda function."
  type        = string
  
}

variable "SOURCE_EXTRACTION_BOT_ID" {
  description = "The ID of the source extraction bot to be used by the orchestration lambda function."
  type        = string
  
}


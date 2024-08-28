# Orthodox Union App Terraform

This repository contains the Terraform code for deploying the Orthodox Union App infrastructure.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [How It Works](#how-it-works)


## Introduction
The Orthodox Union App Terraform repository provides the necessary infrastructure code to deploy the Orthodox Union App. It includes the configuration for provisioning and managing the required resources on various cloud providers.

## Prerequisites
Before getting started, ensure that you have the following prerequisites:
- Terraform installed on your local machine https://www.terraform.io/
- Valid credentials for AWS https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html

## Getting Started
To get started with the Orthodox Union App Terraform, follow these steps:
1. Clone this repository to your local machine.
2. Set up your AWS credentials.
3. Customize the Terraform variables in the `variables.tf` file according to your requirements. (Crucial to update the knowledge base ID for your sources)
4. Run `terraform init` to initialize the Terraform configuration.
5. Run `terraform plan` to preview the changes that will be applied.
6. Run `terraform apply` to provision the infrastructure.

## Usage
Once the infrastructure is provisioned, you can use the Orthodox Union App by following these steps:
1. Access the deployed application using the provided URL. (Found in the tfstate file by searching cloudfront.net)
2. Ask your questions away!

## How It Works
The chatbot has two components, the api, and the current demo frontend.
If you want to set it up without creating the frontend, but just the api to be used seperately, you can get rid of the module called "frontend" as well as in main.tf

The api currently accepts the following syntax:
{
    "action": "sendMessage", #The main route
    "prompt": "Any question" #This is the most recent user prompt
    "history": [{
        "sentBy": sentBy,
        "state": state,
        "message": message
    },
    {...}
    ]
}

You send the route to take, only ever "sendMessage" for this app, as well as the most recent user message as the prompt, plus the an array of the history for the chat.

The sentBy can be "USER" or "BOT" depending on who's message it is.
The "state" can be "FINISHED" which is for bot messages that have finished being recieved, other states aren't currently used
The message is the actual text of the previous message.

The api sends back:
data = {
    'statusCode': 200,
    'type': block_type,
    'text': message_text,
}

The type can be several things, "start", "delta", "end", "blank". 
"start" means the first peice of text, "delta" means a middle part of text. "end" means the last part of the text. Lastly "blank" is a filler with no text.
The message_text is the contents of the current text chunk


NOTE: If you want to update the react code, youll need to add the node_modules, as well as material UI components

NOTE2: If you want to update any of the lambdas, you'll need to re-zip the code manually after any edits
Pay special attention to the ochestration folder, zip up the contents, but also add in the python packages: certifi, chardet, idna, and requests


                


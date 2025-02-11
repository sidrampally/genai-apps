# Bedrock Agents – Plasma Donation Assistant  

## Overview  
The **Plasma Donation Assistant** is an AI-powered virtual assistant built with **Amazon Bedrock Agents** to help users with plasma donation inquiries. It leverages **Amazon Kendra** for knowledge retrieval, **AWS Lambda** for processing, and **Amazon DynamoDB** for managing donor registration data.

## Architecture  
![Bedrock Agents – Plasma Donation Site Assistant](./unnamed.png)  

The system consists of:  
- **Bedrock Agents**: Handles user queries and provides responses using LLM-based retrieval.  
- **Amazon Kendra**: Searches through plasma donation FAQs to provide relevant answers.  
- **Amazon S3**: Stores FAQ documents for indexing by Amazon Kendra.  
- **AWS Lambda**: Processes donor registrations and updates **Amazon DynamoDB**.  
- **Amazon DynamoDB**: Stores structured donor registration data.  

## What is Amazon Bedrock Agents?  
[Amazon Bedrock](https://aws.amazon.com/bedrock/) allows developers to build and deploy **generative AI applications** using foundation models (FMs). **Bedrock Agents** extend this by enabling **multi-step, goal-oriented interactions**, making them ideal for customer support, automation, and knowledge retrieval applications.

## Features  
- **Conversational AI**: Answers plasma donation questions using Amazon Kendra.  
- **Donor Registration Assistance**: Guides users through the donation sign-up process.  
- **Context-Aware Responses**: Uses a knowledge base to provide accurate and up-to-date information.  

## Setup Instructions  
### **Prerequisites**  
Ensure you have:  
- An **AWS Account** with access to Amazon Bedrock, Kendra, Lambda, and DynamoDB.  
- **AWS CLI** configured with necessary permissions.  
- **Python 3.x** installed.  

### **Installation**  
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/plasma-donation-agent.git
   cd plasma-donation-agent

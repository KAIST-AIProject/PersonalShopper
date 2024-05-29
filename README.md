# Personal Shopper AI

## Overview
Personal Shopper AI is a service designed to assist customers in shopping by recommending and explaining various products. The AI scrapes product information, extracts keywords, and recommends personalized products based on the user's preferences and needs. 

## Features

### 1. Product Input and Keyword Extraction
- **User Input**: Users provide a description of the product they are looking for.
- **Keyword Extraction**: The AI extracts relevant keywords and attributes from the user's input to form a search query.

### 2. Web Scraping
- **Scraping Process**: The system scrapes multiple shopping sites (Naver, Coupang, G-Market, Kurly) to gather product data, including prices, reviews, and detailed descriptions.
- **Image Processing**: Uses OCR tools (e.g., Naver Clova OCR, Google Vision API) to extract text from product images when necessary.

### 3. Product Recommendation
- **Personalized Recommendations**: The AI provides tailored product suggestions based on the user's specific requirements (e.g., a professional cyclist vs. a parent looking for a child's bike).
- **Rating Agent**: Evaluates products based on several criteria such as price, review positivity, and specific product features.
- **Sorting and Comparison**: Sorts products by their overall score and provides the best option to the user.

### 4. Decision Making and Purchase Assistance
- **Reasoning Agent**: Explains the rationale behind each product's rating, helping users make informed decisions.
- **Feedback Agent**: Validates the rating process and ensures that the recommendations are reasonable and trustworthy.

## Technical Details

### 1. Pipeline
The project is divided into several key components:
- **Keyword Agent**: Extracts and categorizes keywords from user input.
- **Web Scraper**: Gathers product information from various shopping websites.
- **Decision Agent**: Compares and ranks products based on extracted data.
- **Rating Agent**: Assesses products using predefined criteria.
- **Feedback Agent**: Reviews the rating process to ensure accuracy.

### 2. Fine-Tuning GPT
- **Training Data**: Custom datasets are used to fine-tune GPT models for specific tasks, ensuring accurate keyword extraction and product recommendations.
- **Experimentation**: Continuous testing and refining of the models to improve performance and reliability.

### 3. Further Plans
- **Login and Purchase Automation**: Automate the login and purchase process on various shopping sites using Python scripts and Selenium.
- **Speed Optimization**: Implement parallel processing to improve the efficiency of scraping and data processing tasks.
- **Enhanced User Preferences**: Incorporate user-specific weighting for different product attributes to provide even more personalized recommendations.


## Contributors
- **Kim Dongwoo**
- **Lee Chaewon**
- **Lim Saebom**

## Conclusion
Personal Shopper AI aims to revolutionize the online shopping experience by providing a smart, personalized, and efficient shopping assistant. The project leverages advanced AI techniques and continuous refinement to meet the dynamic needs of users.

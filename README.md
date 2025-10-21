# Simplified ML Pipeline to demo robust input/output data handling

Simple ML pipeline with focus on handling input/output data with strict and convenient validation.


This approach secures production-level data handling in ML pipeline which easy to read and maintain. 


## How to run ML Pipeline?

### Run ml_pipeline.py script
> python ml_pipeline.py

### Expected output:
> 

#### TEST CASE 1

SUCCESS

Input: {'age': 35, 'name': 'jane smith', 'income': 75000.0, 'country': 'usa'}

Output: {'prediction': 0.3, 'confidence': 0.94, 'risk_level': 'low', 'processed_at': '2024-01-01'}
>

#### TEST CASE 2

SUCCESS

Input: {'age': 22, 'name': 'john doe', 'income': 0, 'country': 'unknown'}

Output: {'prediction': 0.8, 'confidence': 0.84, 'risk_level': 'high', 'processed_at': '2024-01-01'}
>

#### TEST CASE 3

SUCCESS

Input: {'age': 67, 'name': 'alice wonder', 'income': 120000.0, 'country': 'unknown'}

Output: {'prediction': 0.48, 'confidence': 0.9, 'risk_level': 'low', 'processed_at': '2024-01-01'}
>

#### TEST CASE 4

FAILED: 

1 validation error for DataModel

extra_field

  Extra inputs are not permitted [type=extra_forbidden, input_value='this is allowed', input_type=str]
    
Process finished with exit code 0


> Good luck ;-)

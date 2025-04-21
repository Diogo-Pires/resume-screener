# IT Resume Screener
An **ongoing** AI-powered API that matches, ranks, and extracts information from IT resumes.​

## Overview
IT Resume Screener is a Python-based API designed to streamline the recruitment process by leveraging artificial intelligence. It analyzes resumes to extract pertinent information, matches them against job descriptions, and ranks candidates based on relevance.​

## Features
 - Resume Parsing: Extracts key details such as skills, experience, and education from resumes.

 - Candidate Matching: Compares extracted resume data with job descriptions to assess suitability.

 - Ranking System: Assigns scores to candidates based on relevance to the job requirements.

 - Model Training: Includes scripts and data for training custom models to improve matching accuracy.​

## Technologies Used
 - Python

 - Natural Language Processing (NLP)

 - Machine Learning

 - FastAPI (for API development)

 - Scikit-learn, Pandas, NumPy​

## Project Structure
 - app/: Contains the FastAPI application code.

 - data/: Holds sample resumes and job descriptions for testing and training.

 - model-training/: Includes scripts and datasets for training and evaluating machine learning models.

 - README.md: Project documentation.​

## Getting Started
### Prerequisites
 - Python 3.7 or higher

 - pip (Python package installer)​

### Installation
Clone the repository:​
```bash
git clone https://github.com/Diogo-Pires/resume-screener.git
```
Navigate to the project directory:​
```bash
cd resume-screener
```
Create and activate a virtual environment (optional but recommended):​
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### Install the required dependencies:​
```bash
pip install -r requirements.txt
```
## Running the Application
Start the FastAPI server:​
```bash
uvicorn app.main:app --reload
```
## Access the API documentation at:​

http://127.0.0.1:8000/docs

## API Endpoints
 - POST /upload-resume/: Upload a resume for parsing and analysis.

 - POST /match-job/: Submit a job description to match against uploaded resumes.

 - GET /ranked-candidates/: Retrieve a list of candidates ranked by relevance.​

## Generate Dataset
 - Navigate to the data/utils directory.
 - Generate dataset
```bash
python generate_dataset.py
```
  - Run other utils scripts if need
```bash
python common_word_removal.py
python find_and_remove_token_from_others_dataset.py
```
  - Create config file
```bash
python -m spacy init config config.cfg --lang en --pipeline ner
```

  - Convert your JSON training data to .spacy format. Navigate to the model-training/ directory.
```bash
python json_to_binary.py
 ```

  - Debug the dataset in the spacy format 
```bash
python -m spacy debug data config.cfg --paths.train train.spacy --paths.dev train.spacy
```

## Model Training
To train custom models:​

  - Navigate to the model-training/ directory.

  - Use the provided scripts to preprocess data and train models.
```bash
python training_extraction.py
```
  - Save the trained models in the appropriate directory for the API to utilize.​
  - Test the model
```bash
python test_extraction.py
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.​

## License
This project is licensed under the MIT License. See the LICENSE file for details.

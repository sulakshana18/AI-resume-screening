# AI Resume Screening & Job Matching System

An AI-powered web application that analyzes PDF resumes, extracts technical skills, and recommends relevant job opportunities by comparing candidate profiles with job requirements. Built using Python, Natural Language Processing (NLP), TF-IDF similarity, and Streamlit.

## Overview

Finding suitable job opportunities can be challenging when candidates need to compare their qualifications against multiple job descriptions. This project automates part of that process by analyzing resume content, identifying relevant skills, and ranking available jobs according to a matching score.

The application provides an interactive interface where users can upload a resume, analyze extracted information, explore recommended jobs, and identify skills that may need improvement.

## Key Features

- **Resume Parsing:** Upload PDF resumes and extract readable text.
- **Text Preprocessing:** Clean and normalize resume text before analysis.
- **Skill Extraction:** Identify technical skills mentioned in the resume.
- **Job Matching:** Compare resume content with job descriptions using TF-IDF-based text similarity and skill coverage.
- **Job Ranking:** Sort job opportunities by their calculated match scores.
- **Skill Gap Analysis:** Display matched skills and missing skills for individual job requirements.
- **AI-Powered Insights:** Generate additional resume analysis using the OpenAI API when configured.
- **Interactive Interface:** Explore resume analysis and job recommendations through Streamlit.
- **Custom Job Datasets:** Upload a CSV file containing job listings.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Pandas | Dataset loading and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF vectorization and cosine similarity |
| pypdf | PDF text extraction |
| OpenAI API | Optional AI-generated insights |
| python-dotenv | Environment variable configuration |
| Git and GitHub | Version control and source code hosting |

## How It Works

1. **Upload a resume:** The user uploads a PDF resume through the application.
2. **Extract text:** The system extracts readable text from the PDF.
3. **Preprocess text:** The extracted content is cleaned and normalized.
4. **Extract skills:** The application identifies technical skills from the resume.
5. **Analyze job listings:** Job descriptions and required skills are loaded from a CSV dataset.
6. **Calculate match scores:** The system combines text similarity and required-skill coverage.
7. **Rank job opportunities:** Jobs are sorted by their final match score.
8. **Review skill gaps:** Users can inspect matched skills, missing skills, and optional AI-generated insights.

## Matching Methodology

The application calculates a heuristic match score using two components:

- **Text similarity:** Measures the similarity between the resume text and job-related text using TF-IDF-based cosine similarity.
- **Skill coverage:** Measures how many of a job's required skills are identified in the resume.

The current scoring formula is:

`Match Score = (0.60 × Text Similarity) + (0.40 × Skill Coverage)`

Both components are represented on a 0–1 scale before calculating the final percentage.

**Important:** The match score is a ranking aid, not a calibrated probability of getting hired. A higher score indicates greater textual and skill overlap under the implemented scoring method; it does not guarantee suitability or selection.

## Project Structure

```text
AI-Resume-Screening-Job-Matching/
│
├── app.py
├── extract_resumes.py
├── requirements.txt
├── README.md
│
├── data/
│   └── raw/
│       ├── job_recommendation_dataset.csv
│       └── resumes/
│           └── Resume.csv
│
└── src/
    ├── __init__.py
    ├── job_loader.py
    ├── job_processing.py
    ├── llm_analysis.py
    ├── matching.py
    ├── pdf_extractor.py
    ├── processing.py
    ├── similarity.py
    └── skill_extraction.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- Git
- A web browser

### 1. Clone the repository

```bash
git clone https://github.com/sulakshana18/AI-resume-screening-_-Job-Matching.git
```

### 2. Navigate to the project directory

```bash
cd AI-resume-screening-_-Job-Matching
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

### 6. Open the application

Visit the following address in your browser:

http://localhost:8501

Keep the terminal running while using the application.

## Dataset Information

The project uses resume and job-related CSV data for processing and testing.

### Job dataset

The application supports a CSV file with fields such as:

- `job_title`
- `company`
- `location`
- `experience_level`
- `salary`
- `industry`
- `required_skills`

The application can also normalize certain alternative column names. Optional fields may use default values when absent.

To use another job dataset, upload a compatible CSV file through the application's sidebar.

### Resume dataset

The repository includes a resume dataset at `data/raw/resumes/Resume.csv`. The application itself accepts PDF resumes for interactive analysis.

**Dataset note:** Check the original dataset license and privacy requirements before redistributing resume data. Do not upload personal or confidential information without authorization.

## Optional OpenAI Integration

The application can generate additional AI-based insights when an OpenAI API key is configured.

1. Create a `.env` file in the project root.
2. Add the following configuration:

```text
OPENAI_API_KEY=your_api_key_here
```

3. Save the file and restart the application.

Keep `.env` out of Git and never publish your API key. The core resume screening and job-matching functionality is designed to work without the OpenAI integration.

## Limitations

- PDF text extraction depends on the document containing readable text. Image-only or scanned resumes may require OCR.
- Skill extraction depends on the skills recognized by the implemented extraction logic.
- Match scores depend on the dataset, text preprocessing, and scoring method.
- AI-generated insights may be incomplete or incorrect and should be reviewed.
- Matching scores should support, not replace, human judgment in recruitment decisions.

## Future Enhancements

- Add OCR support for scanned resumes.
- Expand the technical skills dictionary.
- Introduce evaluation metrics using a labeled test dataset.
- Add resume and job analytics dashboards.
- Support exporting matching reports.
- Deploy the application to a cloud hosting platform.

## Learning Outcomes

This project demonstrates practical experience with:

- Python application development
- Data preprocessing and analysis
- Natural Language Processing fundamentals
- TF-IDF and cosine similarity
- Resume parsing and skill extraction
- Similarity-based recommendation systems
- Streamlit application development
- Git and GitHub workflows

## Author

**Sulakshana Manchikanti**

AI & Machine Learning | Python | NLP | Data Processing

[GitHub Profile](https://github.com/sulakshana18)

---

*This project is intended for educational and portfolio purposes. Matching results are indicative and should not be used as the sole basis for hiring decisions.*

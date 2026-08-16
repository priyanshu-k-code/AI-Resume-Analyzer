import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables from the .env file
load_dotenv()


# Function to generate the AI resume analysis report
def get_report(resume, job_desc):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. Please add it to your .env file."
        )

    client = Groq(api_key=api_key)

    # Prompt used to evaluate the resume against the job description
    prompt = f"""
# Context

You are an AI Resume Analyzer. You will be given a candidate's resume
and the job description of the role they are applying for.

# Instructions

Analyze the candidate's resume against the important requirements
mentioned in the job description.

Consider relevant points such as:

- Technical skills
- Programming languages
- Frameworks and tools
- Projects
- Work experience
- Education
- Certifications
- Relevant soft skills
- Other important job requirements

For every important point:

- Give a score out of 5.
- Start the point with one of these indicators:
  ✅ Good Match
  ❌ Missing
  ⚠️ Partial Match
- Clearly explain the reason for the score.

At the end, create the heading:

## Suggestions to improve your resume:

Give practical suggestions that can improve the candidate's chances
of being shortlisted for this role.

Keep the evaluation clear, relevant and reasonably concise.

# Candidate Resume

{resume}

---

# Job Description

{job_desc}

# Output Format

Each evaluation point must include a score such as 3/5.
Mention the score and relevant indicator at the beginning of each point.
"""

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return chat_completion.choices[0].message.content

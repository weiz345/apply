import openai

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = 'YOUR_API_KEY'

def generate_cold_email(resume_text, job_posting_text):
    # Adapted to use Chat API with gpt-3.5-turbo or gpt-4-turbo
    messages = [
        {
            "role": "system",
            "content": "You are an experienced career advisor and expert in crafting professional emails."
        },
        {
            "role": "user",
            "content": f"Based on the following resume and job posting, please draft a concise and persuasive cold email to the hiring manager, expressing interest in the position and highlighting the relevant skills and experiences.\n\nResume:\n{resume_text}\n\nJob Posting:\n{job_posting_text}\n\nCold Email:"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # or 'gpt-3.5-turbo' if you prefer
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    email = response['choices'][0]['message']['content'].strip()
    return email

if __name__ == "__main__":
    # Read resume and job posting from files
    with open('resume/resume_1.txt', 'r', encoding='utf-8') as f:
        resume_text = f.read()

    with open('posting/posting_1.txt', 'r', encoding='utf-8') as f:
        job_posting_text = f.read()

    # Generate the cold email
    email = generate_cold_email(resume_text, job_posting_text)

    print("Generated Cold Email:\n")
    print(email)

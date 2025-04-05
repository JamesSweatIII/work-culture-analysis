from google import genai

client = genai.Client(api_key="AIzaSyCCtX80L6uJofel7qiK9rSJk4CxWrc2wbs")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(f"\n{response.text}")
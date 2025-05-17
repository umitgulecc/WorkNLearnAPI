# app/ai/gpt.py

def generate_questions(prompt: str) -> list[dict]:
    # GPT’den beklenen örnek yapı
    return [
        {
            "question": "What is the correct way to greet in a business email?",
            "options": [
                {"text": "Hey!", "is_correct": False},
                {"text": "To whom it may concern,", "is_correct": True},
                {"text": "Sup?", "is_correct": False},
                {"text": "Hi buddy,", "is_correct": False},
            ],
            "explanation": "In business emails, formal greetings are preferred.",
            "topic_id": 1
        },
        # Daha fazla ekleyebilirsin
    ]

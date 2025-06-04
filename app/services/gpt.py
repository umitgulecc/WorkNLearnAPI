# GPT yerine sabit data kullanarak sorular oluşturur.(GPT Maliyetli olduğu için)
def generate_questions_with_gpt(topics=None):
    return [
        {
            "content": "What is the purpose of a resume in job applications?",
            "topic_id": 1,
            "options": [
                {"text": "To apply for a driving license", "is_correct": False},
                {"text": "To summarize a candidate's qualifications and experience", "is_correct": True},
                {"text": "To register for health insurance", "is_correct": False},
                {"text": "To provide medical history", "is_correct": False}
            ]
        },
        {
            "content": "Which of the following is an example of professional email etiquette?",
            "topic_id": 1,
            "options": [
                {"text": "Using slang and emojis", "is_correct": False},
                {"text": "Writing in all caps", "is_correct": False},
                {"text": "Keeping the message clear and concise", "is_correct": True},
                {"text": "Ignoring the subject line", "is_correct": False}
            ]
        },
        {
            "content": "What does 'punctuality' mean in a workplace context?",
            "topic_id": 1,
            "options": [
                {"text": "Arriving late regularly", "is_correct": False},
                {"text": "Completing tasks without deadlines", "is_correct": False},
                {"text": "Being on time for work and meetings", "is_correct": True},
                {"text": "Leaving early from meetings", "is_correct": False}
            ]
        },
        {
            "content": "Which of the following is a benefit of teamwork?",
            "topic_id": 1,
            "options": [
                {"text": "Isolation of ideas", "is_correct": False},
                {"text": "Increased conflict", "is_correct": False},
                {"text": "Enhanced problem-solving through collaboration", "is_correct": True},
                {"text": "Less communication", "is_correct": False}
            ]
        },
        {
            "content": "Why is feedback important in the workplace?",
            "topic_id": 1,
            "options": [
                {"text": "It lowers morale", "is_correct": False},
                {"text": "It prevents any change", "is_correct": False},
                {"text": "It helps improve performance and growth", "is_correct": True},
                {"text": "It discourages learning", "is_correct": False}
            ]
        }
    ]

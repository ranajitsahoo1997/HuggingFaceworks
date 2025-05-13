import re
# import json

def rawTextToDictionary(raw_text):
    print("Entered function...")
    raw_text = f"""{raw_text}"""
    # Updated regex patterns
    topic_pattern = re.compile(r'\*\*Topic: (.*?)\*\*')
    question_pattern = re.compile(
        r'(\d+)\.\s+(.*?)\n((?:[A-D]\)\s+.*?\n)+)\s*Answer:\s+([A-D])\)\s+(.*?)\n',
        re.DOTALL
    )

    # Split the content by topics
    topics = topic_pattern.split(raw_text)[1:]  # [topic1, content1, topic2, content2, ...]

    structured_data = {}

    for i in range(0, len(topics), 2):
        topic = topics[i].strip()
        content = topics[i + 1]

        questions = []
        print(f"\n--- Processing Topic: {topic} ---\n")

        for match in question_pattern.finditer(content):
            q_num, question_text, options_block, answer_key, answer_text = match.groups()

            # Extract options from the options block
            options = dict(re.findall(r'([A-D])\)\s+(.*)', options_block))

            questions.append({
                "question": question_text.strip(),
                "options": options,
                "answer": {
                    "option": answer_key.strip(),
                    "text": answer_text.strip()
                }
            })

        structured_data[topic] = questions

    return structured_data


# # Example usage:
# if __name__ == "__main__":
#     # Paste your long string into this variable
#     raw_text = """<your long string here>"""  # <-- Replace this

#     result = rawTextToDictionary(raw_text)
#     print(json.dumps(result, indent=2))

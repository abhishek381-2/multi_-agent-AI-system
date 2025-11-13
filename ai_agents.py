import ollama
import json

# --- Model Configuration ---
OFFLINE_MODEL = 'llama3:8b'
# ---------------------------

def get_ai_response(prompt_text, format_type='json'):
    """Helper function to get response from Ollama."""
    try:
        # --- YEH RAHA FIX ---
        # Arguments ko dynamically build karein
        chat_args = {
            "model": OFFLINE_MODEL,
            "messages": [{'role': 'user', 'content': prompt_text}]
        }
        
        # 'format' parameter sirf tabhi add karein jab 'json' ho
        if format_type == 'json':
            chat_args['format'] = 'json'
        
        # Model ko call karein
        response = ollama.chat(**chat_args) 
        # --- FIX KHATM ---

        return response['message']['content']
        
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        # Return an empty structure matching the expected format
        if format_type == 'json':
            return "[]" 
        return "Error: Could not connect to Ollama server. Please ensure Ollama is running."

def parse_and_validate_json(json_string, expected_keys=['question', 'answer']):
    """
    Parses the JSON string and validates its structure.
    Handles lists of dicts, single dicts, or dicts nested under a key.
    """
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        print(f"JSONDecodeError for: {json_string}")
        return [] # Not valid JSON

    # Case 1: Data is a list (ideal case)
    if isinstance(data, list):
        # Filter out any non-dict items
        valid_items = [item for item in data if isinstance(item, dict) and all(key in item for key in expected_keys)]
        return valid_items

    # Case 2: Data is a single dictionary
    if isinstance(data, dict):
        # Check if it's a single flashcard/quiz
        if all(key in data for key in expected_keys):
            return [data] # Wrap it in a list
        
        # Check if it's nested (e.g., {"questions": [...]})
        # Find the first key that holds a list
        for key in data:
            if isinstance(data[key], list):
                nested_list = data[key]
                valid_items = [item for item in nested_list if isinstance(item, dict) and all(key in item for key in expected_keys)]
                return valid_items
    
    # If no valid structure is found
    print(f"Warning: AI returned unexpected JSON structure: {json_string}")
    return []

def generate_flashcards(text_chunk):
    """
    Generates Q/A flashcards from the given text using Ollama.
    """
    prompt = f"""
    You are an expert flashcard generator.
    From the text below, create exactly 5 essential question-answer pairs.
    Return the output *only* as a valid JSON array.
    Example Format: [ {{"question": "What is 2+2?", "answer": "4"}}, ... ]

    Text:
    {text_chunk}
    """
    
    json_response = get_ai_response(prompt, format_type='json')
    return parse_and_validate_json(json_response, expected_keys=['question', 'answer'])

def generate_quizzes(text_chunk):
    """
    Generates MCQs from the given text using Ollama.
    """
    prompt = f"""
    You are an expert quiz generator.
    From the text below, create exactly 5 multiple-choice questions (MCQs).
    Each question must have 4 options and one correct answer.
    The answer must *exactly match* one of the options.
    Return the output *only* as a valid JSON array.
    
    ---
    EXAMPLE FORMAT:
    [
      {{
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "Paris"
      }},
      {{
        "question": "What is 2+2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
      }}
    ]
    ---
    
    Text to use:
    {text_chunk}
    """
    
    json_response = get_ai_response(prompt, format_type='json')
    return parse_and_validate_json(json_response, expected_keys=['question', 'options', 'answer'])

def generate_summary(text_chunk):
    """
    Generates a 3-line summary from the given text using Ollama.
    """
    prompt = f"""
    You are an expert text summarizer.
    Summarize the text below in 3 simple lines.
    Return only the text of the summary, with no other explanations.

    Text:
    {text_chunk}
    """
    # 'text' format ke liye call karein (ab yeh 'format' parameter nahi bhejega)
    return get_ai_response(prompt, format_type='text')

def answer_doubt(full_text_context, user_question):
    """
    Answers a user's question based on the provided context using Ollama.
    """
    prompt = f"""
    You are a helpful study assistant. You are given a full document context and a user question.
    You must answer the user's question *only* using the provided context.
    If the answer is not in the context, state clearly: "The answer to this question is not found in the provided document."

    CONTEXT:
    ---
    {full_text_context}
    ---
    
    QUESTION:
    {user_question}
    
    ANSWER:
    """
    # 'text' format ke liye call karein
    return get_ai_response(prompt, format_type='text')
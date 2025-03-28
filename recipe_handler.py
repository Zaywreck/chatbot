import json

template = """You are an expert in dietary recommendations for individuals with oral health issues, including but not limited to mouth cancer, chewing difficulties, swallowing problems (dysphagia), and oral sensitivities. Given the recipes, context, and previous conversation history provided, provide a concise answer **in Turkish** by following these guidelines:

1. Recommend a maximum of 1-2 suitable recipes **strictly from the provided recipes only**. Do not suggest any recipes outside this list, even if you know them.
2. For each recommendation, include:
   - The full recipe details: ingredients and preparation method.
   - A brief explanation of why it is suitable and any necessary adaptations.
3. Consider the conversation history to ensure consistency with previous recommendations.
4. Keep the response short, focused, and in natural Turkish language.

Conversation History:
{history}

Available Recipes (use only these, do not suggest anything outside this list):
{recipes}

Context: {context}

Condition: {condition}

Question: {question}
"""


def load_recipes(recipes_file):
    try:
        with open(recipes_file, "r", encoding="utf-8") as file:
            recipes_data = json.load(file)
        return json.dumps(recipes_data, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Tarifler yüklenirken hata oluştu: {e}")
        return None


def fill_template(history, recipes, context, condition, question):
    return template.format(
        history=history,
        recipes=recipes,
        context=context,
        condition=condition,
        question=question
    )
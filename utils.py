import json
from collections import deque


def load_memory(memory_file):
    try:
        with open(memory_file, "r", encoding="utf-8") as file:
            memory_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        memory_data = {}
    return {user: deque(messages, maxlen=10) for user, messages in memory_data.items()}


def save_memory(memory, memory_file):
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump({user: list(messages) for user, messages in memory.items()}, file, indent=2, ensure_ascii=False)


def extract_condition_and_context(prompt, user_memory):
    prompt = prompt.lower()

    # Default values
    default_condition = "Ağız sağlığı sorunları"
    default_context = "Bireyin ağız sağlığı sorunları nedeniyle özel diyet ihtiyaçları var."

    # Retrieve previous state from memory if available
    prev_condition = user_memory[-1]["condition"] if user_memory and "condition" in user_memory[
        -1] else default_condition
    prev_context = user_memory[-1]["context"] if user_memory and "context" in user_memory[-1] else default_context

    # Initialize return values
    condition = prev_condition
    context = prev_context

    # Condition keyword sets (expanded)
    cancer_keywords = {"ağız kanseri", "mouth cancer", "oral cancer", "dil kanseri", "tongue cancer", "boğaz kanseri",
                       "throat cancer"}
    sore_keywords = {"ağız yarası", "mouth sore", "oral ulcer", "aft", "stomatit", "mukozit", "canker sore"}
    chewing_keywords = {"çiğneme zorluğu", "chewing difficulty", "çiğneyememe", "çene ağrısı", "jaw pain",
                        "sert çiğneyememe"}
    swallowing_keywords = {"yutma güçlüğü", "swallowing difficulty", "disfaji", "kolay yutulabilir", "dysphagia",
                           "yutamama", "boğazda takılma"}
    tooth_keywords = {"diş ağrısı", "tooth pain", "diş hassasiyeti", "tooth sensitivity", "diş çürüğü", "tooth decay",
                      "diş eti sorunu", "gum issue"}
    dry_mouth_keywords = {"ağız kuruluğu", "dry mouth", "xerostomia", "tükürük azlığı", "saliva deficiency",
                          "kuru boğaz"}
    inflammation_keywords = {"ağız iltihabı", "oral inflammation", "gingivitis", "diş eti iltihabı", "periodontitis"}

    # Context keyword sets (expanded)
    taste_sweet = {"tatlı", "sweet", "şekerli", "bal", "meyveli", "fruit-flavored", "tatlımsı"}
    taste_savory = {"tuzlu", "savory", "ekşi", "baharatlı", "spicy", "lezzetli", "umami"}
    taste_neutral = {"tatsız", "neutral", "hafif tat", "light taste", "nötr"}
    nutrition_keywords = {"besleyici", "nutritious", "kalorisi yüksek", "high calorie", "protein", "vitamin", "mineral",
                          "enerji verici", "zengin içerik"}
    prep_keywords = {"evde", "prepare at home", "kolay hazırlanır", "easy to prepare", "hızlı", "quick", "pratik",
                     "simple"}
    texture_keywords = {"yumuşak", "soft", "püre", "puree", "sıvı", "liquid", "kremsi", "creamy", "ezilmiş", "mashed",
                        "jöle", "jelly"}
    temp_keywords = {"soğuk", "cold", "sıcak", "hot", "ılık", "warm", "oda sıcaklığı", "room temperature", "buzlu",
                     "iced"}
    restriction_keywords = {"az yağlı", "low fat", "şekersiz", "sugar-free", "tuzsuz", "salt-free", "baharatsız",
                            "spice-free", "asitsiz", "non-acidic"}

    # Determine condition
    if any(keyword in prompt for keyword in cancer_keywords):
        condition = "Ağız kanseri ile çiğneme ve yutma zorlukları"
    elif any(keyword in prompt for keyword in sore_keywords):
        condition = "Ağız yarası ile yutma zorlukları"
    elif any(keyword in prompt for keyword in chewing_keywords):
        condition = "Çiğneme zorlukları"
    elif any(keyword in prompt for keyword in swallowing_keywords):
        condition = "Yutma zorlukları (disfaji)"
    elif any(keyword in prompt for keyword in tooth_keywords):
        condition = "Diş sorunları ve hassasiyet"
    elif any(keyword in prompt for keyword in dry_mouth_keywords):
        condition = "Ağız kuruluğu ile yutma zorlukları"
    elif any(keyword in prompt for keyword in inflammation_keywords):
        condition = "Ağız ve diş eti iltihabı"

    # Determine context
    # Taste preferences
    if any(keyword in prompt for keyword in taste_sweet):
        context = "Birey ağza nazik tatlı yiyecekler istiyor."
    elif any(keyword in prompt for keyword in taste_savory):
        context = "Birey ağza nazik tuzlu veya lezzetli yiyecekler istiyor."
    elif any(keyword in prompt for keyword in taste_neutral):
        context = "Birey ağza nazik ve nötr tatlı yiyecekler istiyor."
    else:
        context = "Bireyin ağız sağlığı için uygun yiyecekler aranıyor."

    # Additional context modifiers
    if any(keyword in prompt for keyword in nutrition_keywords):
        nutrition = next((kw for kw in nutrition_keywords if kw in prompt), "besleyici")
        context = context.replace("arıyor.", f"ve {nutrition} yiyecekler arıyor.")
    if any(keyword in prompt for keyword in prep_keywords):
        prep = next((kw for kw in prep_keywords if kw in prompt), "evde")
        context += f" {prep.capitalize()} hazırlanabilir olması önemli."
    if any(keyword in prompt for keyword in texture_keywords):
        texture = next((kw for kw in texture_keywords if kw in prompt), "yumuşak")
        context += f" {texture.capitalize()} kıvam tercih ediliyor."
    if any(keyword in prompt for keyword in temp_keywords):
        temp = next((kw for kw in temp_keywords if kw in prompt), "ılık")
        context += f" {temp.capitalize()} servis öneriliyor."
    if any(keyword in prompt for keyword in restriction_keywords):
        restriction = next((kw for kw in restriction_keywords if kw in prompt), "az yağlı")
        context += f" {restriction.capitalize()} içerik tercih ediliyor."

    return condition, context


def format_history(user_memory):
    if not user_memory:
        return "Geçmiş konuşma yok."
    history = "\n".join([f"Soru: {entry['prompt']}\nCevap: {entry['response']}" for entry in user_memory])
    return history
import openai
import time  # Pour ajouter des délais entre les demandes

# Remplace par ta clé API OpenAI
openai.api_key = "Your Api Key"

def ask_chatgpt(prompt_list):
    # Messages initiaux pour guider ChatGPT
    messages = [
        {
            "role": "system",
            "content": "You are a Rust programming assistant specialized in generating SVG files using Graphviz. Your responses must always provide only the Rust code that contains the 'digraph {...}' structure. Instead of using function names, output phrases in natural language that describe what the function or method is doing, without any additional explanations, comments, or text outside the code block."
        }
    ]
    
    # Ajouter tous les prompts dans l'historique de messages
    for prompt in prompt_list:
        messages.append({
            "role": "user",
            "content": prompt
        })
    
    while True:  # Boucle infinie jusqu'à obtention de la réponse correcte
        try:
            # Appel à l'API OpenAI ChatGPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ou "gpt-4" selon le modèle souhaité
                messages=messages,
                max_tokens=4000,  # Limite de tokens dans la réponse
                n=1,  # Nombre de réponses
                stop=None,  # La réponse s'arrête automatiquement
                temperature=0.7,  # Niveau de créativité
            )

            # Extraction de la réponse de l'assistant
            answer = response['choices'][0]['message']['content']

            # Vérification que la réponse commence par "```rust\ndigraph {"
            if answer.startswith("```rust\ndigraph {"):
                print("Réponse correcte :\n" + answer)
                return answer[7:-4]  # Extraire la partie utile de la réponse
            else:
                print("Réponse incorrecte, redemande à ChatGPT...")

                # Ajouter un message d'erreur dans la conversation pour indiquer que la réponse n'était pas correcte
                messages.append({
                    "role": "user",
                    "content": "The answer you gave is not correct. It does not start with '```rust\\ndigraph {...}'. Please correct and provide only the correct structure of the control flow graph (CFG) by replacing method and function names with natural language sentences."
                })

        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")
        
        # Petite pause avant de redemander pour éviter une surcharge d'appels API
        time.sleep(2)
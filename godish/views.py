from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# Directly configure the API key here
genai.configure(api_key="AIzaSyBkVoIAI9AzO1n_wrXFB_zsFyO6RmI2klg")

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def blog(request):
    return render(request, 'blog.html')

def home(request):
    return render(request, 'pymin2.html')

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def get_recipe(request):
    if request.method == 'POST':
        try:
            ingredients = request.POST.get('ingredients', '')
            cuisine = request.POST.get('cuisine', '')
            difficulty = request.POST.get('difficulty', '')

            if not ingredients or not cuisine or not difficulty:
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            prompt = f"""
            Create a detailed recipe using the following inputs:
            - Ingredients: {ingredients}
            - Cuisine type: {cuisine}
            - Difficulty level: {difficulty}

            Include:
            1. Full list of ingredients with quantities.
            2. Cooking and preparation time.
            3. Step-by-step preparation instructions with detailed explanations.
            4. Serving suggestions and plating tips.
            5. Optional variations of the recipe.

            Format should be in HTML:
            <h1>Dish Name</h1>
            <h2>Ingredients</h2>
            <ul>
                <li>Ingredient 1</li>
                <li>Ingredient 2</li>
            </ul>
            <h2>Preparation</h2>
            <p>Preparation instructions...</p>
            <h2>Serving Suggestions</h2>
            <p>Serving tips...</p>
            """

            # Start a chat session with the model
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)

            # Use the HTML response from Gemini
            recipe_html = response.text

            # Render the HTML response
            return render(request, 'recipe_form.html', {'recipe': recipe_html})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # If GET request, just render the empty form
    return render(request, 'recipe_form.html')

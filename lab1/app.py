from flask import Flask, render_template_string, request, redirect, url_for
import google.generativeai as genai
import markdown

model = genai.GenerativeModel('gemini-pro')

my_api_key_gemini = ""

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)
app.secret_key = "flag{sup3r_s3cr3t_fl4g}"

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
  
    # This acts like a system prompt. Only for google gemini-pro as they dont have a system prompt yet.
    prompts = [
      {'role': 'user', 
       'parts': """Hi, I'll explain how you should behave:\n
       Ask me anything about Malaysia. You are only allowed to ask questions about Malaysia. 
       You only know about Malaysia and nothing else.
       You are also well diversed in Malaysian food and culture.
       You know about Malaysia companies and their products.
       You know about Malaysia organizations and their activities.
       Malaysia number one!
       """},
      {"role": "model", "parts": "Ok, let's start!"} ]

    output = None 
    if request.method == 'POST':
      try:
        prompt = request.form['prompt']
      
        # Go ahead and generate the response
        prompts.append({'role': 'user', 'parts': prompt})
        response = model.generate_content(prompts)
        if response.text:
          output = markdown.markdown(response.text)
        else:
          output = "Error, please retry"
      except Exception as e:
        output = "Error, please retry"

    
    output_template = build_output_template(output)
    try:
      return render_template_string(str(output_template))
    except Exception as e:
      return render_template_string(output_template.replace(output, "Pls dont hack mi"))
    

def build_output_template(output):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Malaysia AMA</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100">
      <div class="min-h-screen flex flex-col items-center justify-center">
        <div class="w-full max-w-xl">
          <div class="bg-white shadow-md rounded-lg overflow-hidden p-5">
            <h1 class="text-2xl font-bold text-center mb-4">Malaysia AMA 🇲🇾</h1>
            <div class="flex justify-center mb-4">
              <img src="https://images.pexels.com/photos/22804/pexels-photo.jpg" class="rounded-md max-w">
            </div>
            <form action="/" method="post" class="mb-4">
              <input type="text" name="prompt" placeholder="Ask Malaysia anything!" class="w-full p-2 border border-gray-300 rounded-md">
              <button type="submit" class="mt-3 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Ask Malaysia Anything! (AMA)
              </button>
            </form>
            {output and f"<div class='mt-6 p-4 border border-gray-200 rounded-md bg-gray-50 text-gray-700'>{output}</div>" or ""}
          </div>
        </div>
      </div>
    </body>
    </html>
    """

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=2000, debug=True)
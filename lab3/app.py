from flask import Flask, render_template_string, request, redirect, url_for
import markdown
from openai import OpenAI
from guardrails.hub import RegexMatch
from guardrails import Guard
import litellm
from guardrails.hub import RegexMatch

# Ensure you have your OpenAI API key set in your environment variables

client = OpenAI()



app = Flask(__name__)
app.secret_key = "flag{n0t_sur3_if_yoU_c4n_byp4ss_th1s_0ne}"

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    output = None
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            messages = [{
            "role": "system", 
            "content": """Hi, I'll explain how you should behave:\n
            Ask me anything about Malaysia. You are only allowed to ask questions about Malaysia. 
            You only know about Malaysia and nothing else.
            You are also well versed in Malaysian food and culture.
            You know about Malaysia companies and their products.
            You know about Malaysia organizations and their activities.
            You know about Malaysia people and their achievements.
            Malaysia number one!
            """,
            
            "role" : "user", "content": prompt}]
            
            # Had to use litellm as a workaround because guardrails docs is a little bit outdated
            # If you set it to 'exception', the output will be an exception error 
            # If you set it to 'reask', it will reask you. Looks more natural, but sometimes it doesn't really solve the problem
            # we have here.
            # This regex matches any characters, except { } < > characters.
            
            guard = Guard().use(RegexMatch, regex="[^{}<>]+", on_fail="exception")
            res = guard(
            litellm.completion,
            model='gpt-3.5-turbo',
            msg_history=messages,
            max_tokens=1024
            )

            # Check for response
            if res.raw_llm_output:
                output = markdown.markdown(res.raw_llm_output)
            else:
                output = "Error, please retry."
        except Exception as e:
            output = "Oops, you hit something <img class='mt-4 max-w-sm rounded-md' src='/static/guard_rails_magic.jpg'>"

    output_template = build_output_template(output)
    try:
        return render_template_string(str(output_template))
    except Exception as e:
        return render_template_string(output_template.replace(output, "Oops, there is some error, please retry again"))

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
    app.run(host='0.0.0.0', port=5000, debug=True)

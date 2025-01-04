import openai
import os
from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']


def generate_tutorial(components):
  response = openai.Images.create(prompt=components,
                                  model="dall-e-3",
                                  size="1024x1024",
                                  response_format="url")
  image_url = response['data'][0]['url']
  return image_url


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
  output = ""

  if request.method == 'POST':
    components = request.form['components']
    output = generate_tutorial(components)

  return render_template_string('''

  <!DOCTYPE html>
    <html>
        <head>
            <title>Infinite Image Generator</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
    <body>
        <div class="container">
            <h1 class="my-4">Custom Image Generator</h1>
            <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
                <div class="mb-3">
                    <label for="components" class="form-label">Textual Description of the Image:</label>
                    <input type="text" class="form-control" id="components" name="components" placeholder="Enter the Description (Ex: A Lion in a Cage)" required>
                </div>
                <button type="submit" class="btn btn-primary">Generate the Image</button>
            </form>
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    Output:
                    <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
                </div>
                <div class="card-body">
                    <p id="output" style="white-space: pre-wrap;"></p>
                    <img id="myImage" src="" style="width: auto; height: 300px;">
                </div>
            </div>
        </div>

            <script>
            async function generateTutorial() {
                const components = document.querySelector('#components').value;
                const output = document.querySelector('#output');
                const imgElement = document.getElementById('myImage');
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: new FormData(document.querySelector('#tutorial-form'))
                });
                const imageUrl = await response.text();
                imgElement.src = imageUrl;
                output.textContent = 'Generating an image for you...';
            }
            function copyToClipboard() {
                const imgElement = document.getElementById('myImage');
                const imageUrl = imgElement.src;
                const textarea = document.createElement('textarea');
                textarea.value = imageUrl;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('Copied to clipboard');
                }
            </script>
        </body>
    </html>

  ''',
                                output=output)


@app.route('/generate', methods=['POST'])
def generate():
  components = request.form['components']
  return generate_tutorial(components)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

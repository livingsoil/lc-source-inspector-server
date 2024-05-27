from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    print(url)
    return 'URL received'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/health')
def health():
  return 'OK'

def main():
  app.run(debug=True)

if __name__ == '__main__':
  main()
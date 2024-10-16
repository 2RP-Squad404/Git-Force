from flask import Flask

app = Flask(__name__)

# Defina uma rota para a página inicial
@app.route('/')
def home():
    return "Bem-vindo ao backend!"

# Outras rotas que você possa precisar
# Exemplo:
# @app.route('/outra_rota')
# def outra_rota():
#     return "Esta é outra rota."

if __name__ == '__main__':
    app.run(debug=True)

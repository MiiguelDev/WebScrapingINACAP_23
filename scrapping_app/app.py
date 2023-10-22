from flask import Flask, render_template
from funciones import scrap_tallarines

app = Flask(__name__)

@app.route('/')
def mostrar_precio_tallarines():
    resultado = scrap_tallarines()
    return render_template('precio_tallarines.html', resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)

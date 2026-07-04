from flask import Flask, render_template_string, jsonify
from mimesis import Person
from mimesis.locales import Locale
import random

app = Flask(__name__)

# All supported locales
LOCALES = [
    Locale.EN,
    Locale.EN_AU,
    Locale.EN_CA,
    Locale.EN_GB,
    Locale.EN_IE,
    Locale.EN_IN,
    Locale.EN_NZ,
    Locale.EN_SG,
    Locale.EN_US,
    Locale.DE,
    Locale.ES,
    Locale.FR,
    Locale.IT,
    Locale.PT,
    Locale.RU,
    Locale.TR,
    Locale.PL,
    Locale.NL,
    Locale.SV,
    Locale.NO,
    Locale.DA,
    Locale.FI,
    Locale.CS,
    Locale.SK,
    Locale.HU,
    Locale.RO,
    Locale.UK,
    Locale.KK,
    Locale.KO,
    Locale.JA,
    Locale.ZH,
]

def random_name():
    locale = random.choice(LOCALES)
    person = Person(locale)
    return person.full_name()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Name Generator</title>

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
    background:#0f172a;
    font-family:Arial,sans-serif;
}

.card{
    width:100%;
    max-width:420px;
    background:#1e293b;
    border-radius:20px;
    padding:30px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,.35);
}

.title{
    color:#fff;
    font-size:24px;
    font-weight:700;
    margin-bottom:25px;
}

.name-box{
    background:#334155;
    color:#fff;
    font-size:28px;
    font-weight:700;
    padding:18px;
    border-radius:12px;
    word-break:break-word;
    margin-bottom:20px;
}

.change-btn{
    width:100%;
    border:none;
    border-radius:12px;
    padding:16px;
    font-size:18px;
    font-weight:600;
    cursor:pointer;
    color:white;
    background:#16a34a;
    transition:.2s;
}

.change-btn:active{
    transform:scale(.98);
}

@media (max-width:480px){

    .card{
        padding:24px;
    }

    .title{
        font-size:22px;
    }

    .name-box{
        font-size:24px;
        padding:16px;
    }

    .change-btn{
        font-size:17px;
        padding:15px;
    }
}
</style>
</head>

<body>

<div class="card">

    <div class="title">
        Name Generator
    </div>

    <div class="name-box" id="name">
        {{ name }}
    </div>

    <button class="change-btn" onclick="changeName()">
        Change Name
    </button>

</div>

<script>

async function changeName(){

    try{

        const response = await fetch("/new-name");
        const data = await response.json();

        document.getElementById("name").innerText = data.name;

        await navigator.clipboard.writeText(data.name);

    }catch(err){
        console.log(err);
    }
}

</script>

</body>
</html>
"""

@app.route("/new-name")
def new_name():
    return jsonify({
        "name": random_name()
    })

@app.route("/")
def home():
    return render_template_string(
        HTML,
        name=random_name()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, render_template_string, jsonify
from faker import Faker
import random

app = Flask(__name__)
LOCALES = [
    "en_US",
    "en_GB",
    "en_CA",
    "en_AU",
    "fr_FR",
    "de_DE",
    "es_ES",
    "it_IT",
    "pt_BR",
    "nl_NL",
    "pl_PL",
    "ru_RU",
    "uk_UA",
    "tr_TR",
    "el_GR",
    "cs_CZ",
    "sv_SE",
    "fi_FI",
    "da_DK",
    "no_NO",
    "hu_HU",
    "ro_RO",
    "sk_SK",
    "sl_SI",
    "hr_HR",
    "bg_BG",
    "ja_JP",
    "ko_KR",
    "zh_CN",
    "zh_TW",
    "hi_IN",
    "bn_BD",
    "ar_EG",
    "th_TH",
    "vi_VN",
    "id_ID",
]

fakers = [Faker(locale) for locale in LOCALES]

def random_name():
    return random.choice(fakers).name()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>US Name Generator</title>

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
        US Name Generator
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

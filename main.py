from flask import Flask, render_template_string, jsonify
from faker import Faker
from collections import deque
import random
import threading

app = Flask(__name__)

ENGLISH_LOCALES = [
    "en_US",
    "en_GB",
    "en_CA",
    "en_AU",
    "en_NZ",
    "en_IE",
    "en_IN"
]

fakers = [Faker(locale) for locale in ENGLISH_LOCALES]

# Keeps track of recently generated names so the same one
# doesn't pop up again too soon. Thread-safe for Flask's
# multi-threaded dev/prod servers.
RECENT_HISTORY_SIZE = 50
MAX_GENERATION_ATTEMPTS = 20

_recent_names = deque(maxlen=RECENT_HISTORY_SIZE)
_recent_names_lock = threading.Lock()


def _generate_candidate():
    fake = random.choice(fakers)
    return f"{fake.first_name()} {fake.last_name()}"


def random_name():
    with _recent_names_lock:
        for _ in range(MAX_GENERATION_ATTEMPTS):
            candidate = _generate_candidate()
            if candidate not in _recent_names:
                _recent_names.append(candidate)
                return candidate

        # Fallback: if we somehow can't find a fresh name
        # (extremely unlikely), just return the last candidate
        # generated rather than looping forever.
        _recent_names.append(candidate)
        return candidate


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Name Generator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
    --bg-1:#0b0f1a;
    --bg-2:#141a2e;
    --accent-1:#8b5cf6;
    --accent-2:#22d3ee;
    --accent-3:#f472b6;
    --surface:rgba(255,255,255,0.06);
    --surface-border:rgba(255,255,255,0.12);
    --text-main:#f5f7ff;
    --text-dim:#9aa3bd;
}
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}
html,body{
    min-height:100vh;
}
body{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:24px;
    font-family:'Inter',sans-serif;
    color:var(--text-main);
    background:
        radial-gradient(circle at 15% 20%, rgba(139,92,246,0.25), transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(34,211,238,0.18), transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(244,114,182,0.15), transparent 45%),
        linear-gradient(160deg, var(--bg-1), var(--bg-2));
    background-attachment:fixed;
    position:relative;
    overflow:hidden;
}

/* subtle floating orbs */
.orb{
    position:absolute;
    border-radius:50%;
    filter:blur(60px);
    opacity:0.5;
    animation:float 12s ease-in-out infinite;
    z-index:0;
}
.orb-1{
    width:280px;height:280px;
    background:var(--accent-1);
    top:-80px;left:-80px;
    animation-delay:0s;
}
.orb-2{
    width:220px;height:220px;
    background:var(--accent-2);
    bottom:-60px;right:-60px;
    animation-delay:3s;
}
@keyframes float{
    0%,100%{ transform:translateY(0) translateX(0); }
    50%{ transform:translateY(-25px) translateX(15px); }
}

.card{
    position:relative;
    z-index:1;
    width:100%;
    max-width:440px;
    background:var(--surface);
    border:1px solid var(--surface-border);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border-radius:24px;
    padding:40px 32px;
    text-align:center;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.08);
    animation:rise .6s cubic-bezier(.22,1,.36,1);
}
@keyframes rise{
    from{ opacity:0; transform:translateY(18px) scale(.98); }
    to{ opacity:1; transform:translateY(0) scale(1); }
}

.badge{
    display:inline-flex;
    align-items:center;
    gap:6px;
    font-size:12px;
    font-weight:600;
    letter-spacing:.06em;
    text-transform:uppercase;
    color:var(--accent-2);
    background:rgba(34,211,238,0.12);
    border:1px solid rgba(34,211,238,0.25);
    padding:6px 14px;
    border-radius:999px;
    margin-bottom:18px;
}
.badge::before{
    content:"";
    width:6px;height:6px;
    border-radius:50%;
    background:var(--accent-2);
    box-shadow:0 0 8px var(--accent-2);
}

.title{
    font-family:'Sora',sans-serif;
    font-size:26px;
    font-weight:700;
    margin-bottom:6px;
    letter-spacing:-.02em;
}
.subtitle{
    font-size:14px;
    color:var(--text-dim);
    margin-bottom:28px;
}

.name-box{
    position:relative;
    background:linear-gradient(135deg, rgba(139,92,246,0.15), rgba(34,211,238,0.1));
    border:1px solid var(--surface-border);
    color:var(--text-main);
    font-family:'Sora',sans-serif;
    font-size:28px;
    font-weight:700;
    padding:26px 20px;
    border-radius:16px;
    word-break:break-word;
    margin-bottom:24px;
    transition:transform .25s ease, opacity .25s ease;
}
.name-box.swapping{
    transform:scale(.96);
    opacity:0.4;
}

.copied-tag{
    position:absolute;
    top:10px;
    right:14px;
    font-size:11px;
    font-weight:600;
    color:#22d3ee;
    opacity:0;
    transition:opacity .3s ease;
}
.copied-tag.show{
    opacity:1;
}

.change-btn{
    width:100%;
    border:none;
    border-radius:14px;
    padding:17px;
    font-family:'Sora',sans-serif;
    font-size:16px;
    font-weight:700;
    letter-spacing:.01em;
    cursor:pointer;
    color:#0b0f1a;
    background:linear-gradient(135deg, var(--accent-2), var(--accent-1));
    box-shadow:0 8px 24px rgba(139,92,246,0.35);
    transition:transform .15s ease, box-shadow .15s ease, filter .15s ease;
}
.change-btn:hover{
    filter:brightness(1.08);
    box-shadow:0 10px 28px rgba(139,92,246,0.45);
}
.change-btn:active{
    transform:scale(.97);
}
.change-btn:disabled{
    opacity:0.6;
    cursor:default;
}

.hint{
    margin-top:16px;
    font-size:12.5px;
    color:var(--text-dim);
}

@media (max-width:480px){
    .card{
        padding:32px 22px;
    }
    .title{
        font-size:22px;
    }
    .name-box{
        font-size:23px;
        padding:22px 16px;
    }
    .change-btn{
        font-size:15px;
        padding:16px;
    }
}
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<div class="card">
    <div class="badge">Live Generator</div>
    <div class="title">Name Generator</div>
    <div class="subtitle">Realistic English-locale names, one tap away</div>

    <div class="name-box" id="name">
        <span class="copied-tag" id="copiedTag">Copied</span>
        {{ name }}
    </div>

    <button class="change-btn" id="changeBtn" onclick="changeName()">
        Generate New Name
    </button>

    <div class="hint">Auto-copied to your clipboard</div>
</div>

<script>
async function changeName(){
    const box = document.getElementById("name");
    const btn = document.getElementById("changeBtn");
    const tag = document.getElementById("copiedTag");

    btn.disabled = true;
    box.classList.add("swapping");

    try{
        const response = await fetch("/new-name");
        const data = await response.json();

        setTimeout(() => {
            box.innerHTML = `<span class="copied-tag" id="copiedTag">Copied</span>${data.name}`;
            box.classList.remove("swapping");
        }, 150);

        await navigator.clipboard.writeText(data.name);

        setTimeout(() => {
            const newTag = document.getElementById("copiedTag");
            if(newTag){
                newTag.classList.add("show");
                setTimeout(() => newTag.classList.remove("show"), 1400);
            }
        }, 200);
    }catch(err){
        console.log(err);
        box.classList.remove("swapping");
    }finally{
        btn.disabled = false;
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

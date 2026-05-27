from flask import Flask, render_template, request
import time

app = Flask(__name__, template_folder="../templates")


def rabin_karp(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)

    h = pow(d, m - 1) % q
    p = 0
    t = 0
    result = []

    if m > n:
        return []

    # Calculate hash
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Sliding window
    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                result.append(s)

        if s < n - m:
            t = (
                d * (t - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t < 0:
                t += q

    return result


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    execution_time = None
    text_length = 0
    pattern_length = 0

    if request.method == "POST":
        text = request.form["text"]
        pattern = request.form["pattern"]

        stime = time.time()

        result = rabin_karp(text, pattern)

        etime = time.time()

        execution_time = etime - stime
        text_length = len(text)
        pattern_length = len(pattern)

    return render_template(
        "index.html",
        result=result,
        execution_time=execution_time,
        text_length=text_length,
        pattern_length=pattern_length
    )


app = app
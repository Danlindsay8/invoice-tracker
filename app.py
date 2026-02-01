from flask import Flask, request, render_template_string

app = Flask(__name__)

FORM_TEMPLATE = """
<!doctype html>
<html>
  <head><title>Invoice Tracker</title></head>
  <body>
    <h1>Add an Invoice</h1>
    <form method="POST">
      Customer name: <input name="customer" required><br><br>
      Amount ($): <input name="amount" type="number" step="0.01" required><br><br>
      Due date: <input name="date" type="date" required><br><br>
      <button type="submit">Save & Send Reminder</button>
    </form>
    <hr>
    {% if saved %}
      <p style="color:green;">Saved! Reminder would go to {{ customer }} for ${{ amount }} on {{ date }}.</p>
    {% endif %}
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    saved = False
    customer = amount = date = None

    if request.method == 'POST':
        customer = request.form.get('customer')
        amount = request.form.get('amount')
        date = request.form.get('date')
        saved = True

    return render_template_string(FORM_TEMPLATE, saved=saved, customer=customer, amount=amount, date=date)

if __name__ == '__main__':
    app.run()

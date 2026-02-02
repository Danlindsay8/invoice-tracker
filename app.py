from flask import Flask, request, render_template_string
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Brevo SMTP config (replace with YOUR values)
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_brevo_account_email@gmail.com'          # ← your signup email
app.config['MAIL_PASSWORD'] = 'your_generated_smtp_key_here'               # ← the SMTP key from Brevo
app.config['MAIL_DEFAULT_SENDER'] = 'your_verified_sender_email@gmail.com' # ← verified in Brevo

mail = Mail(app)

FORM_TEMPLATE = """
<!doctype html>
<html>
  <head><title>Invoice Tracker</title></head>
  <body>
    <h1>Add an Invoice</h1>
    <form method="POST">
      Customer name: <input name="customer" required><br><br>
      Amount ($): <input name="amount" type="number" step="0.01" required><br><br>
      Email / Phone: <input name="contact" placeholder="email@example.com" required><br><br>
      Due date: <input name="date" type="date" required><br><br>
      <button type="submit">Save & Send Reminder</button>
    </form>
    <hr>
    {% if saved %}
      <p style="color:green;">Saved! Reminder sent to {{ contact }} for ${{ amount }} due {{ date }}.</p>
    {% endif %}
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    saved = False
    customer = amount = contact = date = None

    if request.method == 'POST':
        customer = request.form.get('customer')
        amount = request.form.get('amount')
        contact = request.form.get('contact')
        date = request.form.get('date')
        saved = True

        if contact:
            try:
                msg = Message(
                    subject=f"Invoice Reminder - ${amount}",
                    recipients=[contact],
                    body=f"Hi {customer},\n\nYour invoice for ${amount} is due on {date}.\n\nThanks!\nPlease pay soon."
                )
                mail.send(msg)
                print("Email sent successfully!")  # shows in Render logs
            except Exception as e:
                print(f"Failed to send email: {e}")

    return render_template_string(
        FORM_TEMPLATE,
        saved=saved,
        customer=customer,
        amount=amount,
        contact=contact,
        date=date
    )

if __name__ == '__main__':
    app.run()

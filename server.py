from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/<string:page_name>")
def html_page(page_name=None):
    return render_template(page_name)

def write_to_database(data):
    with open("database.txt", mode="a") as db:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        db.write(f"{email},{subject},{message}")


def write_to_csv(data):
    file_exists = os.path.isfile("database.csv")

    if not file_exists:
        with open("database.csv", mode="w", newline='') as db2:
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["email", "subject", "message"])

    with open("database.csv", mode="a", newline='') as db2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/email_sent', methods=['POST', 'GET'])
def email_sent():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv(data)    
            return redirect("/thankyou.html")
        except:
            return "did not save to the database"
    else:   
        return "something went wrong :( Try again! "

if __name__ == "__main__":
    app.run(debug=True)
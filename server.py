from flask import Flask, jsonify, render_template, request
import sqlite3
import json
import mich

SUB_MED_FOUND = "מצאנו את התרופה שחיפשת!"
BODY_MED_FOUND = "!משתמש חדש הוסיף למאגר את התרופה שחיפשת<br> היכנס.י לאתר למציאת התרופה המבוקשת"

SUB_GETTER_FOUND = "מצאנו מישהו שמוסר את התרופה שחיפשת!"
SUB_GIVER_FOUND = "מצאנו מישהו שמעוניין בתרופה שאתה רוצה למסור!"
HEADERS = ["id", "medicine name", "amount", "city", "expiration date", "is closed", "owner name", "picture"]


app = Flask(__name__, static_url_path='/static')

def translate_to_dict(list_data):
    dict_id = 1
    outer_dict = {}
    for cur_tuple in list_data:
        inner_dict = {}
        for i in range(8):
            inner_dict[HEADERS[i]] = cur_tuple[i]
        outer_dict[dict_id] = inner_dict
        dict_id += 1

    return outer_dict


@app.route("/")
def index():
    return render_template("final_website.html")

@app.route("/insert")
def insert():
    return render_template("insert.html")


@app.route("/check=<name>")
def check(name):
    name = mich.my_trans(name)
    name = mich.best_word(all_meds, name)
    name = (name,)
    c.execute('''select meds.uid, meds.med_name, meds.amount, meds.city,
                  meds.expiration_date, meds.is_closed, meds.owner_name, meds_data.picture
                  from meds
                  inner join meds_data on meds.med_name = meds_data.med_name
                  where meds.med_name = ? collate nocase''', name)
    dict_result = translate_to_dict(c.fetchall())
    json_return = json.dumps(dict_result)

    return json_return


@app.route("/add_waiting", methods= ["POST"])
def add_waiting():
    data = request.form
    details = (data["mail"], data["name"], data["med"])

    c.execute("INSERT INTO waiting VALUES (?,?,?)", details)
    conn.commit()
    return jsonify(json.dumps({'state':0}))

# @app.route("/add_waiting")
# def add_waiting():
#     details = (request.args.get("mail"), request.args.get("name"),
#                request.args.get("med"))
#
#     print("klklk")
#     c.execute("INSERT INTO waiting VALUES (?,?,?)", details)
#     conn.commit()
#     return


def send_mails_to_waiting_list(med_name):
    med_tuple = (med_name,)
    c.execute('''select mail, name
                      from waiting
                      where med_name = ? collate nocase''', med_tuple)
    data = c.fetchall()
    if data:
        for tup in data:
            mich.send_mail(tup[0], tup[1], SUB_MED_FOUND, BODY_MED_FOUND)


def create_msg_getter(mail_giver, name_giver):
    return (SUB_GETTER_FOUND, "מצאנו מישהו שימסור לך את התרופה, אנא פנה ל- " + name_giver + " במייל: " + mail_giver)


def create_msg_giver(mail_getter, name_getter):
    return (SUB_GIVER_FOUND, "מצאנו מישהו שישמח לקבל ממך את התרופה, אנא פנה ל- " + name_getter + " במייל: " + mail_getter)


@app.route("/select_item", methods = ["POST"])
def select_item():
    print("here")

     #in args i need: uid of giver, mail_getter, name_getter
    data = request.form
    uid_tuple = (data["uid"], )
    c.execute('''select mail, name
                 from meds
                 where uid = ? collate nocase''', uid_tuple)
    mail_giver, name_giver = c.fetchall()
    msg_to_getter = create_msg_getter(mail_giver, name_giver)
    mich.send_mail(data["mail"], data["name"],
                   msg_to_getter[0], msg_to_getter[1])

    msg_to_giver = create_msg_giver(request.args["mail"], request.args["name"])
    mich.send_mail(mail_giver, name_giver, msg_to_getter[0], msg_to_getter[1])

    c.execute('''select med_name
                     from meds
                     where uid = ?''', uid_tuple)
    medication = c.fetchone()[0]

    # delete the med
    c.execute('''delete
                from meds
                where uid = ?''', uid_tuple)

    # delete the request

    waiting_details = (request.args["mail_getter"], medication)
    c.execute('''delete
                from waiting
                where mail = ? and med_name = ? collate nocase''', waiting_details)
    conn.commit()

    return


@app.route("/add", methods=['POST'])
def add():
    global uid
    data = request.form
    med_name = mich.my_trans(data["med_name"])
    med_name = mich.best_word(all_meds, med_name)
    if med_name is None:
        return jsonify(json.dumps({'state': 1}))
    print(data["is_closed"])
    if data["is_closed"] == "true":
        closed = "YES"
    else:
        closed = "NO"
    details = (uid, med_name, data["date"], float(data["amount"]), closed,
               data["city"], data["owner_mail"], data["owner_name"])
    uid += 1
    c.execute("INSERT INTO meds VALUES (?,?,?,?,?,?,?,?)", details)
    conn.commit()
    send_mails_to_waiting_list(med_name)
    return jsonify(json.dumps({'state': 0}))


if __name__ == "__main__":
    conn = sqlite3.connect('medicine_db.db')
    c = conn.cursor()
    c.execute('''select distinct med_name from meds_data''')
    all_meds = []
    for med in c.fetchall():
        all_meds.append(med[0])
    c.execute('''select max(uid) from meds''')
    uid = c.fetchone()[0] + 1
    app.run()
    conn.close()



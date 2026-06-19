from flask import Flask,request,make_response,jsonify, render_template
from pony import orm
from datetime import datetime
from collections import defaultdict

DB = orm.Database()

app = Flask(__name__)

class Gear(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    gear_type = orm.Required(str)
    slot = orm.Required(str)
    power = orm.Required(int)
    stat = orm.Required(str)
    modifier = orm.Required(int) # prvotno nazvan "effect", ali "modifier" je bolji opis

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

def add_gear(json_request):
    try:
        name = json_request["name"]
        gear_type = json_request["gear_type"]
        slot = json_request["slot"]
        power = int(json_request["power"])
        stat = json_request["stat"]
        modifier = int(json_request["modifier"])

        with orm.db_session:
            Gear(name=name, gear_type=gear_type, slot=slot, power=power, stat=stat, modifier=modifier)
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def get_gear():
    try:
        with orm.db_session:
            db_querry = orm.select(x for x in Gear)[:]
            results_list = []
            for r in db_querry:
                results_list.append(r.to_dict())
            response = {"response": "Success", "data": results_list}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}
    
def get_gear_by_id(gear_id):
    try:
        with orm.db_session:
            result = Gear[gear_id].to_dict()
            response = {"response": "Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def patch_gear(gear_id, json_request):
    try:
        with orm.db_session:
            g = Gear[gear_id]
            if not g:
                return {"response": "Not found"}, 404
            g.name = json_request['name']
            g.gear_type = json_request['gear_type']
            g.slot = json_request['slot']
            g.power = int(json_request['power'])
            g.stat = json_request['stat']
            g.modifier = int(json_request['modifier'])
            return {"response": "Success"}, 200
    except Exception as e:
        return {"response": "Fail", "error": str(e)}, 400
    
def delete_gear(gear_id):
    try:
        with orm.db_session:
            to_delete = Gear[gear_id]
            to_delete.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

@app.route("/add_gear", methods=["POST","GET"])
@orm.db_session
def dodaj_gear():
    if request.method == "POST":
            try:
                json_request = {}
                for key,value in request.form.items():
                    if value == "":
                        json_request[key] = None
                    else:
                        json_request[key] = value
            except Exception as e:
                response = {"response":str(e)}
                return make_response(jsonify(response),400)

            response = add_gear(json_request)

            if response["response"] == "Success":
                return make_response(render_template("add_gear.html"),200)
            return make_response(jsonify(response),400)
    else:
        return make_response(render_template("add_gear.html"),200)
    
@app.route("/view_gear", methods=["GET"])
@orm.db_session
def vrati_gear():
    if request.args and 'id' in request.args:
        gear_id = int(request.args.get("id"))
        response = get_gear_by_id(gear_id)
        if response["response"] == "Success":
            return make_response(render_template("view_gear.html", data=response["data"]), 200)
        return make_response(jsonify(response), 400)
    response = get_gear()
    if response["response"] == "Success":
        return make_response(render_template("view_gear.html", data=response["data"]), 200)
    return make_response(jsonify(response), 400)

@app.route("/gear/<int:gear_id>", methods=["DELETE"])
@orm.db_session
def obrisi_gear(gear_id):
    response = delete_gear(gear_id)
    if response["response"] == "Success":
            return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)



@app.route('/gear/<int:gear_id>', methods=['PATCH'])
@orm.db_session
def izmjeni_gear(gear_id):
    try:
        json_request = request.json
    except Exception as e:
        return jsonify({"response": "Invalid JSON"}), 400
    
    response, status = patch_gear(gear_id, json_request)
    return jsonify(response), status


@app.route("/")
@orm.db_session
def home():
    return render_template("index.html")


@app.route("/vizualizacija")
@orm.db_session
def gear_stats():
    gear_slots = ["Head", "Armor", "Back", "Weapon", "Trinket"]
    stats = {}
    
    for gear_slot in gear_slots:
        avg_power = orm.select(orm.avg(g.power) for g in Gear if g.slot == gear_slot).first()
        stats[gear_slot] = avg_power if avg_power else 0
    
    return render_template("vizualizacija.html", data=stats)

if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)

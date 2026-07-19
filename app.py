from flask import Flask,jsonify,request
from database import get_connection
from validation import validate_server, patch_validation


app = Flask(__name__)

# ============================================================
# BASIC ROUTES
# ============================================================

@app.route("/")
def home():
    return "Welcome to Infra List of Servers"

@app.route("/version")
def version():
    return "ver 1.0.0"

@app.route("/author")
def author():
    return "current user"

# ============================================================
# SERVER ROUTES
# ============================================================
@app.route("/servers")
def get_servers():
    connection=get_connection()

    cursor=connection.cursor()

    cursor.execute("Select * from servers")

    db_rows=cursor.fetchall()
    connection.close()


    servers=[]

    for row in db_rows:
        server_record = {
        
            "id":row[0],
            "name":row[1],
            "ip":row[2],
            "os":row[3],

        }

        servers.append(server_record)
    return jsonify(servers)

#POST FUNCTION

@app.route("/servers",methods=["POST"])
def post_servers():
    
    data=request.get_json()
    error=validate_server(data)

    if error:
        return error
    

    connection=get_connection()
    cursor=connection.cursor()
    


    cursor.execute("""
    INSERT INTO servers (name,ip,os) 
    Values (?,?,?)""",
    (data["name"],data["ip"],data["os"]) 
    )

    new_id=cursor.lastrowid

    connection.commit()
    connection.close()

    return jsonify({
    "message": "Server created successfully",
    "id": new_id
    }), 201
    
    '''data= request.get_json()
    
    error = validate_server(data)

    if error:
        return error

    new_id=len(servers)+1
    data["id"]=new_id
    servers.append(data)
    return jsonify(data),201
'''
#GET SERVER ID
@app.route("/servers/<int:id>")
def get_server_by_id(id):

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("Select * from servers where id=?",(id,))


    row=cursor.fetchone()
    connection.close()
    
    if row:   

        server_record = {
        
            "id":row[0],
            "name":row[1],
            "ip":row[2],
            "os":row[3],

        }

        
        return jsonify(server_record)
    return jsonify({"error": "Server not found"}), 404





    """for server in servers:
        if server["id"]==id:
            return jsonify(server)
    else:
        return jsonify({"error": "Server not found"}), 404"""


#PUT FUNCTION
@app.route("/servers/<int:id>",methods=['PUT'])
def put_servers(id):

    data = request.get_json()

    error = validate_server(data)

    if error:
        return error

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    UPDATE servers SET name=?,ip=?,os=? where id =? """, (data["name"], data["ip"], data["os"], id)
    )

    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Server not found"}), 404

    connection.commit()

    connection.close()

    return jsonify({"message": "Server updated successfully"}), 200



    """
    data=request.get_json()
    
    error=validate_server(data)
    if error:
        return error
    
    for server in servers:
        if server["id"]==id:
            server["name"]=data["name"]
            server["ip"]=data["ip"]
            server["os"]=data["os"]
            return jsonify(server),200 #contains id
    
    return "ID not found", 404
"""
#DELETE SERVER
@app.route("/servers/<int:id>",methods=['DELETE'])
def delete_server(id):

    data = request.get_json()

    
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("DELETE from servers where id=?" ,(id,))

    if cursor.rowcount==0:
        connection.close()
        return jsonify({"error": "Server not found"}), 404
    
    connection.commit()

    connection.close()

    return jsonify({"message": "Server deleted successfully"}), 200


"""
    for server in servers:
        if server["id"]==id:
            servers.remove(server)
            return "delete successful" ,200

  return "ID not found" , 404 """

#PATCH SERVER
@app.route("/servers/<int:id>",methods=['PATCH'])
def patch_servers(id):

    data=request.get_json()

    error=patch_validation(data)
    
    if error:
        return error


    update_field=[]
    update_values=[]

    if "name" in data:
        update_field.append("name=?")
        update_values.append(data["name"])

    if "ip" in data:
        update_field.append("ip=?")
        update_values.append(data["ip"])

    if "os" in data:
        update_field.append("os=?")
        update_values.append(data["os"])

    # No valid fields provided
    if not update_field:
        return jsonify({"error": "No fields provided"}), 400


    set_clause=",".join(update_field)

    connection=get_connection()
    cursor=connection.cursor()

    update_values.append(id)


    query=f"""
    UPDATE servers
    SET {set_clause} where id=? 
    """


    print(query)
    print(update_values)
    
    cursor.execute(query,update_values)

    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Server not found"}), 404

    connection.commit()

    connection.close()

    return jsonify({"message": "Server updated successfully"}), 200
    




"""
    for server in servers:
        if server["id"]==id:
            if "name" in data:
                server["name"]=data["name"]
            if "ip" in data:
                server["ip"]=data["ip"]
            if "os" in data:
                server["os"]=data["os"]
            return jsonify(server), 200
    return "Not found", 404
"""

if __name__ == "__main__":
    app.run(debug=True)
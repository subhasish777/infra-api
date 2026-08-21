from flask import Flask, jsonify, request, render_template
from database import get_connection
from validation import validate_server, patch_validation


def create_app():
    app = Flask(__name__)

    def row_to_dict(row):
        return {
            "id": row[0],
            "name": row[1],
            "ip": row[2],
            "os": row[3]
        }


    # ============================================================
    # BASIC ROUTES
    # ============================================================

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy"
        }), 200    
    
    # CHANGED: Now rendering the HTML template instead of a raw string
    @app.route("/")
    def home():
        return render_template("index.html")

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
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("Select * from servers")

        db_rows = cursor.fetchall()
        connection.close()

        servers = []
        for row in db_rows:
            servers.append(row_to_dict(row))

        return jsonify(servers)


    @app.route("/servers", methods=["POST"])
    def post_servers():
        data = request.get_json()
        error = validate_server(data)

        if error:
            return error
        
        connection = get_connection()
        cursor = connection.cursor()
        
        # CHANGED: ? to %s and added "RETURNING id" for Postgres compatibility
        cursor.execute("""
        INSERT INTO servers (name, ip, os) 
        VALUES (%s, %s, %s) RETURNING id""",
        (data["name"], data["ip"], data["os"]) 
        )

        # CHANGED: Using fetchone() instead of lastrowid to grab the new Postgres ID
        new_id = cursor.fetchone()[0]

        connection.commit()
        connection.close()

        return jsonify({
        "message": "Server created successfully",
        "id": new_id
        }), 201
        
            
    @app.route("/servers/<int:id>")
    def get_server_by_id(id):
        connection = get_connection()
        cursor = connection.cursor()

        # CHANGED: ? to %s
        cursor.execute("Select * from servers where id=%s", (id,))

        row = cursor.fetchone()
        connection.close()
        
        if row:   
            return jsonify(row_to_dict(row))

        return jsonify({"error": "Server not found"}), 404


    @app.route("/servers/<int:id>", methods=['PUT'])
    def put_servers(id):
        data = request.get_json()
        error = validate_server(data)

        if error:
            return error

        connection = get_connection()
        cursor = connection.cursor()

        # CHANGED: ? to %s across the board
        cursor.execute("""
        UPDATE servers SET name=%s, ip=%s, os=%s where id=%s """, 
        (data["name"], data["ip"], data["os"], id)
        )

        if cursor.rowcount == 0:
            connection.close()
            return jsonify({"error": "Server not found"}), 404

        connection.commit()
        connection.close()

        return jsonify({"message": "Server updated successfully"}), 200
    
    
    @app.route("/servers/<int:id>", methods=['DELETE'])
    def delete_server(id):
        connection = get_connection()
        cursor = connection.cursor()

        # CHANGED: ? to %s
        cursor.execute("DELETE from servers where id=%s", (id,))

        if cursor.rowcount == 0:
            connection.close()
            return jsonify({"error": "Server not found"}), 404
        
        connection.commit()
        connection.close()

        return jsonify({"message": "Server deleted successfully"}), 200


    @app.route("/servers/<int:id>", methods=['PATCH'])
    def patch_servers(id):
        data = request.get_json()
        error = patch_validation(data)
        
        if error:
            return error

        update_field = []
        update_values = []

        # CHANGED: ? to %s in all appended strings
        if "name" in data:
            update_field.append("name=%s")
            update_values.append(data["name"])

        if "ip" in data:
            update_field.append("ip=%s")
            update_values.append(data["ip"])

        if "os" in data:
            update_field.append("os=%s")
            update_values.append(data["os"])

        if not update_field:
            return jsonify({"error": "No fields provided"}), 400

        set_clause = ",".join(update_field)

        connection = get_connection()
        cursor = connection.cursor()
        update_values.append(id)

        # CHANGED: ? to %s in the WHERE clause
        query = f"""
        UPDATE servers
        SET {set_clause} 
        where id=%s 
        """
                
        cursor.execute(query, update_values)

        if cursor.rowcount == 0:
            connection.close()
            return jsonify({"error": "Server not found"}), 404

        connection.commit()
        connection.close()

        return jsonify({"message": "Server updated successfully"}), 200
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
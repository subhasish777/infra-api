# ============================================================
# VALIDATION
# ============================================================

def validate_server(data):
    if "name" not in data or "ip" not in data or "os" not in data:
        return "Missing data", 400
    #name validation 
    if data["name"] =="":
        return "Name cannot be empty", 400 
    if len(data["name"]) <=3:
        return "Server name should be more than 3 char", 400
    if data["ip"] =="":
        return "IP cannot be empty", 400
    if data["os"] == "":
        return "OS cannot be empty" , 400
    return None

#Server validation for PATCH
def patch_validation(data):

        if "name" in data:
            if data["name"]=="":
                return "Name cannot be empty", 400
            if len(data["name"])<=3:
                return "name should be more than 3 char",400
        if "ip" in data:
            if data["ip"]=="":
                return "IP cannot be empty" ,400
            
        if "os" in data:
            if data["os"]=="":
                return "OS cannot be empty",400
        return None

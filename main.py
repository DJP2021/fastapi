from fastapi import FastAPI
import functions as djp
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/v1")
def hello(apikey = None, prompt = None):

    if apikey is None:
        status = 0
        return {"status": status, "error": "No API-Key given"}
    else:
        validation = djp.validate_key(apikey)
        if validation == 1:
            if prompt is None:
                status = 0
                return {"status": status, "error": "No Prompt given"}
            validation = djp.check_permission(apikey, 1)
            if validation != -1:
                if validation != 0:
                    validation = djp.check_balance(apikey, 0.1)
                    if validation == 1:
                        status = 1
                        response = djp.openai_request(prompt)
                        return {"status": status, "response": response}
                    else:
                        status = 0
                        return {"status": status, "error": "Insufficent Balance"}
                else:
                    return {"status": status, "error": "Insufficient Account Tier"}
            else:
                status = 0
                return {"status": status, "error": "User has been blocked from using the API"}
        else:
            status = 0
            return {"status": status, "error": "Invalid Key"}

@app.get("/service/suspend")
def hello(userid = None, access = None):
    if access == None:
        status = 0
        return {"status": status, "error": "You have no permission to access this information"}
    else:
        permission = djp.validate_access(access, 3)
        if permission == -1:
            status = 0
            return {"status": status, "error": "Invalid Access Key"}
        else:
            if userid != None:
                validate = djp.get_user_rank(userid)
                if validate == 0:
                    key = djp.register_user(userid)
                    return key
                else:
                    status = 0
                    return {"status": status, "error": "User is already registered"}
            else:
                status = 0
                return {"status": status, "error": "Invalid Input"}

@app.get("/service/getbalance")
def balance(apikey = None):
    balance = djp.get_key_balance(apikey)
    if balance != "invalid":
        status = 1
        return {"status": status, "balance": balance}
    else:
        status = 0
        return {"status": status, "error": "Invalid Key"}
    
@app.get("/service/suspenduser")
def userinfo(userid = None, access = None):
    if access == None:
        status = 0
        return {"status": status, "error": "You have no permission to access this information"}
    else:
        permission = djp.validate_access(access, 5)
        if permission == -1:
            status = 0
            return {"status": status, "error": "Invalid Access Key"}
        elif permission == 0:
            status = 0
            return {"status": status, "error": "Insufficient Permission Level"}
    if userid == None:
        status = 0
        return {"status": status, "error": "No User given"}
    rank = djp.get_user_rank(str(userid))
    if rank == 0:
        status = 0
        return {"status": status, "error": "Invalid User"}
    djp.set_user_rank(str(userid), "Blocked")
    status = 1
    return {
  "status": status,
}
    
@app.get("/v1/number/rent")
def number_request(apikey = None):
    if apikey is None:
        status = 0
        return {"status": status, "error": "No API-Key given"}
    else:
        validation = djp.validate_key(apikey)
        if validation == 1:
            validation = djp.check_permission(apikey, 2)
            if validation != -1:
                if validation != 0:
                    validation = djp.check_balance(apikey, 2.5)
                    if validation == 1:
                        status = 1
                        number = djp.rent_number(apikey)
                        return {"status": status, "number": number}
                    else:
                        status = 0
                        return {"status": status, "error": "Insufficent Balance"}
                else:
                    if validation == "verify":
                        status = 0
                        return {"status": status, "error": "User is not verified"}
                    else:
                        status = 0
                        return {"status": status, "error": "Insufficient Account Tier"}
            else:
                status = 0
                return {"status": status, "error": "User has been blocked from using the API"}
        else:
            status = 0
            return {"status": status, "error": "Invalid Key"}  

@app.get("/v1/number/get")
def number_request(apikey = None):
    if apikey is None:
        status = 0
        return {"status": status, "error": "No API-Key given"}
    else:
        validation = djp.validate_key(apikey)
        if validation == 1:
            validation = djp.check_permission(apikey, 1)
            if validation == 1:
                smscode = djp.receival(apikey)
                if smscode != 0:    
                    status = 1
                    return {"status": status, "smscode": smscode}
                else:
                    status = -1
                    return {"status": status, "error": "Not arrived yet"}
            else:
                status = 0
                return {"status": status, "error": "User has been blocked from using the API"}
        else:
            status = 0
        return {"status": status, "error": "Invalid Key"}  

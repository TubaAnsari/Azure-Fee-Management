import azure.functions as func
import logging
import json
import pymssql
import os
import jwt

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetStudentFeeStatus")
def GetStudentFeeStatus(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GetStudentFeeStatus function processed a request.')

    student_id = req.params.get('StudentID')
    if not student_id:
        return func.HttpResponse(
            json.dumps({"error": "Please provide a StudentID parameter"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        student_id = int(student_id)
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "StudentID must be a number"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        server = 'server-fee-mgmt-ats.database.windows.net'
        database = 'db-FeeManagement'
        username = 'azureuser'
        password = os.environ.get('DB_PASSWORD')

        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Name, Course, TotalFee, PaidAmount, DueDate FROM Students WHERE StudentID = %s",
            (student_id,)
        )
        row = cursor.fetchone()

        if not row:
            return func.HttpResponse(
                json.dumps({"error": f"Student with ID {student_id} not found"}),
                status_code=404,
                mimetype="application/json"
            )

        name, course, total_fee, paid_amount, due_date = row
        total_fee = float(total_fee)
        paid_amount = float(paid_amount)

        from datetime import date
        if paid_amount >= total_fee:
            status = "Paid"
        elif paid_amount > 0:
            status = "Partially Paid"
        else:
            # Check if overdue
            if due_date < date.today():
                status = "Overdue"
            else:
                status = "Overdue"  # unpaid = overdue per assignment

        result = {
            "StudentID": student_id,
            "Name": name,
            "Course": course,
            "TotalFee": total_fee,
            "PaidAmount": paid_amount,
            "DueDate": str(due_date),
            "Status": status
        }

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        import traceback
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="UpdateStudentFee", methods=["POST"])
def UpdateStudentFee(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('UpdateStudentFee function processed a request.')

    auth_header = req.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            TENANT_ID = os.environ.get('AZURE_TENANT_ID')
            CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
            
            jwks_uri = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
            jwks_client = jwt.PyJWKClient(jwks_uri)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            
            decoded = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=CLIENT_ID
            )
            
            roles = decoded.get('roles', [])
            if 'FeeAdmin' not in roles:
                return func.HttpResponse(
                    json.dumps({"error": "Forbidden - FeeAdmin role required"}),
                    status_code=403,
                    mimetype="application/json"
                )
            logging.info(f"Azure AD auth successful for: {decoded.get('preferred_username')}")

        except Exception as e:
            logging.warning(f"Azure AD token invalid: {str(e)}, falling back to admin key")
            admin_key = req.headers.get('x-admin-key')
            if admin_key != os.environ.get('ADMIN_KEY'):
                return func.HttpResponse(
                    json.dumps({"error": "Unauthorized - Invalid token and invalid admin key"}),
                    status_code=401,
                    mimetype="application/json"
                )
    else:
        admin_key = req.headers.get('x-admin-key')
        if admin_key != os.environ.get('ADMIN_KEY'):
            return func.HttpResponse(
                json.dumps({"error": "Unauthorized - Provide Bearer token or admin key"}),
                status_code=401,
                mimetype="application/json"
            )

    try:
        req_body = req.get_json()
        student_id = req_body.get('StudentID')
        paid_amount = req_body.get('PaidAmount')

        if not student_id or paid_amount is None:
            return func.HttpResponse(
                json.dumps({"error": "Please provide StudentID and PaidAmount"}),
                status_code=400,
                mimetype="application/json"
            )

        server = 'server-fee-mgmt-ats.database.windows.net'
        database = 'db-FeeManagement'
        username = 'azureuser'
        password = os.environ.get('DB_PASSWORD')

        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Students SET PaidAmount = %s WHERE StudentID = %s",
            (float(paid_amount), int(student_id))
        )
        conn.commit()

        if cursor.rowcount == 0:
            return func.HttpResponse(
                json.dumps({"error": f"Student with ID {student_id} not found"}),
                status_code=404,
                mimetype="application/json"
            )

        return func.HttpResponse(
            json.dumps({
                "message": "Fee updated successfully",
                "StudentID": student_id,
                "NewPaidAmount": paid_amount
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        import traceback
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
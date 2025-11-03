import json
from flask import Request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_coverage(request: Request):
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for actual request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)
    if not request_json:
        return (jsonify({'error': 'Invalid or missing JSON body'}), 400, headers)

    procedure = request_json.get('procedure')
    plan_tier = request_json.get('plan_tier')

    if not plan_tier:
        return (jsonify({'error': 'Missing plan_tier'}), 400, headers)

    creds = service_account.Credentials.from_service_account_file(
        'service-account.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    sheet_id = '1FSPzWZ8s4w2XYyteiyMkOTQQlV7n03zbAjuB-x8Bxz4'
    range_name = 'healthplan_service_feed!A2:P'

    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    rows = result.get('values', [])

    plan_term = plan_tier.strip().lower()

    # 🔍 If procedure is provided, do a specific lookup
    if procedure:
        search_term = procedure.strip().lower()
        for row in rows:
            try:
                if len(row) < 16:
                    continue

                row_plan = row[1].strip().lower() if row[1] else ""
                row_service = row[5].strip().lower() if row[5] else ""
                is_covered = row[15].strip().lower() if row[15] else "no"

                if row_plan == plan_term and search_term in row_service:
                    limits = {
                        "monetary_limit_per_year": row[8] if len(row) > 8 else "NULL",
                        "monetary_limit_per_month": row[9] if len(row) > 9 else "NULL",
                        "coverage_day_in_a_year": row[11] if len(row) > 11 else "NULL",
                        "visit_limit_per_year": row[13] if len(row) > 13 else "NULL",
                        "session_limit_per_year": row[13] if len(row) > 13 else "NULL",
                        "coverage_remark": row[14] if len(row) > 14 else "NULL"
                    }
                    return (jsonify({'covered': is_covered == 'yes', 'limits': limits}), 200, headers)
            except Exception:
                continue

        return (jsonify({'covered': False, 'limit': 0}), 200, headers)

    # 📋 If no procedure is provided, return all covered procedures for the plan
    covered_procedures = []
    for row in rows:
        try:
            if len(row) < 16:
                continue

            row_plan = row[1].strip().lower() if row[1] else ""
            procedure_name = row[5].strip() if row[5] else ""
            is_covered = row[15].strip().lower() if row[15] else "no"
            remark = row[14].strip() if len(row) > 14 and row[14] else ""

            if row_plan == plan_term and is_covered == "yes":
                covered_procedures.append({
                    "procedure": procedure_name,
                    "coverage_remark": remark
                })
        except Exception:
            continue

    return (jsonify({'plan_tier': plan_tier, 'covered_procedures': covered_procedures}), 200, headers)
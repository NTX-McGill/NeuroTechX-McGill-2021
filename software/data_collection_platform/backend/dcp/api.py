from flask import Blueprint, request
import dateutil.parser
import pyodbc

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/anxious/start', methods=['POST'])
def anxiety_up():
    if not request.is_json:
        return {}, 400

    time = dateutil.parser.isoparse(request.json['time'])
    print(f"Anxious start at {time}")
    return {}, 200

@bp.route('/anxious/stop', methods=['POST'])
def anxiety_down():
    if not request.is_json:
        return {}, 400

    time = dateutil.parser.isoparse(request.json['time'])
    print(f"Anxious stop at {time}")
    return {}, 200

# DATABASE CONFIGURATION
server = '<server>.database.windows.net'
database = '<database>'
username = '<username>'
password = '<password>'   
driver= '{ODBC Driver 17 for SQL Server}'
table_name = ""

@bp.route('/videos', methods=['GET'])
def get_videos():
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            vid_array = []

            for row in cursor.execute("SELECT * FROM " + table_name):
                new_entry = {}
                new_entry["link"] = row.link
                new_entry["start"] = row.start
                new_entry["end"] = row.end
                new_entry["is_stressful"] = row.is_stressful
                new_entry["keywords"] = row.keywords
                new_entry["video_id"] = row.link.split('/')[-1]
                vid_array.append(new_entry)

            return vid_array, 200

            
        
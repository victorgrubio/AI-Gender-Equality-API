from flask import render_template, request, redirect, url_for
import requests

from web_client.gender_equality_client import app
from web_client.gender_equality_client import utils
from web_client.gender_equality_client.forms import SelectVideoForm

@app.route('/', methods=['GET'])
def index():
    form = SelectVideoForm()
    return render_template('index.html', title="Home", form=form)

@app.route('/process', methods=["POST"])
def process_video():
    video_path = request.form["video"]
    videos_proc = app.config["PROCESSED_VIDEOS"]
    if video_path in videos_proc:
        return redirect(url_for('get_results_from_csv', 
                                results = app.config["CSV_FILES"][videos_proc.index(video_path)]))
    detector_response = requests.post(
            "http://localhost:5000/v1/gender_equality/face_detection",
            headers={"Content-Type": "application/json"},
            json={ "video" : str(video_path) }
    ).json()
    print(detector_response)
    detector_id = detector_response["data"]["id"]
    return redirect(url_for('loading', detector_id=detector_id))

@app.route('/results', methods=["GET"])
def get_results():
    detector_id = request.args.get("detector_id")
    report = requests.get(
        "http://localhost:5000/v1/gender_equality/results",
        headers = {"Content-Type": "application/json"},
        json={"id": detector_id}
    ).json()
    results = report["data"]["results"]
    utils.save_results(results, app.config["UPLOAD_FOLDER"])
    processed_results = utils.process_results(results)
    return render_template('results.html',
                           title="Video Results",
                           gender_dict=processed_results["gender_percentage"],
                           speakers_dict=processed_results["speakers_percentage"],
                           time_table=processed_results["time_group"].to_html(
                                index=False,
                                justify="left",
                                classes=["table", "table-fixed", "table-borderless", "table-condensed", "table-hover"]))

@app.route("/loading" , methods=["GET"])
def loading():
    detector_id = request.args.get("detector_id")
    return render_template("loading.html", detector_id=detector_id)


@app.route("/results_csv" , methods=["GET"])
def get_results_from_csv():
    results_name = request.args.get("results")
    results = utils.load_dataframe_from_server(app.config["UPLOAD_FOLDER"], results_name)
    processed_results = utils.process_results(results)
    return render_template('results.html',
                           title="Video Results",
                           gender_dict=processed_results["gender_percentage"],
                           speakers_dict=processed_results["speakers_percentage"],
                           time_table=processed_results["time_group"].to_html(
                                index=False,
                                justify="left",
                                classes=["table", "table-fixed", "table-borderless", "table-condensed", "table-hover"]))

    
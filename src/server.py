from flask import Flask, render_template, jsonify
from flask import request
from flask import send_file
from .main import Main
import threading

class Server():
    def __init__(self, main) -> None:
        
        app =  Flask(__name__)

        @app.route("/")
        def home():
            return 'Hello, form Docker!'
        
        @app.route("/status/")
        def status():
            return jsonify({
                "busy": Main().busy
            })
            
        @app.route('/download/')
        def downloadFile():
            file_name = request.args.get('file-name')
            path = f"../{file_name}"
            return send_file(path, as_attachment=True)
        
        @app.route("/update/")
        def update():
            threading.Thread(target=Main().do_progress(force=True)).start()
            return "<h1>started</h1>"

        app.run(host='0.0.0.0')


        
        
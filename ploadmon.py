from flask import *
from engine import *

app = Flask(__name__)

srvos = ServerOS()
cpu = ServerCPU()
memc = MemChart()
corc = CoresChart()


@app.route('/')
def main():
    return render_template("main.html", cpu=cpu.getcpuinfo(), os=srvos.getserveros())


@app.route('/stats')
def stats():
    srvstat = ServerStatus()

    return jsonify({"memchart": memc.getchart(),
                    "corechart": corc.getchart(),
                    "serverstatus": srvstat.getstatstable(),
                    "memdognut": Dognut("memdognut", srvstat.getmemload()).chart,
                    "hdddognut": Dognut("hdddognut", srvstat.gethddload()).chart})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

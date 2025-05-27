from flask import Flask, render_template, request, redirect, url_for
from container_manager import ContainerManager

app = Flask(__name__)
manager = ContainerManager()

@app.route('/')
def index():
    containers = manager.containers
    mem_state = manager.get_memory_state()  # call method to get current memory state
    page_fault_log = manager.get_page_fault_log()  # correct, call method to get logs
    return render_template('index.html', containers=containers, mem_state=mem_state, page_fault_log=page_fault_log)

@app.route('/create', methods=['POST'])
def create_container():
    container_id = request.form['container_id']
    memory_kb = int(request.form['memory_kb'])
    manager.create_container(container_id, memory_kb)
    return redirect(url_for('index'))

@app.route('/allocate', methods=['POST'])
def allocate_memory():
    container_id = request.form['container_id']
    page_number = int(request.form['page_number'])
    algorithm = request.form['algorithm']
    manager.allocate_memory(container_id, page_number, algorithm)
    return redirect(url_for('index'))

@app.route('/terminate/<container_id>')
def terminate_container(container_id):
    manager.terminate_container(container_id)
    return redirect(url_for('index'))

@app.route('/start/<cid>')
def start_container(cid):
    manager.start_container(cid)
    return redirect(url_for('index'))

@app.route('/stop/<cid>')
def stop_container(cid):
    manager.stop_container(cid)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

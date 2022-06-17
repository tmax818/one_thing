from flask import Flask, render_template, request, redirect

app = Flask(__name__)

from thing import Thing

# ! CREATE

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create():
    print(request.form)
    Thing.save(request.form)
    return redirect('/')

# ! READ / RETRIEVE

@app.route('/')
@app.route('/things')
def index():
    return render_template('index.html', things = Thing.get_all())

@app.route('/show/<int:id>')
def show(id):
    data = {'id': id}
    return render_template('show.html', thing = Thing.get_one(data))

# ! UPDATE

@app.route('/edit/<int:id>')
def edit(id):
    data = {'id': id}
    return render_template('edit.html', thing = Thing.get_one(data) )

@app.route('/update', methods=['post'])
def update():
    print(request.form)
    Thing.update(request.form)
    return redirect('/')

# ! DELETE

@app.route('/destroy/<int:id>')
def destroy(id):
    data = {'id': id}
    Thing.destroy(data)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
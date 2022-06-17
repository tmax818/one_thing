# one_thing

- create virtual environment:
```bash
pipenv install flask pymysql
```
- activate virtual environment:
```bash
pipenv shell
```
- start server
```bash
python server.py
```
- go to the root of the application [localhost](http://localhost:5000/)
- This will cause this route to activate its function:

```py
@app.route('/')
@app.route('/things')
def index():
    return render_template('index.html', things = Thing.get_all())
```

- This function does two things:
    
1. it calls the class method: `Things.get_all()`

```py
   @classmethod
    def get_all(cls):
        query = "SELECT * FROM things;"
        results = connectToMySQL(DATABASE).query_db(query)
        things = []
        for thing in results:
            things.append( Thing(thing) )
        return things
```

2. it renders the [template](templates/index.html) and passes the `things` variable to it for use in jinja tags.

- clicking the `new` link in [index.html](templates/index.html) will cause this route to activeate its function:

```py
@app.route('/new')
def new():
    return render_template('new.html')
```
- the above method renderts the [template](templates/index.html) that contains the form for a new thing:

```html
    <form action="/create" method='post'>
        <input type="text" name="property">
        <input type="submit" value="submit">
    </form>
```
- the following route handles that form's data:

```py
@app.route('/create', methods=['POST'])
def create():
    print(request.form) #=> prints form data for debugging
    Thing.save(request.form) #=> saves form data to the database
    return redirect('/') #=> redirects to the root route
```

- the following class method saves the from data to the database and is invoked above as `Thing.save(request.form)`

```py
    @classmethod
    def save(cls, data):
        query = "INSERT INTO things (property) VALUES (%(property)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
```
- notice that the `name` attribute below:

```html
<input type="text" name="property">
```
matches the value to be inserted in the query statement and the column name in the database:

```py
    query = "INSERT INTO things (property) VALUES (%(property)s)"
```

- The `get_one()` class method can be used for both the `show` and the `edit` route.

```py
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM things WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return Thing(result[0])
```
- The value returned from the database will be a list of dictionaries. The expression `result[0]` accesses the first element of the list(i.e. the first and only dictionary in this case). The method returns an instance of the `Thing` class.

- The following route:

```py
@app.route('/edit/<int:id>')
def edit(id):
    data = {'id': id}
    return render_template('edit.html', thing = Thing.get_one(data) )
```
Will call the `get_one()` method and send the object returned to the [template](templates/edit.html). The data from the `thing` object can then be used to populate the form:

```html
    <form action="/update" method='post'>
        <input type="hidden" name="id" value="{{thing.id}}">
        <input type="text" name="property" id="" value="{{thing.property}}">
        <input type="submit" value="submit">
    </form>
```
The `edit` form is almost identical to the `new` form. However, we need to specify which item in the database to update. We use a hidden input to pass the item's id:

```html
<input type="hidden" name="id" value="{{thing.id}}">
```

- The following route handles the data from the edit form:

```py
@app.route('/update', methods=['post'])
def update():
    print(request.form)
    Thing.update(request.form)
    return redirect('/')
```

- The same thing happens for the `show` route:

```py
@app.route('/show/<int:id>')
def show(id):
    data = {'id': id}
    return render_template('show.html', thing = Thing.get_one(data))
```

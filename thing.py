from mysqlconnection import connectToMySQL

DATABASE = 'one_thing'

class Thing:
    def __init__( self , data ):
        self.id = data['id']
        self.property = data['property']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO things (property) VALUES (%(property)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! READ / RETRIEVE ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM things;"
        results = connectToMySQL(DATABASE).query_db(query)
        things = []
        for thing in results:
            things.append( Thing(thing) )
        return things

    
    # ! READ / RETRIEVE ONE
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM things WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return Thing(result[0])
        
    # ! DELETE
    @classmethod
    def update(cls, data):
        query = "UPDATE things SET property=%(property)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM things WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        
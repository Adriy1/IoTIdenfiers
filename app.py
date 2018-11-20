# from flask import Flask, request, jsonify, abort
#
# app = Flask(__name__)
# api = Api(app)
#
# class HelloWorld(Resource):#     def get(self):
#         return {'hello': 'world'}
#
# # class getFile(Resource):
# #     def get(self):
# #         return {'hello': 'world'}
# #
# # class getFiles(Resource):
# #     def get(self):
# #         return {'hello': 'world'}
#
# class encodeFile(Resource):
#     def post(self,message,file):
#         return {'hello': 'world'}
#
# class decodeFile(Resource):
#     def post(self,file):
#         return {'hello': 'world'}
#
#
# api.add_resource(HelloWorld, '/')
# # api.add_resource(getFile, '/file/<int:todo_id>')
# # api.add_resource(getFiles, '/files')
# api.add_resource(encodeFile, '/encode')
# api.add_resource(decodeFile, '/decode')
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask
import writer
app = Flask(__name__)

@app.route("/")
def hello():
    writer.openAndHide()
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)

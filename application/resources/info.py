from flask_restful import Resource


class Info(Resource):
    def get(self):
        return {
            'title': 'Fest Management REST API',
            'version': '0.1',
            'author': 'Ahmed Sadman Muhib (Samyo), CSE 16, IUT'
        }

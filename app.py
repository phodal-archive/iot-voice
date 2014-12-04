#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
import jieba
jieba.initialize()
jieba.set_dictionary('data/dict.txt.small')

app = Flask(__name__)
api = Api(app)

COMMAND = {}


def abort_if_todo_doesnt_exist(cmd_id):
    if cmd_id not in COMMAND:
        abort(404, message="Command {} doesn't exist".format(cmd_id))

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)

#   show a single todo item and lets you delete them
class Todo(Resource):
    def participle(self,data):
        jieba_cut = jieba.cut(data, cut_all=True)
        return jieba_cut

    def get(self, cmd_id):
        abort_if_todo_doesnt_exist(cmd_id)
        return COMMAND[cmd_id]

    def delete(self, cmd_id):
        abort_if_todo_doesnt_exist(cmd_id)
        del COMMAND[cmd_id]
        return '', 204

    def put(self, cmd_id):
        cmd_id = 'cmd%d' % (len(COMMAND) + 1)
        jieba_cut = self.participle(request.form['data'])
        print "".join(jieba_cut)
        task = {'task': str(jieba_cut)}
        COMMAND[cmd_id] = {'taks': str(jieba_cut)}
        return task, 201

# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return COMMAND

    def post(self):
        args = parser.parse_args()
        cmd_id = 'cmd%d' % (len(COMMAND) + 1)
        COMMAND[cmd_id] = {'task': args['task']}
        return COMMAND[cmd_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/command')
api.add_resource(Todo, '/command/<string:cmd_id>')


if __name__ == '__main__':
    app.run(debug=True)
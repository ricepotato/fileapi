# -*- coding: utf-8 -*-

import os
import magic
import shutil
from flask import jsonify
from flask_restful import Resource


class NoContentException(Exception):
    pass


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoContentException:
            return "", 204

    return wrapper


class Files(Resource):
    def __init__(self, **kwargs):
        self.aliases = {
            "ricepotato": {"path": "/home/ricepotato", "methods": ["get"]},
            "incomming": {
                "path": "/home/ricepotato/incomming",
                "methods": ["get", "delete"],
            },
        }

    def _get_real_path(self, path):
        root_path = path.split("/")[0]
        if root_path not in self.aliases:
            raise NoContentException(root_path)

        self.methods = self.aliases[root_path].get("methods", ["get"])
        self.root_path = os.path.abspath(self.aliases[root_path]["path"])
        real_path = path.replace(root_path, self.aliases[root_path]["path"])
        if not os.path.exists(real_path):
            raise NoContentException(real_path)
        return real_path

    @handle_error
    def get(self, path):
        real_path = self._get_real_path(path)

        files = []
        dirs = []
        res = {
            "path": path,
            "real_path": real_path,
            "sub_dirs": dirs,
            "files": files,
        }

        if os.path.isdir(real_path):
            listdir = os.listdir(real_path)
            for item in listdir[:50]:
                target = os.path.join(real_path, item)
                if os.path.isdir(target):
                    dirs.append(item)
                else:
                    files.append(item)
        else:
            res["filetype"] = magic.from_file(real_path)
            res["size"] = os.path.getsize(real_path)

        return jsonify(res)

    def delete(self, path):
        real_path = self._get_real_path(path)
        if "delete" not in self.methods:
            return (
                {
                    "action": "delete",
                    "msg": "delete not available.",
                    "real_path": real_path,
                },
                400,
            )
        if os.path.abspath(real_path) == self.root_path:
            return (
                {
                    "action": "delete",
                    "msg": "Can't delete root path.",
                    "real_path": real_path,
                },
                400,
            )
        if os.path.isfile(real_path):
            os.remove(real_path)
        else:
            shutil.rmtree(real_path)
        return jsonify(
            {
                "action": "delete",
                "msg": "OK",
                "abs_path": os.path.abspath(real_path),
                "real_path": real_path,
            }
        )

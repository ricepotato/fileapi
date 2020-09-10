# -*- coding: utf-8 -*-

from waitress import serve
from app.main import app

serve(app, host="0.0.0.0", port=8080)

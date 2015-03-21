# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required

user_controller = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@user_controller.route("/")
@login_required
def members():
    return render_template("users/members.html")


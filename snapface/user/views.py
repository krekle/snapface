# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask.ext.login import login_required
import subprocess
from snapface.bots.models import Bot

user_controller = Blueprint("user", __name__, url_prefix='/users',
                            static_folder="../static")


@user_controller.route("/")
@login_required
def members():
    return render_template("users/members.html")


@user_controller.route("/bots/")
@login_required
def bots():
    bots = subprocess.Popen('screen -ls | grep snapface', stdout=subprocess.PIPE, shell=True)
    (output, err) = bots.communicate()
    return render_template("users/bots.html", output=output)


@user_controller.route("/test/")
@login_required
def test():
    b = Bot.query.all()[0]
    b.start_bot()
    return render_template("users/members.html")
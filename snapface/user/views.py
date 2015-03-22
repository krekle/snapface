# -*- coding: utf-8 -*-

import subprocess

from flask import Blueprint, render_template, flash, url_for, redirect
from flask.ext.login import login_required
from snapface.bots.models import Bot


user_controller = Blueprint("user", __name__, url_prefix='/users',
                            static_folder="../static")


@user_controller.route("/meh/")
@login_required
def members():
    return render_template("users/members.html")


@user_controller.route("/")
@login_required
def bots():
    # Crete new bot form
    # bot_form = model_form(Bot, Form)

    # Get the running bots
    bots = subprocess.Popen('screen -ls | grep snapface', stdout=subprocess.PIPE, shell=True)
    (output, err) = bots.communicate()
    running_bots = []
    if output:
        print 'got output'
        screen_bots = output.rstrip().split('\n')
        print screen_bots
        for bots in screen_bots:
            bots_pid = bots.replace('\t', '').split('.')[0]
            running_bots.append(Bot.query.filter(Bot.bot_pid == str(int(bots_pid) - 1)).first())
    # Get all bots
    all_boots = Bot.query.all()

    disabled_bots = list(set(all_boots) - set(running_bots))

    return render_template("users/bots.html", running_bots=running_bots, disabled_bots=disabled_bots)


@user_controller.route("/start/<name>")
@login_required
def start(name):
    if name:
        start_this = Bot.query.filter(Bot.username == name).first()
        if start_this:
            start_this.start_bot()
        else:
            flash('Error starting bot', 'warning')
    flash('Input error, missing name', 'warning')
    return redirect(url_for('user.bots'))


@user_controller.route("/stop/<name>")
@login_required
def stop(name):
    if name:
        stop_this = Bot.query.filter(Bot.username == name).first()
        if stop_this:
            stop_this.stop_bot()
        else:
            flash('Error starting bot', 'warning')
    flash('Input error, missing name', 'warning')
    return redirect(url_for('user.bots'))

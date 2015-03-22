# -*- coding: utf-8 -*-

import subprocess

from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask.ext.login import login_required
from snapface.bots.models import Bot
# from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from snapface.extensions import db


user_controller = Blueprint("user", __name__, url_prefix='/users',
                            static_folder="../static")

BotForm = model_form(Bot, base_class=Form, exclude=['friends', 'bot_pid'])


@user_controller.route("/create/", methods=['GET', 'POST'])
@login_required
def create():
    form = BotForm(request.form)
    print 'at create'
    if form:
        bot = Bot()
        form.populate_obj(bot)
        db.session.add(bot)
        db.session.commit()
        flash('Bot created!', 'info')
    else:
        flash('Something went wrong!', 'error')

    return redirect(url_for('.bots'))


@user_controller.route("/")
@login_required
def bots():
    # Crete new bot form
    bot_form = BotForm()

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

    return render_template("users/bots.html", running_bots=running_bots, disabled_bots=disabled_bots, botform=bot_form)


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

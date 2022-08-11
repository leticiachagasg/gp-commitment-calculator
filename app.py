import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.template_filter()
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

@app.route("/", methods=["GET", "POST"])
def index():

    result = 0

    if request.method == "POST":

        gp_percentage = request.form.get("gp_percentage")
        fund_size = request.form.get("fund_size")

        if not gp_percentage or not fund_size:
           return redirect("/")

        else:

            #make fund_size all numbers
            for char in fund_size:
                if char != "." and not char.isnumeric():
                    fund_size = fund_size.replace(char, '')

            #make gp_percentage all numbers
            for char in gp_percentage:
                if not char.isnumeric():
                    gp_percentage = gp_percentage.replace(char, '')

            if not fund_size.isnumeric() or not gp_percentage.isnumeric():
                return redirect("/")

            fund_size = float(fund_size)
            gp_percentage = float(gp_percentage)/100
            lp_percentage = 1 - gp_percentage


            # Get formula to round + show 2 decimals
            result = (fund_size * gp_percentage) / lp_percentage

        return render_template("index.html", result=result)

    else:

        return render_template("index.html", result=result)



from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    states = get_state_options()
    #print(states)
    return render_template('home.html', state_options=states)

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    counties = get_county_options()
    state = request.args.get('state')
    county = county_most_under_18(state)
    foreign = county_most_foreign(state)
    poverty = county_least_poverty(state)
    veterans = county_most_veterans(state)
    fact = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county + "."
    fact2 = "In " + state + ", the county with the highest percentage of foreign born individuals is " + foreign + "."
    fact3 = "In " + state + ", the county with the lowest percentage of people below the poverty level is " + poverty + "."
    fact4 = "In " + state + ", the county with the highest amount of veterans is " + veterans + "."

    return render_template('home.html', state_options=states, county_options=counties, funFact=fact, funFact2=fact2, funFact3=fact3, funFact4=fact4)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_county_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    county=[]
    for c in counties:
        if c["County"] not in county:
            county.append(c["County"])
    options=""
    for s in county:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county
    
def county_most_foreign(state):
    """Return the name of a county in the given state with the highest percent of foreign born."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Miscellaneous"]["Foreign Born"] > highest:
                highest = c["Miscellaneous"]["Foreign Born"]
                county = c["County"]
    return county
    
def county_least_poverty(state):
    """Return the name of a county in the given state with the least percent of poverty."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=100
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Income"]["Persons Below Poverty Level"] < highest:
                highest = c["Income"]["Persons Below Poverty Level"]
                county = c["County"]
    return county
    
def county_most_veterans(state):
    """Return the name of a county in the given state with the most amount of veterans."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Miscellaneous"]["Veterans"] > highest:
                highest = c["Miscellaneous"]["Veterans"]
                county = c["County"]
    return county


def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production

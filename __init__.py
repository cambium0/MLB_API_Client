from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap5
import statsapi
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, URLField
from wtforms.validators import DataRequired, URL
import json


FORMATTED = ['boxscore', 'game_highlights', 'game_pace', 'game_scoring_plays', 'last_game', 'league_leaders',
             'linescore', 'next_game', 'player_stats', 'roster', 'standings', 'team_leaders']
app = Flask(__name__)
bootstrap = Bootstrap5(app)
all_cafes = {}
app.secret_key = "38dkkd8lk3009328dld88ldk3294874l"


@app.route('/', methods=['GET', 'POST'])
def home():
    data = ""
    textform = ""
    if request.method == 'POST':
        query_params = {}
        form = request.form.to_dict(flat=False)
        for item in form:
            query_params[item] = form[item][0]
        query_p1 = f"statsapi.{query_params['function']}("
        print(f"query_params is {query_params}")
        for key in query_params.keys():
            if key != 'function':
                if form[key][0] != "":
                    query_p1 += f"{key}={form[key][0]},"
        query_p2 = query_p1 + ")"
        print(f"{query_p2}")
        result = eval(query_p2)
        print(f"result is {result}")
        if query_params['function'] in FORMATTED:
            data = result
            textform = 'y'
            data_links = ""
            link_flag = False
            link = ""
            a_link_pre = '<a href="'
            a_link_post = '">a link</a>'
            for i in range(0, len(str(data))):
                if i <= len(str(data)) - 8 and data[i:i+8] == 'https://':
                    link_flag = True
                    # link = data[i]

                if link_flag:
                    if data[i] == '\n' or data[i] == ' ':
                        link_flag = False
                        hyper_link = a_link_pre + link + a_link_post
                        data_links += hyper_link
                        data_links = data_links + data[i]
                        link = ""
                    else:
                        link += data[i]
                else:
                    try:
                        data_links = data_links + str(data)[i]
                    except IndexError:
                        continue
            data = data_links
        else:
            data = result
            textform = 'n'
    return render_template('index.html', istext=textform, data=data)


@app.route('/meta', methods=['POST'])
def meta_queries():
    textform = 'y'  # list of dictionaries
    form = request.form.to_dict(flat=False)
    results = statsapi.meta(form['meta_type'][0])
    data = json.dumps(results, indent=2)
    # print(f"param_name is {param_name}")
    # result = eval('statsapi.meta("' + param_name + '")')

    return render_template('index.html', istext=textform, data=data)


@app.route('/notes', methods=['POST'])
def query_notes():
    textform = 'y'
    form = request.form.to_dict(flat=False)
    query_term = form['endpoint_name'][0]
    print(f"query_term is {query_term}")
    query = 'statsapi.notes("' + query_term + '")'
    print(f"query is {query}")
    result = eval(query)
    print(f"result is {result}")
    return render_template('index.html', istext=textform, data=result)


@app.route('/raw', methods=['POST'])
def raw_queries():
    textform = 'y'
    form = request.form.to_dict(flat=False)
    query_arg = form['raw_query'][0]
    query = "statsapi.get('" + query_arg + "')"
    result = eval(query)
    return render_template('index.html', istext=textform, data=result)


if __name__ == "__main__":
    app.run(debug=True)

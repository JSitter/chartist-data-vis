from functools import reduce
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Attach pandas datafram to python app
app.df = pd.read_csv('data.csv', skiprows=1)
app.df.columns = ['month', 'diet', 'gym', 'finance']

@app.route('/', methods=['GET'])
def index():
  '''
  Get Main Root
  '''
  return render_template("index.html"), 200

@app.route('/time_series', methods=['GET'])
def getData():
  '''
  Get Chart Data
  '''

  year_range = [int(year) for year in request.args.getlist('n')]
  view_cols = request.args.getlist('m')

  # Generate List of all Years
  years_list = [str(year) for year in range(min(year_range), max(year_range)+1)]

  user_months = reduce(
    lambda a, b: a | b, (app.df['month'].str.contains(year) for year in years_list)
  )

  # Create New dataframe
  new_df = app.df[user_months][['month']+view_cols]

  # Convert date strings to date objects
  new_df['month'] = pd.to_datetime(new_df['month'])
  new_df = new_df.sort_values(by=["month"])

  # Return jsonified dataframe
  return new_df.to_json(), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)

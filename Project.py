import pandas as pd
def main_data():
    crime_df = pd.read_csv(r'C:\Users\swati.ah.kumari\demos\Documents\Assignment-2_CrimeData\crime-data.csv')
    crime_df['year'] = crime_df['Month'].map(lambda x: '20'+x.split('-')[1])
    crime_df['total_crimes'] = crime_df['Murders'] + crime_df['Thefts'] + crime_df['Eveteasing']
    # data=crime_df.groupby(['year', 'City']).agg({'total_crimes': 'sum'}).reset_index().sort_values(by=['year', 'total_crimes'], ascending = False)
    crime_df['Months'] = crime_df['Month'].map(lambda x: (x.split('-')[0]))
    return crime_df
    


from flask import Flask, jsonify, request,redirect,render_template,url_for
 
 
app = Flask(__name__)




@app.route("/")

def home():

    return render_template("home.html")




####-SafestCityByYear


@app.route('/safestCityByYear/<year>', methods=['POST', 'GET'])
def safestCityByYear(year):
    crime_df=main_data()
    Yearwise_data= crime_df.groupby(["year","City"]).agg({'total_crimes': "sum"}).reset_index().sort_values(by=["year","total_crimes"], ascending = True)
    Yearwise_data2= Yearwise_data.groupby('year').get_group(year).reset_index().sort_values(by=["total_crimes"])
    return (jsonify(Year = year,city = Yearwise_data2["City"][0]))

@app.route('/safestCityByYear', methods=['POST', 'GET'])
def safestcity():
    if request.method == 'POST':
        user = request.form['Year']
        return redirect(url_for('safestCityByYear', year=user))
    return(render_template('safestCityByYear.html'))









####--UnsafestCityByYear

@app.route('/UnsafestCityByYear/<year>', methods=['POST', 'GET'])
def UnsafestCityByYear(year):
    crime_df=main_data()
    a = crime_df.groupby(["year","City"]).agg({'total_crimes': "sum"}).reset_index().sort_values(by=["year","total_crimes"], ascending = False)
    b = a.groupby('year').get_group(year).reset_index().sort_values(by=["total_crimes"])
    return (jsonify(Year = year,city = b["City"][0]))

@app.route('/UnsafestCityByYear', methods=['POST', 'GET'])
def unsafestcity():
    if request.method == 'POST':
        user = request.form['Year']
        return redirect(url_for('UnsafestCityByYear', year=user))
    return(render_template('UnsafestCityByYear.html'))










####--UnsafestMonthByCity


@app.route('/UnsafestMonthbyCity/<city>', methods=['POST', 'GET'])
def UnsafestMonthByCity(city):
    crime_df=main_data()
    city=city.capitalize()
    grp=crime_df.groupby(['City','Months']).agg({'total_crimes': 'sum'}).reset_index().sort_values(by=['total_crimes', 'City'], ascending = False)
    citydata=grp.groupby('City').get_group(city) .reset_index()
    return jsonify(UnsafestMonth=citydata['Months'][0],totalcrimes=int(citydata['total_crimes'][0]))

@app.route('/UnsafestMonthByCity', methods=['POST', 'GET'])
def UnsafestMonth():
    if request.method == 'POST':
        user = request.form['City']
        return redirect(url_for('UnsafestMonthByCity', city=user))
    return(render_template('UnsafestMonthByCity.html'))








# ####--SafestMonthByCity

@app.route('/safestMonthByCity/<city>', methods=['POST', 'GET'])
def safestMonthByCity(city):
    crime_df=main_data()
    city=city.capitalize()
    grp=crime_df.groupby(['City','Months']).agg({'total_crimes': 'sum'}).reset_index().sort_values(by=['total_crimes', 'City'], ascending = True)
    citydata=grp.groupby('City').get_group(city) .reset_index()
    return jsonify(UnsafestMonth=citydata['Months'][0],totalcrimes=int(citydata['total_crimes'][0]))

@app.route('/safestMonthByCity', methods=['POST', 'GET'])
def safestMonth():
    if request.method == 'POST':
        user = request.form['City']
        return redirect(url_for('safestMonthByCity', city=user))
    return(render_template('safestMonthByCity.html'))










# ####--MostCommittedCrimeByCityandYear

@app.route('/getMostCommittedCrimeByCityandYear/<city>/<year>', methods=['POST', 'GET'])
def getMostCommittedCrimeByCityandYear(city,year):
      crime_df=main_data()
      city=city.capitalize()
      grp=crime_df.groupby('year').get_group(year)
      data=grp.groupby(['year','City']).agg({'Murders': 'sum','Thefts':'sum','Eveteasing':'sum'}).reset_index().sort_values(by=['year','Murders','Thefts','Eveteasing'], ascending = False).reset_index()
      dta=data.groupby('City').get_group(city).reset_index()
      maxdta=max((dta['Murders'][0],'Murders'),(dta["Thefts"][0],'thefts'),(dta['Eveteasing'][0],'Eveteasing'))
      return jsonify(crime=maxdta[1],numberofcrime=int(maxdta[0]))


@app.route('/getMostCommittedCrimeByCityandYear', methods=['POST', 'GET'])
def mostcommitedcrime():
    if request.method == 'POST':
        City = request.form['City']
        Year=request.form['Year']
        return redirect(url_for('getMostCommittedCrimeByCityandYear', city=City,year=Year))
    return(render_template('getMostCommittedCrimeByCityandYear.html'))










# ####--LeastCommittedCrimeByCityandYear

@app.route('/getLeastCommittedCrimeByCityandYear/<city>/<year>', methods=['POST', 'GET'])
def getLeastCommittedCrimeByCityandYear(city,year):
      crime_df=main_data()
      city=city.capitalize()
      grp=crime_df.groupby('year').get_group(year)
      data=grp.groupby(['year','City']).agg({'Murders': 'sum','Thefts':'sum','Eveteasing':'sum'}).reset_index().sort_values(by=['year','Murders','Thefts','Eveteasing'], ascending = False).reset_index()
      dta=data.groupby('City').get_group(city).reset_index()
      maxdta=min((dta['Murders'][0],'Murders'),(dta["Thefts"][0],'thefts'),(dta['Eveteasing'][0],'Eveteasing'))
      return jsonify(crime=maxdta[1],numberofcrime=int(maxdta[0]))


@app.route('/getLeastCommittedCrimeByCityandYear', methods=['POST', 'GET'])
def leastcommitedcrime():
    if request.method == 'POST':
        City = request.form['City']
        Year=request.form['Year']
        return redirect(url_for('getLeastCommittedCrimeByCityandYear', city=City,year=Year))
    return(render_template('getLeastCommittedCrimeByCityandYear.html'))










# ####-- getLeastCommittedCrimeByCityAndMonth

@app.route('/getLeastCommittedCrimeByCityandMonth/<`city>/<month>', methods=['POST', 'GET'])
def getLeastCommittedCrimeByCityandMonth(city,month):
      crime_df=main_data()
      city=city.capitalize()
      month=month.capitalize()
      grp=crime_df.groupby('City').get_group(city)
      data=grp.groupby(['Months','City']).agg({'Murders': 'sum','Thefts':'sum','Eveteasing':'sum'}).reset_index().sort_values(by=['Months','Murders','Thefts','Eveteasing'], ascending = False).reset_index()
      dta=data.groupby('Months').get_group(month).reset_index()
      monthwisedta=min((dta['Murders'][0],'Murders'),(dta['Thefts'][0],'Thefts'),(dta['Eveteasing'][0],'Eveteasing'))
      return jsonify(crime=monthwisedta[1],numberofcrime=int(monthwisedta[0]))

@app.route('/getLeastCommittedCrimeByCityandMonth', methods=['POST', 'GET'])
def leastcommitedcrimeMonth():
    if request.method == 'POST':
        City = request.form['City']
        Month=request.form['Month']
        return redirect(url_for('getLeastCommittedCrimeByCityandMonth', city=City,month=Month))
    return(render_template('getLeastCommittedCrimeByCityandMonth.html'))






if __name__ == '__main__':
    app.run(debug=True)
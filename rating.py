from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset into a DataFrame
df = pd.read_csv('modified_dataset.csv')

@app.route('/rating', methods=['GET', 'POST'])
def home():
    average_rating = None
    city = None
    
    if request.method == 'POST':
        city = request.form.get('City')
        
        # Filter the DataFrame by the city
        city_data = df[df['City'].str.lower() == city.lower()]
        
        if not city_data.empty:
            # Calculate the average rating
            average_rating = city_data['Rating'].mean()
    
    return render_template('rating.html', average_rating=average_rating, city=city)

if __name__ == '__main__':
    app.run(debug=True)

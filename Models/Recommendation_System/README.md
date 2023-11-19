# Property Recomendations sytem
- Content based Recommendation Syatem


## Important factors that are highlighted:

#### Dataset from:
Latest_maintable_copy 
Latest_maintable_risk_rating_score_copy (result from Risk_Rating_Model)

#### Preprocessed and Model ready dataset are :
Categories used in Algorithm : zpid,city,homeType,homeStatus,lotAreaUnit,state,newConstructionType,Average Risk Level,bathrooms,bedrooms,livingArea,lotAreaValue,price,rentZestimate,zipcode,taxAssessedValue,datePriceChanged,priceChange,Average Score,investment_risk

Property Type: The type of property, such as residential, single family, multifamily, commercial, land, etc.
Location: The geographic location of the property, including city, state, neighborhood, and ZIP code.
Property Size: The size of the property in terms of square footage or number of rooms and bedrooms.
Property Description: A textual description of the property, which can be analyzed using natural language processing techniques.
Price: The price of the property or the investment amount required.
Property Age: The age of the property, if available.
Property Condition: The condition of the property, whether it's new, renovated, or needs repairs.
Property Category: Categorization of properties based on specific criteria, such as luxury, budget, high-risk, low-risk, etc.

####
you can modify no. of required recommended properties in model.py

### How to Run the project

- Clone this repository in your system. 
`
git clone https://github.com/Shoptaki/real-estate-ai-be.git
`
- Install all the libraries mentioned in the 'requirements.txt' inside Models/Recommendation_System folder.
`
pip install -r reqyirements.txt
`
- Run all cell in RE_DataCleaning python notebook and get the processed clean dataset to use further (auto create dataset 'final_data.csv)

- Run model.py in Terminal
- Result will show 10 properties id. 
    (You can fetch details of that id and display for recommendation while working on frontend)
  
- ToDo: Deploy the model with any Restful API (Django, etc)
  


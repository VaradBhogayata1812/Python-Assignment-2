# Importing necessary libraries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

def loadingandCorrecting(filepath):
    data = pd.read_csv(filepath)
    # Correcting column entries
    data['Serial'] = data['Serial'].str.split('.').str[0]
    # Removing the prefix set in Type column and Code column
    data['Type'] = data['Type'].str.replace('Thingful.Connectors.GROWSensors.', '')
    data['Code'] = data['Code'].str.replace('Grow.Thingful.Sensors_', '')
    return data

def filtering(data):
    # Dropping zero value because it didn't restrict in our bounding box
    data = data.drop(data[(data['Latitude'] == 0) & (data['Longitude'] == 0)].index)
    # Deleting duplicate entries
    data = data.drop_duplicates(subset=['Latitude', 'Longitude'])
    return data

def plotData(image, data, x_col, y_col, output_filename):
    # Removing all the values that are outside bounding box
    data = data[(data['Latitude'].between(50.681, 57.985)) & (data['Longitude'].between(-10.592, 1.6848))]
    plt.imshow(image, extent=[-10.592, 1.6848, 50.681, 57.985], aspect='auto', label='Growth Locations')
    plt.scatter(data[x_col], data[y_col], color="red", s=10, label='Growth Locations')
    plt.title('Plotting Grow Data'); plt.xlabel('East-West'); plt.ylabel('North-South'); plt.legend(loc = "upper left")
    plt.savefig(output_filename)
    plt.clf()

def pieChart(data, output_filename):
    type_counts = data['Type'].value_counts()
    type_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Proportion of Each Type in the Dataset')
    plt.ylabel('')  # Hide the y-label for the pie chart
    plt.savefig(output_filename)

def main():
    # Loading data and correcting the column names
    data = loadingandCorrecting('GrowLocations.csv')
    # Map image
    image = mpimg.imread('map7.png')
    
    # Filtering data
    filteredData = filtering(data.copy())    
    # Plotting filteredData
    plotData(image, filteredData, 'Latitude', 'Longitude', "outputImage1.png")
    
    # With the usual labels, the output maps value outside of the uk. Which means that the labels of Latitude and Longitude column is wrong.
    # Allocating the correct names to the columns Latitude and Longitude
    finalData = filteredData.rename(columns={'Latitude': 'Longitude', 'Longitude': 'Latitude'})
    # Plotting finalData
    plotData(image, finalData, 'Longitude', 'Latitude', "outputImage2.png")
    
    # Additional analysis
    pieChart(data, "piechart.png")

if __name__ == '__main__':
    main()

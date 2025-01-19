#!/usr/bin/env python
# coding: utf-8

# # Mortgage deliquency rate and Unemployment Rate in the US

# **Problem Statement**

# 1. Problem Statement: To investigate the relationship between the mortgage deliquency rate in single households and the unemployment rate (focused on Black or African Americans)
# 2. Hypothesis: An increase in unemployment rate in the Black community is most likely to lead to an increase in mortgage deliquency rate in single households. 
# 3. Introduction: The cyclical nature of unemployment within a business cycle has a significant impact on mortgage payments, particularly in times of economic downturns. Notably, during the Great Financial Crisis of 2008, an increase in mortgage defaults was observed, especially among borrowers with high loan-to-value ratios, predominately in minority groups (especially, Blacks and Hispanics groups). The mortgage delinquency rate surged to a record-high at 14.4 per cent. Furthermore, as the Mortgage Bankers Association reported, the delinquency rate was up to 8.22% in the second quarter of 2020. This study aims to investigate the relationship between unemployment rates and high mortgage delinquency rates. 

# **Data Collection**

# The following data sets were collected by from FRED data:
# 1. __[FRED Delinquency Rate on Single-Family Residential Mortgages, Booked in Domestic Offices, All Commercial Banks](https://fred.stlouisfed.org/series/DRSFRMACBS)__
# 2. __[Unemployment Rate - Black or African American](https://fred.stlouisfed.org/series/LNS14000006)__

# **Investigation**

# 1. Data Collection (using FRED API)
# 2. Data Cleaning 
# 3. Data Visualisation 
# 4. Findings

# # Data Collection   

# In[1]:


get_ipython().system('pip install chart-studio')

# Import libraries
import pandas as pd 
import chart_studio.plotly as py
import plotly.graph_objs as go


# ## Install FRED API

# In[2]:


get_ipython().system('pip install fredapi ')


# In[3]:


#import FRED API
from fredapi import Fred
fred_key = 'b4a932dd43aaa0ab9400ac241a790dca'
fred = Fred(api_key=fred_key)


# In[4]:


mortgage_deliq = fred.get_series(series_id = 'DRSFRMACBS')
mortgage_deliq = pd.DataFrame(mortgage_deliq)
mortgage_deliq = mortgage_deliq.reset_index()
mortgage_deliq.columns = ['Date', 'Mortgage Delinquency Rate_Single Family']
mortgage_deliq['Date'] = pd.to_datetime(mortgage_deliq['Date'])  # Convert to datetime
mortgage_deliq = mortgage_deliq[(mortgage_deliq['Date'] >= '2005-03-01') & (mortgage_deliq['Date'] <= '2024-01-01')]

unempBA = fred.get_series(series_id = 'LNS14000006')
unempBA = pd.DataFrame(unempBA)
unempBA = unempBA.reset_index()
unempBA.columns = ['Date', 'Unemployment Rate_Black']
unempBA['Date'] = pd.to_datetime(unempBA['Date'])  # Convert to datetime
unempBA = unempBA[(unempBA['Date'] >= '2005-03-01') & (unempBA['Date'] <= '2024-01-01')]


# # Data Cleaning 

# In[5]:


#shape of the data
mortgage_deliq.shape


# In[6]:


unempBA.shape


# In[7]:


mortgage_deliq.head()


# In[8]:


unempBA.head()


# In[9]:


mortgage_deliq.describe()


# In[10]:


unempBA.describe()


# In[11]:


#checking for missing values
mortgage_deliq.isnull().sum()


# In[12]:


unempBA.isnull().sum()


# # Explore the replationship from the mortgage fixed rates and unemployment from 2008-2024 

# ### Interactive plot to compare mortgage deliquency rate_sinlge family and unemployment rate

# In[13]:


#Define the layout for the plot
layout = go.Layout(
    height=600, 
    width=800,
    title='Mortgage Delinquency Rate and Unemployment Rate',
    xaxis=dict(title='Date'),
    yaxis=dict(
        title='Residential Commercial Mortgage Delinquency Rate on Single-Family',
        color='red',
        range=[0, 20]  # Adjust range for better visualization
    ),
    yaxis2=dict(
        title='Unemployment Rate (Black/African American)',
        color='blue',
        overlaying='y',
        side='right',
        range=[0, 20]  # Adjust range for better visualization
    ),
    legend=dict(
        x=1.05,  # Move the legend farther to the right
        xanchor='left',  # Anchor the legend to the left side of its position
        y=1,  # Position the legend vertically at the top
        yanchor='top'  # Anchor the legend to the top side of its position
    )
)

# Create traces for both y-axes
trace1 = go.Scatter(
    x=mortgage_deliq['Date'],
    y=mortgage_deliq['Mortgage Delinquency Rate_Single Family'],
    name='Mortgage Delinquency Rate',
    yaxis='y',  # Maps to the left y-axis
    line=dict(color='red')
)

trace2 = go.Scatter(
    x=unempBA['Date'],
    y=unempBA['Unemployment Rate_Black'],
    name='Unemployment Rate',
    yaxis='y2',  # Maps to the right y-axis
    line=dict(color='blue')
)

# Create figure with both traces and layout
fig = go.Figure(data=[trace1, trace2], layout=layout)

# Add vertical lines - for dates
dates_for_lines = {
    '2007-04-01': 'Subprime Mortgage Crisis',
    '2020-01-01': 'COVID Pandemic'
}

for date, label in dates_for_lines.items():
    fig.add_vline(
        x=date,  # Use string format for date
        line=dict(color='gray', dash='dash')
    )
    fig.add_annotation(
        x=date,
        y=1,  # Adjust y value according to your data range
        text=f'<b>{label}</b>',
        showarrow=True,
        arrowhead=2
    )

# Plot the figure
fig.show()  # This will display the plot in your local environment


# In[14]:


#printing out the plotly as html
fig.write_html("mortgage_unemploymentBlack.html")


# ## Findings

# 1. There is a correlation between unemployment in the Black community and mortgage deliquency rate in single households. 
# 2. During Submprime mortgage crisis, we can see the mortgage deliquency rate surged up around 200%. 
# 3. During the Covid Pandemic, the mortgage deliquency rate has a smaller percentage icnreaase due to forbearance scheme, despite having  very high levels of unemployment.  

# # Future investigations

# 1. Perform a Predictive model: using a time series forecasting and regression analysis
# 2. Advise solutions based on data analysis results, and scholar journals and articles

# Canadian Crime Dashboard Reflection

Our dashboard is split into two tabs, which we can discuss individually, along with the experience of implementing the dashboard in R, rather than Python.

## Tab 1

### Widgets

We have four widgets that are in a partial state of completion.

- The first widget (Select Metric) is fully implemented.

- Our second widget is fully implemented. It asks users to select from a crime topic (e.g., property, violent, etc).

- Our third widget is fully implemented. Based on what the user selected in the 2nd widget, this allows a user to select a sub-category (e.g., homicide) .

- The fourth widget is fully implemented (Select a Year).


### Visualizations

We have two visualizations to display in this tab.

- First is a Choropleth map for Canada and its provinces. This is fully implemented. As a user selects different crime measurements, the map and its color gradient will update. We've also implemented a feature so that if you click on a province, the bar chart will color code any Census Metropolitian Areas that are in that province. 

- Second is a bar chart of the crime measurement broken down by Census Metropolitan Area. This is fully implemented. 

### Tab 1 Misc

We've recently added a text box with some basic information about our project, where the data is sourced from, and where they can find our Github Repo.


## Tab 2

### Widgets 

- The first widget (a radio button) for selecting the Provincial or CMA level has been fully implemented.

- The second widget (a dropdown component) that lets user select multiple locations (provinces, or CMAs) has been fully implemented.  

- In our original proposal, we had an enhancement widget we were considering to let a user select a crime measurement (e.g., incidents per 100k, % of incidents unfounded). We did not implement this widget. The default graphs use "Incidents per 100k". We did not think that it would be of sufficient value, especially as we demonstrated this functionality in the first tab. 


### Visualizations 

There are four plots on display in this tab. Each plot displays a metric (currently Criminal Incidents per 100,000 population) for different types of crimes in different geographical locations. 

Small improvements we could have made, but didn't in time for our deadline were to relabel the y-axis (it currently is labelled as "value").


## Other Components

We cleaned up all textual descriptions of our data, for example, converting Winnipeg, Manitoba [466062]" to "Winnipeg, Manitoba", fixing french name spellings.

## Why we Implemented with Python

We found it very challenging (and unsuccesful) to implement our Leaflet choleropeth map with R. It was a very easy implementation with Python, which was more than enough to tip us over to completing this project in Python.


## Reflections on TA and Student Feedback

Here is a status of all the feedback we obtained throughout the project:

*Peer Feedback Group 21*

For the screenshot that you included in the readme file, I think it would be great to include the screenshot of your real app interface instead of the prototype given that it was milestone2. **addressed**

For the convenience of potential contributors who are interested in contributing to your project, it would be great to include the instructions on how they can run the app, and suggestions on what aspects they can contribute to for the project. **addressed - we included a simple text book in the app, and some nudging instructions in our map.**

However, regarding usability, I think the appearance can be improved. For example,

    the font of the two tabs could be bigger & bolded. **implemented**
    You can also add more white space between filters. **implemented**
    would be great if you add a side note to explain what the empty plots mean based on user selections (e.g. no data).  

**somewhat addressed - we revised our dashboard in ways that reduce the chance that a user produces an empty plot (e.g., setting the default year to 2019, and removing the ability of a user to select nothing from the widgets). However, our dataset has missing data for certain types of measurements for certain years. For our deadline, we weren't able to deal with missing data in smarter ways than what we have already done.**


*TA Feedback*

Nice touch adding a graph save option. It would be helpful if you made a note to let the user know they can do this. It was hard to notice. **This is a default altair feature and not something we are really advertising, so we are leaving it in but not drawing attention to it**

...In regards to your question about manually cleaning the y-axis of your Tab 1 bar graph, removing the [number] from each label would be more than enough... **addressed**

....I would instead focus on ordering the data in the bar graph, either from highest to lowest or by province... **addressed**

...Having the x-axis at the bottom of the graph outside the immediate view is not ideal. Consider putting it at the top of the graph as well, and even more ideal would be for it to float as you scroll... **addressed - we resized our dashboard so that the entire bar chart on the first tab should display without any scrolling**

For tab 2: As I was using this tab, I found it a little frustrating that my location selection was lost when I toggled between the Province and CMA options. **addressed somewhat - we put default selection values for provinces and CMA's. However, if you  toggle back and forth, it won't remember what you previously had selected. We found implementing that kind of "memory" feature in the dashboard to be too much of a challenge given we haven't encountered this kind of functionality in class**

Tab 2: will there be a max number of CMAs Sarah can select to compare? **a user can select/deselect as they please**

Will the abbreviation CMA be explained anywhere in the dashboard? **addressed - we spell out CMA in the About this Dashboard text box**


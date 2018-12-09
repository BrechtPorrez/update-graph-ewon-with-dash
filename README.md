# update-graph-ewon-with-dash

All the data of different installations at different customers sites is collected and send to a MySql DB with the help of an EWon.
This web application enables the user to select an installation with the help of a dropdown menu. This dropdown menu automatically updates a new dropdown menu. Is this second dropdown menu the user can select the available parameters of the corresponding installation. When he selects the desired parameter, the graph is automatically updated.
Now the user can zoom, pan,… on the graph and also save it as a png.

Todo:
*Possibility for selection of multiple parameters with multiple Y-axis.
*Add date range to reduce loading time.
*Add moving average, this could be useful for example to filter out the downtime of an installation and get a proper view of the evolution over time.

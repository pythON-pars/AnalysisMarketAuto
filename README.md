# Price Market Analysis
### This project is being developed with almost minimal knowledge
___
This project does not pursue a commercial goal, but was written for the sake of interest, at least it was like that at the beginning :)
And so his goal is to analyze a certain sample of exact goods, and create a dynamic table for a quarter of the time.
The data will be collected by Python, a JavaScript front end, and a database, most likely PostgreSQL (currently using SQLite).

In the process of creating a project, its goals will be adjusted, in principle, this is normal!
___
## Architecture
To view architecture.drawio you need to install the drawio extension in Vscode and open the architecture.drawio file
___
# Small notes
A decision has been made so far to synchronously take the correct links to cars and generations, and put the necessary data in the database.
Perhaps if I'm not too lazy, I'll add asynchronous data collection;)

There will be only two tables in the database, one of them for storing links to models and their generations, and the second with prices, year of manufacture and other indicators. After that, the data will be collected, and while the data is being collected, the frontend will be written
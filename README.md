# Expense Tracker using Natural Language Processing
The project is a simple montly expense tracker android application. It consists of 
three major blocks
 - The Android application
 - The NLP processing server
 - Deployment on AWS
 
The user can speak in the app and query for expenses or add new expenses. These spoken sentences are converted to text using Google's speech-to-text API and sent to the server on AWS for processing. The text is processed and the new expenses are added/existing expenses are queried from the database and the result is returned to the App which displays them on the screen.

 ### Examples of tasks
 **Query**: add $55 for transportation. 
 
 **Action**: adds $55 to the transportation category for current month.
 
 **Result**: I added that to your expenses, you said $55 for transportation. 
 
 ----------------------------------
 **Query**: add $25 for groceries notes purchased bread and milk.
 
 **Action**: adds $25 to the groceries category for current month and updates the notes with purchased bread and milk.
 
 **Result**: I added that to your expenses, you said $25 for groceries purchased bread and milk in notes.
  
 ----------------------------------
 **Query**: How much did I spend on eating out last week?
 
 **Action**: queries the database to get the total amount spent in the eating out category for the dates in the previous week.
 
 **Result**: You spent $45 eating out last week. 
 
 ----------------------------------
 **Query**: This month expenses on laundry
 
 **Action**: queries the database to get the total amount spent in the laundry category for the dates in the current month (untill now).
 
 **Result**: You spent $14 on laundry this month. 
 
 ## NLP with RASA framework
The open source framwork RASA is used for the NLP tasks. Below is a brief explanation of the file contents. More information about how RASA works and what each file contains can be found in the [RASA documentation]
(https://rasa.com/docs/rasa/installation/)

### Folder/File contents
**domain.yml** - contains the intents, entities, actions and responses

**data/stories.md** - Stories are the training data with conversation path examples used to train language model. 

**data/nlu.md** - NLU examples for all the intents with entities.

**functions.py** - custom python code to process the data and store/extract from the database.

**models/** - Contains the trained model.

 - The way RASA works on a high level is when it receives a sentence it processes the text in a pipeline consisting of various tools. 
 - Each step in the processing pipeline performs a specific task and appends the result to a data structure. For example the sentence is first classified as belonging to a particular intent (category), then the next step is to extract all the entities and store them. Once all the information is extracted the core decides what action to take and outputs the appropriate response.
 - There are a lot of components, a few important ones are Intents, Entities, and Actions.
 - Intents are like categories. Every sentence gets classifies as belonging to a particular category.
 - Entities are the important pieces of text that we want to extract from the sentences. In this case information about the price, category, notes etc. 
 - Actions are custom code which connects the RASA engine to external application such as a database and is also used to perform additional processing on the extracted text.
 - For this particular case, once the entities are extracted further processing is done in the actions.py and function.py files to add to/query the database for results. 
 - Once the date and category are extracted by RASA NLU server, this information is further processed to get the proper date range and a query is returned to the action (take a look at functions.py to see how the query is built with the information). 
 - Then a call to mongoDB is made with the query using pymongo to insert/query the data.  
 
-----------------
-----------------
## Deployment on AWS

#### Resources used on AWS

 - EC2 instance (t2 medium) 
 - Route53
 ----------
 - A t2 medium instace was used to deploy the RASA server (even micro
   and mini should work but RASA installation required > 1GB RAM so
   medium was used). The instance runs Ubuntu 16.04.
 - Route53 is a cloud DNS service. It was used to map the domain (www.ext_____.com) to instance's internal IP. It redirects user requests to the instance. Route 53 is required since the domain was not purchased on AWS. The GoDaddy nameservers need to be  pointed to EC2 on AWS.
 - MongoDB was locally set up on the compute instance and could be accesed vis localhost from the instance.
 - RASA runs on the Flask micro framework.  To launch the application uWSGI application server is used and then Nginx was used to launch the application which acts as a front end reverse proxy.

#### Steps in brief

 1. [Install RASA](https://legacy-docs-v1.rasa.com/user-guide/installation/), Pandas and MongoDB.
 2. Set up MongoDB. Pymongo connected is used to access the database from custom actions in RASA.
 3. Run the RASA core and actions server in background using tmux session.
 4. Install and create uWSGI and configure it. Create an WSGI entry point.
 5. Nginx is needed to pass web requests to the created socket using the uwsgi protocol. 
 6. Install Nginx and configure* the sites-available in `/etc/nginx` with port 80 and server_name with the domain. 
 7. Configure Route 53 to map the domain to instance IP. 
 
 *More information on installation of [UWSGI and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04)  
 **[Route53 additional instructions](https://www.tutorialspoint.com/amazon_web_services/amazon_web_services_route_53.htm)

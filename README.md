# Django Web App: Music Collection

**Dorset College Dublin**  
**BSc in Science in Computing & Multimedia**  
**Back-End Web Development - BSC30922**  
**Year 3, Semesters 1 & 2**  
**Continuous Assessments 1, 2 & 3**

**Lecturer name:** Geoff Wright  
**Lecturer email:** geoff.wright@dorset.ie

**Student Name:** Mateus Fonseca Campos  
**Student Number:** 24088  
**Student Email:** 24088@student.dorset-college.ie

**Submission date:** 29 November 2022 (CA1), 18 December 2022 (CA2) and 28 March 2023 (CA3)

This repository contains a "Music Collection" Django web app developed for my CAs 1, 2 and 3 at Dorset College BSc in Computing, Year 3, Semesters 1 and 2.

## Part 1: Requirements and Setup

**Framework:** this project requires installation of both [Python](https://www.python.org/downloads/) and [Django](https://www.djangoproject.com/download/).

**Packages:** to install all the packages required by this application, as well as their dependencies, type the following on a terminal window at the root of the project:

    pip install -r requirements.txt

**Environment:** create a file called *.env* at the root of the project with the following content:

    SECRET_KEY='<replace with your project's secrete key>'
    DISCOGS_USER_TOKEN='<replace with your personal Discogs user token>'

**DNS configuration:** this project requires a simple DNS configuration in order to enable domain differentiation between the webapp's domain and the fake CDN's domain. Add the following, depending on your operating system:

    # on Linux/Mac open /etc/hosts
    # on Windows open C:\Windows\System32\drivers\etc\hosts
    # add:

    127.0.0.1     www.dorsetmusiccollection.com cdn.dmc.net
    
**Database engine:** it also requires access to a database through a user with enough privileges to create new tables and manipulate the data therein ([see docs](https://docs.djangoproject.com/en/4.1/ref/databases/)). The project is currently set to work with [MySQL](https://dev.mysql.com/downloads/), but switching to another supported backend should be an easy fix.

**Migration:** it is necessary to tell Django to create the tables in the database from the models defined in the project. On a terminal window at the project's root directory:

    python manage.py makemigrations
    python manage.py migrate

**Fixture:** once the tables are created, it is possible to populate them with predefined data to start playing with the app right away. The project contains the file */fixtures/data.json*, which is a fixture, a JSON object that tells Django what data to use to populate the tables in the database. On the terminal:

    python manage.py loaddata data.json

**Run Configuration:** in order to successfully execute the application, two instances of the Django server need to be run, one for the main website and another for the fake CDN. The file *[runSiteAndCDN](https://github.com/mateusfonseca/dorsetMusicCollection/blob/master/.idea/runConfigurations/runSiteAndCDN.xml)* can be used to tell [PyCharm](https://www.jetbrains.com/pycharm/) to do just that in a very simple way (see [Run/debug configurations](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html)). Alternatively, both instances can also be run from the terminal:

    # start processes and send them to background
    python manage.py runsslserver cdn.dmc.net:9000 &
    python manage.py runsslserver www.dorsetmusiccollection.com:8000 &

    # bring each process back to foreground and end it
    # on Linux/Mac
    fg # then Ctrl+C
    # on Windows
    get-job # then Ctrl+C

**API:** this app fetches its music data from the [Discogs](https://www.discogs.com/) database through their [official API](https://www.discogs.com/developers). It is free to use, but it does require user authentication in the form of a token. In this project, the file */polls/views.py*, on line 106, reads the user token string from a local file that is gitignored. In order to create more polls than the ones provided with the app via fixture, it is necessary to create a Discogs user account and request a token.

## Part 2: Background

At the core of Django's design philosophies, there lives the MVT (Model-View-Template) pattern. This architectural approach aims to provide *separation of concerns*, a key aspect of modular programming, as well as adhering to the framework's principles. Each component of the MVT pattern has distinct responsibilities:

- **Model:** Django models are Python classes that can be instantiated as runtime representations of a database entity. The class' attributes map to the entity's fields.


- **View:** views are Python functions/classes written to respond to web requests. They map to specific URL endpoints and are set to handle requests according to the implemented logic inside.


- **Template:** through DTL, Django Template Language, the framework makes it possible to write text files containing variables as placeholders that can be dynamically rendered as part of a web response. It also allows for the implementation of control flow statements to handle data pertaining presentation.

Read more about Django's philosophies and principles [here](https://docs.djangoproject.com/en/4.1/misc/design-philosophies/).

## Part 3: Breakdown

This project was developed based on the web framework Django and its MVT design pattern. As of now, it only offers one application, the Polls app, which allows for the creation of music related polls that can be voted by other users. The following scheme explains the organization of its main components:

- **1. Models** \#CA1
  - **1.1. Question**  
  This class represents the Question entity in the database. Each question is, in fact, one individual poll, with up to ten music albums as options to be chosen from. Its attributes are:
    - **genre:** the music genre of the albums that feature in the poll.
    - **year:** the release year of the albums that feature in the poll.
    - **text:** the presentation text of the poll, the question itself. It always follows the format "What is the best \<genre\> album of \<year\>?"
    - **pub_date:** the publication date of the poll.
  - **1.2. Choice**  
  This class represents the Choice entity in the database. Each choice is a music album whose genre (at least one, because an album can have many) and year match those defined for the poll that the choice belongs to. Its attributes are:
    - **question:** the database ID of the question that the choice belongs to.
    - **image:** the URL to the album cover image at [Discogs](https://www.discogs.com/).
    - **title:** the album's title.
    - **artist:** the album's main artist.
    - **year:** the release year of the album (matches its parent's).
    - **genres:** the list of genres of the album (at least one matches its parent's).
    - **votes:** the number of votes the album has received.
    - **country:** the album's release country.
    - **url:** the URL to the album's page at [Discogs](https://www.discogs.com/).

  Other models used in this project, such as the User model, are provided out-of-the-box by Django itself. Access it [here](https://docs.djangoproject.com/en/4.1/ref/contrib/auth/) for more information.


- **2. Views**  
  - **2.1 accounts/SignUpView** \#CA2  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../accounts/signup*. It renders the template *registration/signup.html* and has the following methods:
    - **post:** it handles POST requests with the attached [UserCreationForm](https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#django.forms.ModelForm) and saves the newly created user to the database.
  
    **Restrictions:** this view has no restrictions.
  - **2.2 accounts/DetailView** \#CA2  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../accounts/<user_id>/detail/*. It renders the template *accounts/detail.html* and has the following methods:
    - **test_func:** it tests if the user making the request is the same whose details are being requested.
  
    **Restrictions:** user must be logged in; test_func must be true.
  - **2.3 accounts/DeleteView** \#CA2   
  This class controls user requests to the associated endpoint defined in the URL pattern *.../accounts/<user_id>/delete/*. It renders the template *accounts/delete.html* and has the following methods:
    - **post:** it handles POST requests with the attached form and, if successful, deletes the current user from the database.
    - **test_func:** it tests if the user making the request is the same whose details are being requested.
  
    **Restrictions:** user must be logged in; test_func must be true.
  - **2.4 accounts/UpdateEmailView** \#CA2   
  This class controls user requests to the associated endpoint defined in the URL pattern *.../accounts/<user_id>/detail/email/*. It renders the template *accounts/change_email.html* and has the following methods:
    - **post:** it handles POST requests with the attached form and, if successful, updates the current user's email in the database.
    - **test_func:** it tests if the user making the request is the same whose details are being requested.
  
    **Restrictions:** user must be logged in; test_func must be true.
  - **2.5 polls/IndexView** \#CA1  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../polls/*. It renders the template *polls/index.html* and has the following methods:
    - **get_queryset:** it handles GET requests by returning a list with all published questions to date ordered from the most recent to the oldest.
  
    **Restrictions:** this view has no restrictions.
  - **2.6 polls/DetailView** \#CA1  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../polls/<poll_id>/*. It renders the template *polls/detail.html*. It has no explicitly declared methods, but it handles GET requests by returning a detailed view of the current poll with all its choice options.  
  **Restrictions:** this view has no restrictions.
  - **2.7 polls/ResultsView** \#CA1  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../polls/<poll_id>/results/*. It renders the template *polls/results.html*. It has no explicitly declared methods, but it handles GET requests by returning a list view of the current poll with all its choice options ordered from most to least voted.  
  **Restrictions:** this view has no restrictions.
  - **2.8 polls/CreateView** \#CA1  
  This class controls user requests to the associated endpoint defined in the URL pattern *.../polls/create/*. It renders the template *polls/create.html* and has the following methods:
    - **get:** it handles GET requests by returning one list of genres and one list of years to be selected from when creating the new poll.
    - **post:** it handles POST requests with the selected genre and year and queries Discogs' database through their API with the provided terms. Upon successful retrieval of the album objects, selects only the top-10 most popular ones, create the new poll and all its choices, and saves them to the database.  
  
    **Restrictions:** user must be logged in. #CA2 
  - **2.9 polls/vote** \#CA1  
  This function controls user requests to the associated endpoint defined in the URL pattern *.../polls/<poll_id>/vote/*. It handles POST requests with the ID of the chosen album by incrementing by one the value its votes field in the database.  
  **Restrictions:** user must be logged in. \#CA2 


- **3. Templates**  
  - **3.1 accounts/change_email.html** \#CA2   
  This HTML file gets dynamically inflated by the *accounts/UpdateEmailView* view and displays a form that allows the current logged-in user to alter the e-mail address associated with their account.
  - **3.2 accounts/delete.html** \#CA2   
  This HTML file gets dynamically inflated by the *accounts/DeleteView* view and displays a form that allows the current logged-in user to completely delete their account.
  - **3.3 accounts/delete_confirmation.html** \#CA2   
  This HTML file gets dynamically inflated by the *accounts/DeleteView* view and displays a message that confirms the user account deletion.
  - **3.4 accounts/detail.html** \#CA2   
  This HTML file gets dynamically inflated by the *accounts/DetailView* view and displays the current logged-in user's details.
  - **3.5 polls/create.html** \#CA1  
  This HTML file gets dynamically inflated by the *polls/CreateView* view and displays a form that allows the current logged-in user to create a new poll by selecting both a genre and a year from the dropdowns.
  - **3.6 polls/detail.html** \#CA1  
  This HTML file gets dynamically inflated by the *polls/DetailView* view and displays the select poll's details, such as its question text and the options to choose from.
  - **3.7 polls/index.html** \#CA1  
  This HTML file gets dynamically inflated by the *polls/IndexView* view and displays a list of the 5 most recently created polls, as well as a search box that filters polls by genre and year.
  - **3.8 polls/no_matches.html** \#CA1  
  This HTML file gets dynamically inflated by the *polls/CreateView* view and displays a message that informs that the chosen combination of genre and year did not return any results.
  - **3.9 polls/results.html** \#CA1  
  This HTML file gets dynamically inflated by the *polls/ResultsView* view and displays all the options for the selected poll ranked by number of votes, from most to least.
  - **3.10 admin/base_site.html** \#CA1  
  This HTML file is automatically generated by Django and pertains to the admin view. It gets dynamically inflated and displays the default administrative options provided by Django.
  - **3.11 registration/login.html** \#CA2   
  This HTML file gets dynamically inflated and displays a form that allows users to log in.
  - **3.12 registration/password_change_done.html** \#CA2   
  This HTML file gets dynamically inflated and displays a message that confirms the current logged-in user's password has been changed.
  - **3.13 registration/password_change_form.html** \#CA2   
  This HTML file gets dynamically inflated and displays a form that allows the current logged-in user to change their password.
  - **3.14 registration/password_reset_complete.html** \#CA2   
  This HTML file gets dynamically inflated and displays a message that confirms the user's password has been reset.
  - **3.15 registration/password_reset_confirm.html** \#CA2   
  This HTML file gets dynamically inflated and displays a form that allows the user to set a new password.
  - **3.16 registration/password_reset_done.html** \#CA2   
  This HTML file gets dynamically inflated and displays a message that informs that an e-mail has been sent to the user with instructions for resetting their password.
  - **3.17 registration/password_reset_form.html** \#CA2   
  This HTML file gets dynamically inflated and displays a form that allows the user to inform their e-mail address and receive instructions for resetting their password.
  - **3.18 registration/signup.html** \#CA2   
  This HTML file gets dynamically inflated and displays a form that allows the user to create a new account.
  - **3.19 about.html** \#CA1  
  This HTML file gets dynamically inflated and displays a brief description of the website's background and purpose.
  - **3.20 base.html** \#CA1 \#CA2  
  This HTML file gets dynamically inflated and is the base of all other templates on the website. It holds the HTML head content shared amongst all other webpages, as well as the body container, navbar and footer.
  - **3.21 home.html** \#CA1  
  This HTML file gets dynamically inflated and is the response to accessing the very root of the website.

## Part 4: Testing \#CA3

The application now offers unit testing modules that can be run from the command line. Both manual and automated tests are available, and it is important to note that the manual tests will halt execution and wait for user input. On a terminal window:

    # to run all tests
    python manage.py test
    
    # to run only the automated tests
    python manage.py test --exclude-tag=manual

    # to run only the manual tests
    python manage.py test --tag=manual

Test files breakdown:

- **1. Manual Testing:**
  - **1.1 polls.test_manual**  
  This python file defines manual test case classes and methods that are run against the views within polls.
- **2. Automated Testing:**
  - **2.1 accounts.test_views**  
  This python file defines automated test case classes and methods that are run against the views within accounts.
  - **2.2 polls.test_views**  
  This python file defines automated test case classes and methods that are run against the views within polls.
  - **2.3 polls.test_models**  
  This python file defines automated test case classes and methods that are run against the models within polls.

In order to determine the percentage of the application that is currently covered by the available tests, the [Coverage.py](https://coverage.readthedocs.io/en/7.2.2/) package was used. Access the most up-to-date coverage report for this application [here](http://htmlpreview.github.io/?https://github.com/mateusfonseca/dorsetMusicCollection/blob/master/htmlcov/index.html), which indicates a 99% of total coverage.

## Part 5: Security \#CA3

A number of security features have been added to this project as of its latest version:

- **1. Authentication:**
  - **1.1 Media content from CDN:**  
  To prevent the *redirect_authenticated_user* flag from being exploited by social media fingerprinting, media content, such as images and the favicon, are now serverd by a CDN (albeit a simulated one, as it is actually just another app running on a different port and accessible through a dedicated domain name).
- **2. Protecting sensitive data:**
  - **2.1 SECURE_SSL_REDIRECT:**  
  Enabled to redirect all non-HTTPS requests to HTTPS.
  - **2.2 CSRF_COOKIE_SECURE:**  
  Enabled so that CSRF cookies are only sent with an HTTPS connection.
  - **2.3 SESSION_COOKIE_SECURE:**  
  Enabled so that session cookies are only sent with an HTTPS connection.
- **3. Misconfigurations:**
  - **3.1 Safely joining paths:**  
  Using the method *os.path.join()* to join path strings is safer than pure string concatenation as it prevents injected malicious code from being executed.
  - **3.2 Production site:**  
  *DEBUG* has been disabled as it should always be in production. When enabled, it provides backend details to the browser for debugging purposes.
  - **3.3 Allowed hosts:**  
    Limited allowed hosts for both the main site and the fake CDN to the relevant IP addresses and domain names only.
  - **3.4. Secrets:**  
  Using *python-dotenv* to read secret keys from gitignored file to make sure they are kept secret.
  - **3.5 Django admin URL:**  
  Changed URL for admin from default *"admin"* to *"management"* to make it a less obvious target for hackers.
  - **3.6 Django deployment check:**  
  Command *check --deploy* returned no issues.
- **4. Cross Site Request Forgeries (CSRF):**
  - **4.1 CSRF token:**  
  All POST requests are sent with an attached *csrf_token* to prevent CSRF attacks.
- **5. HTTP Strict Transport Security:**
  - **5.1 SECURE_HSTS_SECONDS:**  
  Set to 2592000 so that the browser refuses to connect via an insecure connection for 30 days.
  - **5.2 SECURE_HSTS_INCLUDE_SUBDOMAINS:**  
  Enabled so that all subdomains are included in this configuration.
  - **5.3 SECURE_HSTS_PRELOAD:**  
  Enabled so that the domain can be submitted to browser preload list.

## Part 6: References

Conceptually, every line of code in this project was written based on official documentation:

- **[Python](https://docs.python.org/3/)**
- **[Django](https://docs.djangoproject.com/en/4.1/)**
- **[MDN Web](https://developer.mozilla.org/)**
- **[Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)**
- **[Coverage.py](https://coverage.readthedocs.io/en/7.2.2/)**

Robin Linus on **[social media fingerprint](https://robinlinus.github.io/socialmedia-leak/)**.

Clarifying code snippets from **[W3Schools](https://www.w3schools.com/)**.

Visits to our most beloved **[StackOverflow](https://stackoverflow.com/)** certainly happened, for insight and understanding.

This app uses data from the **[Discogs API](https://www.discogs.com/developers)***.

*This application uses Discogs’ API but is not affiliated with, sponsored or endorsed by Discogs. ‘Discogs’ is a trademark of Zink Media, LLC.

## Part 7: Copyright Disclaimer

This project may feature content that is copyright protected. Please, keep in mind that this is a student's project and has no commercial purpose whatsoever. Having said that, if you are the owner of any content featured here and would like for it to be removed, please, contact me and I will do so promptly.

Thank you very much,  
Mateus Campos.

# CA1: CRUD Application
# CA2: Registration/Authentication
# CA3: Test and Security

"""
This file defines all the views in the app polls.
The views are classes and functions that respond to web requests with appropriate web responses.
They invoke the templates that will be rendered in return (if applicable) and handle any errors
that may arise during the handling of the requests.
"""

import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic

from .models import Choice, Question


# get parameters used to create new poll
# lifted out of CreatView so that it can be accessed from tests
def get_parameters():
    genres = ['AOR', 'Abstract', 'Acid', 'Acoustic', 'African', 'Alternative Rock', 'Ambient',
              'Arena Rock', 'Art Rock', 'Audiobook', 'Avant-garde', 'Jazz Avantgarde', 'Ballad',
              'Baroque', 'Beat', 'Big Band', 'Black Metal', 'Bluegrass', 'Blues Rock', 'Bolero',
              'Bollywood', 'Boom Bap', 'Bop', 'Bossa Nova', 'Bossanova', 'Breakbeat', 'Breakcore',
              'Breaks', 'Celtic', 'Cha-Cha', 'Chanson', 'Choral', 'Classic Rock', 'Classical',
              'Comedy', 'Conscious', 'Contemporary', 'Contemporary Jazz', 'Contemporary R&B',
              'Cool Jazz', 'Country', 'Country Rock', 'Cumbia', 'Dance-pop', 'Dancehall',
              'Dark Ambient', 'Darkwave', 'Death Metal', 'Deep House', 'Disco', 'Dixieland', 'Doo Wop',
              'Doom Metal', 'Downtempo', 'Drone', 'Drum n Bass', 'Dub', 'Dubstep', 'EBM',
              'Easy Listening', 'Electric Blues', 'Electro', 'Electro House', 'Emo', 'Euro House',
              'Eurodance', 'Europop', 'Experimental', 'Field Recording', 'Flamenco', 'Folk',
              'Folk Rock', 'Free Improvisation', 'Free Jazz', 'Funk', 'Fusion', 'Future Jazz',
              'Gangsta', 'Garage House', 'Garage Rock', 'Glam', 'Glitch', 'Gospel', 'Goth Rock',
              'Grindcore', 'Grunge', 'Happy Hardcore', 'Hard Bop', 'Hard House', 'Hard Rock',
              'Hard Trance', 'Hardcore', 'Hardcore Hip-Hop', 'Hardstyle', 'Harsh Noise Wall',
              'Heavy Metal', 'Hi NRG', 'Hindustani', 'Hip Hop', 'House', 'IDM', 'Indie Pop',
              'Indie Rock', 'Industrial', 'Instrumental', 'Italo-Disco', 'Italodance', 'J-pop',
              'Jazz-Funk', 'Jazz-Rock', 'Jungle', 'Krautrock', 'Latin', 'Latin Jazz', 'Laïkó',
              'Leftfield', 'Lo-Fi', 'MPB', 'Merengue', 'Metalcore', 'Minimal', 'Mod', 'Modern',
              'Modern Classical', 'Musical', 'Musique Concrète', 'Neo-Classical', 'New Age',
              'New Wave', 'Noise', 'Novelty', 'Nu Metal', 'Oi', 'Opera', 'Parody', 'Poetry', 'Polka',
              'Pop Punk', 'Pop Rap', 'Pop Rock', 'Post Bop', 'Post Rock', 'Post-Punk', 'Power Metal',
              'Power Pop', 'Prog Rock', 'Progressive House', 'Progressive Metal', 'Progressive Trance',
              'Psy-Trance', 'Psychedelic Rock', 'Punk', 'Radioplay', 'Reggae', 'Reggae-Pop',
              'Religious', 'Renaissance', 'Rhythm & Blues', 'RnB/Swing', 'Rock & Roll', 'Rockabilly',
              'Romantic', 'Roots Reggae', 'Rumba', 'Salsa', 'Samba', 'Schlager', 'Score', 'Shoegaze',
              'Ska', 'Sludge Metal', 'Smooth Jazz', 'Soft Rock', 'Soul', 'Soul-Jazz', 'Soundtrack', 'Southern Rock',
              'Space Rock', 'Speed Metal', 'Spoken Word', 'Stoner Rock', 'Story', 'Surf', 'Swing',
              'Symphonic Rock', 'Synth-pop', 'Synthwave', 'Tango', 'Tech House', 'Techno', 'Theme',
              'Thrash', 'Thug Rap', 'Trance', 'Trap', 'Tribal', 'Trip Hop', 'UK Garage', 'Vaporwave',
              'Vocal', 'Volksmusik']  # list of available genres to choose from
    years = [year for year in range(1900, datetime.now().year + 1)]  # range of years: 1900 to present year
    years.reverse()  # most recent years first
    return genres, years  # return parameters


class IndexView(generic.ListView):  # poll's app home view
    template_name = 'polls/index.html'  # template to be rendered
    context_object_name = 'question_list'  # object that can be accessed from the template.

    def get_queryset(self):  # returns list of published questions
        return Question.objects.order_by('-pub_date')  # list ordered, most recent first


class DetailView(generic.DetailView):  # details view of specific poll
    model = Question  # Question instance from models
    template_name = 'polls/detail.html'  # template to be rendered


class ResultsView(generic.DetailView):  # results view of specific poll
    model = Question  # Question instance from models
    template_name = 'polls/results.html'  # template to be rendered


@method_decorator(login_required, name='get')  # only logged-in users can access this view
class CreateView(generic.CreateView):  # create new poll view
    model = Question  # Question instance from models
    template_name = 'polls/create.html'  # template to be rendered
    fields = ['genre', 'year']  # fields to be filled in the creation form
    genres, years = get_parameters()  # get parameters used to create new poll

    def get(self, request, *args, **kwargs):  # handles GET requests
        context = {'genres': self.genres, 'years': self.years}  # sends lists of genres and years to template
        return render(request, self.template_name, context)  # renders the template

    def post(self, request, **kwargs):  # handles POST requests
        genre = request.POST['genre']  # genre selected by user in the creation form
        year = request.POST['year']  # year selected by user in the creation form

        # Discogs API for Python, for more information access:
        # https://www.discogs.com/developers and https://github.com/joalla/discogs_client
        import discogs_client

        # authenticated queries to Discogs API require a personal user token.
        # here, the token is retrieved from a git-ignored file at the root of the project.
        # even without authentication, it is still possible to query their database,
        # but some pieces of information may be missing from the results.
        d = discogs_client.Client('dorsetMusicCollection/0.1',
                                  user_token=os.getenv('DISCOGS_USER_TOKEN'))

        # query Discogs' database with provided genre and year
        results = d.search(type='master', style=genre, year=year)

        if len(results) == 0:  # if query returned empty
            # render no_matches template
            return render(request, 'polls/no_matches.html', context={'genre': genre, 'year': year})
        else:  # if query is not empty
            self.model = Question.objects.create()  # create an entry in the database for this new poll
            self.model.genre = genre  # set its genre
            self.model.year = year  # set its year
            self.model.text = f'What is the best {genre} album of {year}?'  # set its text
            self.model.save()  # save it to database

            # combines all results' pages into one list
            all_pages = [(results.page(i)) for i in range(results.pages)]
            # only master release records from each page in new list
            all_pages_flattened = [master for page in all_pages for master in page]

            masters = {}
            for master in all_pages_flattened:

                artist = master.title.split(' - ')[0]  # set artist from master
                artists = [v[4] for k, v in masters.items()]  # list of artists being handled

                if artist in artists:  # checks if the current artist is already in the list
                    artist_index = artists.index(artist)

                    # if current artist is already in the list, keep only their most popular release
                    if master.data['community']['have'] + master.data['community']['want'] > \
                            [v[0] for k, v in masters.items()][artist_index]:
                        artists.pop(artist_index)
                        masters.pop([master_id for master_id in masters][artist_index])

                # if current artist is not yet in the list, add the release
                if artist not in artists:
                    masters[master.id] = [
                        master.data['community']['have'] + master.data['community']['want'],  # album's popularity
                        master.data['country'],  # album's release country
                        master.data['cover_image'],  # album's cover image
                        master.title.split(' - ')[1],  # album's title
                        artist,  # album's artist
                        master.year,  # album's release year
                        "/".join(master.data['style']),  # album's list of genres
                        "https://www.discogs.com" + master.data['uri'],  # album's url on Discogs website
                    ]
            masters = sorted(masters.items(), key=lambda x: x[1][0])  # sort all albums by popularity

            top_10 = masters[len(masters) - 10:]  # only the 10 most popular

            # creates one database entry for each album in the top 10
            for release in top_10:
                choice = Choice(
                    country=release[1][1],
                    image=release[1][2],
                    title=release[1][3],
                    artist=release[1][4],
                    year=release[1][5],
                    genres=release[1][6],
                    url=release[1][7],
                    question_id=self.model.pk,
                )
                choice.save()  # saves to database

            # renders template for details view of the newly created poll
            return HttpResponseRedirect(reverse('polls:detail', kwargs={'pk': self.model.pk}))


@login_required  # only logged-in users can access this function
def vote(request, question_id):  # handles vote submission
    question = get_object_or_404(Question, pk=question_id)  # if question cannot be found renders 404 page
    try:  # tries to use choice_id from form
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):  # excepts if no choice_id was passed in
        return render(request, 'polls/detail.html', {  # renders the question voting form again
            'question': question,  # same question
            'error_message': "You didn't select a choice.",  # error message to be added
        })
    else:  # once accepted
        selected_choice.votes += 1  # increases number of votes by one
        selected_choice.save()  # saves to database
        # renders template for results view of the current poll
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

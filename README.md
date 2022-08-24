# MovieRecommendation

## Introduction

A recommender system, or a recommendation system (sometimes replacing 'system' with a synonym such as platform or engine), is a subclass of information filtering system that <br/>provide suggestions for items that are most pertinent to a particular user.

![alt text](https://github.com/alessandroNarcisi96/MovieRecommendation/blob/master/Images/simpson.jpg)

This notebook aims at building a recommendation engine from the content of the TMDB dataset that contains around 5000 movies and TV series.<br/>
Basically, the engine will work as follows: after the user has provided the name of a film he liked, the engine should be able to select in the database a list of 5 films that the user will enjoy.

During the analysis I will use the following features to suggest a list of movies:<br/>

**1. Genre**
* This feature represents the movie genre among these:<br/>
  'Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','Foreign','History','Horror','Music','Mystery','Romance','Science Fiction','TV Movie','Thriller','War','Western'
     
**2. Description of the movie.** 
* A short description of the movie<br/>
    
**3. Cast.**
* List of actors<br/>

## Challenge : How do you determine which movies are similar to one another?

This is the main problem to address infact we should find a way to highlight when two movies have features in common.<br/>

The approach is more less the same of any data science project:<br/>
    1)Translate your object in a math object<br/>
    2)Find a way to deal with this object to achieve the goal<br/>
    3)Decode the result<br/>


First of all we are going to convert a movie in a vector by trasforming each feature in a number.<br/>
For genre and cast will be enough the hot-encoding.<br/>
For the description we will see it in details in the next step.<br/>

Let's say that we have a now a list of movies represented by vectors.<br/>
How can we determine how similar they are?<br/>

#### A good measure is the cosine similarity.<br/>

![alt text](https://github.com/alessandroNarcisi96/MovieRecommendation/blob/master/Images/cosSim2.png)<br/>

Cosine similarity measures the similarity between two vectors of an inner product space.<br/>
It is measured by the cosine of the angle between two vectors and determines whether two vectors are pointing in roughly the same direction<br/>
![alt text](https://github.com/alessandroNarcisi96/MovieRecommendation/blob/master/Images/formula.png)<br/>
By using this criteria we will figure out similar vectors.<br/>

Finally we will decode the closest vector to the given one to return the list of movies<br/>

## Text-Embedding

As said above we have to find a way to trasform the description in numbers.<br/>
We can't use hot-encoding here as it can be used only when the feature is categorical.<br/>
So to achieve the goal we are going to follow the next steps:<br/>

### Extract the nouns
Let's see the description of Inception:<br/>

'Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible: "inception", the implantation of another person\'s idea into a target\'s subconscious.'<br/>

Here there are many words but of course there are words more relevant than others.<br/>
For example nouns,verbs and adjectives.<br/>
By using a library called spacy we can extract all the nouns easily.<br/>

This is the result:<br/>
"thief espionage subconscious targets chance life payment task inception implantation person idea target subconscious"<br/>

### Clean the words

Another step to follow is that we want to trasform all the variations of the same word to only one word.<br/>
For example {'spy', 'spying','spies'} we could use just one word like spy,<br/>


### Group by meaning
The last step has performed to increase the words in common in the movie description.<br/>
For example {'world', 'planet','Earth'} are all synonyms so we could pick just one word to use in all the description.<br/>

To find the set of synonyms we will use nlkt and then we are going to replace each word with the most common synonym of the other words.<br/>
For example:<br/>
planet -> {'major planet', 'planet', 'satellite',**'world'**}<br/>
world -> {'cosmos', 'earth','globe','human beings','macrocosm','man','mankind', 'populace','universe',**'world'**}<br/>
Earth -> {'dry land','earth','globe','ground','land',**'world'**}<br/>

As we can see world is present in all three cases so we are going to replace planet and Earth with world.<br/>

In case of Inception the result will be:<br/>
'someone fortune espionage mark subconscious spirit job requital origin stealer implantation mind'<br/>

### Term Frequency Inverse Document Frequency
We are going to trasform each word in a column and the value will be the frequency of that word within the sentence.<br/>
As a result we get a vector of numbers.<br/>

## Apply the cosine similarity and get the most similar movies

Now given a movies we will get the corresponding vector and then we will find the closest vectors by using the cosine similarity criteria.<br/>
The decoding to retrive the movies will be easy as we can use the position of the rows.<br/>

So in case of inception the movies recommended are:<br/>
622                   Body of Lies<br/>
1380      The Man in the Iron Mask<br/>
1701    Once Upon a Time in Mexico<br/>
914           Central Intelligence<br/>

The result is good as it fits pretty well with Inceptio.n<br/>

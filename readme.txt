Name: Michael Pedersen
Date: 2/22/2016

My A* implementation was basically a copy of my Uniform Cost Search with the heuristic function taking the place of the cost field.

I had a fair bit of trouble finding out how to allow my A* and Breadth First Search functions to accept the input from the prior questions (1-4) while still retaining the state information for the corner search heuristic. I tried to convert A* into using a hashmap as the state so I could arbitrarily throw in new data but I couldn't find an elegant way to do so while keeping backwards compadibility. Specifically it was exploding the successors into their fields that tripped me up. Overall, the only field that doesn't get modified in either Breadth or A* is location so, somewhat haphazardly, I can piggyback the corner state data on the first state field. In retrospect I had used the name "location" as that field's name in my search functions that it took me a while to realize that it was suppose to be the general state variable, not just location.

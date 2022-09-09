
## Submission Specification
- Your code should be written in either Matlab, Python, or C++.
- Please upload your code to a public github repository for us to review
- Please document your code. The more readable your code is the better you can show your coding skills.
- Please include a README that contains the following:
    - answer.png
    - Methodology 
    - What did you try and why do you think it did not work.
    - What libraries are used

## Image Location

The image my program produces gets saved in the same directory that the program is run in, titled "answer.png." I just renamed the original answer.png to sampleAnswer.png

Link to it [here](https://github.com/noahlessard/Wisconsin-Autonomous-Perception-Coding-Challenge/blob/main/perception/answer.png).

If you want to run the python code yourself, install the librarys and run

'''python3 detect.py'''

## Methodology

I wrote this in a couple hours, but I think it still displays my knowledge well and fulfills all the tasks required by the
question. If it is not fulfilling all the requirements, please let me know and I'll work on it some more!!

Looking at this image with the experience I had in CV in the past, I intuitively thought that this task would not be work making
a image detection model for, since the cones are already a specific case and they are very small. For the object detection 
models that I am capable of making, I don't think they could find an object with that low of resolution. So instead, I 
decided to just use a color mask, filtering for the color of orange that the cones were (I just used a color picker online to find those values). I also applied a bit of a blur, noise removal, and added a circular mask to limit the amount of information
that the color decector had to work with. The circle mask idea came from the point of focus in biological eyes... animals don't need to see everything in their vision, just what is directly ahead of them. Maybe this is silly, but it seemed to help in this test case of navigation.

There is a step by step explanation of the code in the comment of detect.py... Please read it!!

## What I tried / What didn't work
The hardest part of this challenge for me was figuring out how to make the program draw lines between
the points in a vertical way, not just playing connect the dots and doing zig-zags everywhere. I tried a lot
of solutions trying to group them based on their x positions, like splitting the screen in half and stuff, but
that just felt weird. Like what would happen if the robot moved too much and then the splitting the screen method
didn't work anymore? I had a big realization when I realized I could just sort the points by their x values... 
That seemed to be the best solution that I knew how to do. I think the only problem is the points at the top. I had
to make an if statement that just doesn't draw the line if the points are too far apart in the x direction, to avoid making
rectangles. It does work with the test image, but I'm not sure how it would work with other images. But I can't think of 
another way to do it, so it stays for now.


## What Libraries I used
I used python-opencv, version 2, to do most of the image manipluation, countour drawing, and masking.
I used numpy to do some array operations
I used os in order to help with finding the correct location to read/save images

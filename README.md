## YouTube Heatmap

# Idea
Go through a channel and create a heatmap for which day in the week they upload most often. To extend this, you could click the day and get an hour by hour overview of when they most often upload. 

Alternatively, the overview could look like Google Calendars 7-day view where you could scroll down and see which hours of the day they most often upload.

**Issues that will arise**
* Which timezone to use


# Tools
* [YouTube API](https://developers.google.com/youtube/v3/docs/)
* [youtube-python](https://pypi.org/project/youtube-python/)
* matplotlib (for heatmap)
    * [Different colormaps](https://matplotlib.org/tutorials/colors/colormaps.html)
    * [Seaborn for easy heatmap](https://seaborn.pydata.org/generated/seaborn.heatmap.html)




# Implementation
The data should be organized in a matrix/plane with day of week (0..6) as x-axis and time of day in hours (0..23) as y-axis. The values at each point should be the probability (0..1) that the youtuber uploads at that time of day on that day of the week. 

The probablilty decides the intensity/color of the heatmap at that point. 
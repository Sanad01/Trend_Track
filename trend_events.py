from datetime import datetime, timedelta
import math

# Defines an error for dates that are in the past
# Returns nothing because this class is used to raise a custom exception
class PastDateError(Exception):
    pass


# Class: TrendEvent
#
# Purpose:
#      Represents a general event by storing the event title source name date
#      and interest score. The class provides common functions for changing
#      the event date updating the interest score checking the time until the
#      event and displaying the event information
#
# Relationships:
#      TrendEvent is the base class for MusicEvent GamingEsportsEvent and
#      StreamingCreatorEvent. These derived classes inherit the common event
#      information and functions while adding their own event specific data
#
# Data Hiding:
#      The title source name event date and interest score are hidden using
#      private instance data members. These values are accessed and changed
#      through member functions such as reschedule and update_interest
class TrendEvent:
    # Initializes a TrendEvent with a title, source name, event date, and interest score
    # Raises TypeError if any argument has the wrong type
    # Raises ValueError if the title or source name is empty or the interest score is out of range
    # Returns None
    def __init__(self, title: str, source_name: str, event_date: datetime, interest_score: int):
         # Type checking
        if not isinstance(title, str):
            raise TypeError("title must be a string")

        if not isinstance(source_name, str):
            raise TypeError("source_name must be a string")

        if not isinstance(event_date, datetime):
            raise TypeError("event_date must be a datetime")

        if not isinstance(interest_score, (int, float)):
            raise TypeError("interest_score must be a number")

        # Value checking
        if not title:
            raise ValueError("title cannot be empty")

        if not source_name:
            raise ValueError("source_name cannot be empty")

        if interest_score <= 0 or interest_score >= 10:
            raise ValueError("interest_score must be between 1 and 10 inclusive")

        #make sure event is after the current hour
        current_hour = datetime.now().replace(
            minute=0,
            second=0,
            microsecond=0
            )

        if event_date <= current_hour:
            raise PastDateError("Event date must be after the current hour")

        self._title = title
        self._source_name = source_name
        self._date = event_date
        self._interest_score = interest_score


    # Changes the event date to a new date
    # Raises PastDateError if the new date is not later than the current hour
    # Returns True if the event date is changed successfully
    def reschedule(self, new_date: datetime) -> bool:
        #get the hour the event starts
        current_hour = self._date.replace(minute = 0, second = 0, microsecond = 0)

        next_hour = current_hour + timedelta(hours=1)

        if new_date < next_hour:
            raise PastDateError(
                "New date must be an hour later than the current hour"
            )

        self._date = new_date
        return True


    # Updates the interest score to a new value.
    # Raises TypeError if the new score is not an integer.
    # Raises ValueError if the new score is not between 0 and 10.
    # Returns None
    def update_interest(self, new_score: int): 
        if not isinstance(new_score, int):
            raise TypeError("New score must be an integer")

        if new_score <= 0 or new_score > 10:
            raise ValueError("New score must be between 0 and 10 inclusive")

        self._interest_score = new_score
        return True


    # Calculates the time remaining until the event
    # Raises TypeError if reference_date is not a datetime object
    # Raises PastDateError if the event has already occurred
    # Returns a timedelta showing the time until the event
    def time_until_event(self, reference_date: datetime) -> timedelta:
        if not isinstance(reference_date, datetime):
            raise TypeError("Reference date must be a datetime object")

        if self._date < reference_date:
            raise PastDateError("Event has already occurred")

        return self._date - reference_date


    # Creates a string that shows the event information
    # Returns a string containing the title, source, date, and interest score
    def __str__(self):
        return (
            f"Title: {self._title}, "
            f"Source: {self._source_name}, "
            f"Date: {self._date}, "
            f"Interest Score: {self._interest_score}"
        )

    # Compares the event date with another TrendEvent
    # Raises TypeError if other is not a TrendEvent
    # Returns True if this event happens before the other event and False otherwise
    def __lt__(self, other):
        if not isinstance(other, TrendEvent):
            raise TypeError("other must be a TrendEvent")

        return self._date < other._date

    # Compares this event with another TrendEvent using the event date and title
    # Returns True if both events have the same date and title and False otherwise
    def __eq__(self, other):
        if not isinstance(other, TrendEvent):
            return False

        return (
            self._date == other._date
            and self._title.strip().lower() == other._title.strip().lower()
        )



'''
____________________________________________________________________________
____________________________________________________________________________
                                MusicEvent
____________________________________________________________________________
____________________________________________________________________________
'''
# Class: MusicEvent
#
# Purpose:
#      Represents a music event by storing the artist venue ticket price and
#      playlist tags along with the general event information inherited from
#      TrendEvent. The class provides functions for adding playlist tags
#      estimating the total cost checking the budget and changing the venue
#
# Relationships:
#      MusicEvent inherits from TrendEvent and uses its common event
#      information and functions. It adds music specific information such as
#      the artist venue ticket price and playlist tags
#
# Data Hiding:
#      The artist venue ticket price and playlist tags are stored in private
#      instance data members. These values are accessed and changed through
#      member functions such as add_playlist_tag and change_venue
class MusicEvent(TrendEvent):
    # Initializes a MusicEvent with music event information
    # Raises TypeError if any argument has the wrong type
    # Raises ValueError if any string is empty, 
    # the ticket price is negative, or a playlist tag is empty
    # Returns None
    def __init__(
        self,
        title,
        source_name,
        event_date,
        interest_score,
        artist,
        venue,
        ticket_price,
        playlist_tags
    ):
        super().__init__(
            title,
            source_name,
            event_date,
            interest_score
        )

        normalized_tags = []

        # Artist validation
        if not isinstance(artist, str):
            raise TypeError("artist must be a string")
        if artist == "":
            raise ValueError("artist cannot be empty")

        # Venue validation
        if not isinstance(venue, str):
            raise TypeError("venue must be a string")
        if venue == "":
            raise ValueError("venue cannot be empty")

        # Ticket price validation
        if not isinstance(ticket_price, (int, float)):
            raise TypeError("ticket_price must be a number")
        if ticket_price < 0:
            raise ValueError("ticket_price cannot be negative")

        # Playlist tags validation
        if not isinstance(playlist_tags, list):
            raise TypeError("playlist_tags must be a list")

        for tag in playlist_tags:
            if not isinstance(tag, str):
                raise TypeError("each playlist tag must be a string")
            if tag == "":
                raise ValueError("playlist tags cannot contain empty strings")

            normalized_tags.append(tag.strip().lower())

        self._artist = artist
        self._venue = venue
        self._ticket_price = ticket_price
        self._playlist_tags = normalized_tags


    # Adds a new tag to the playlist tag list
    # Raises TypeError if the tag is not a string
    # Raises ValueError if the tag is empty or already in the list
    # Returns True if the tag is added successfully
    def add_playlist_tag(self, tag: str):

        if not isinstance(tag, str):
            raise TypeError("tag needs to be a string")

        tag = tag.strip().lower()

        if tag == "":
            raise ValueError("playlist tag cannot contain empty strings")

        if tag in self._playlist_tags:
            raise ValueError("tag is already in there")

        self._playlist_tags.append(tag)

        return True


    # Calculates the total cost of the event including travel cost
    # Raises TypeError if travel_cost is not a number
    # Raises ValueError if travel_cost is negative
    # Returns the total cost as a number
    def estimate_total_cost(self, travel_cost):
        if not isinstance(travel_cost, (int, float)):
            raise TypeError("Travel cost has to be a number")

        if travel_cost < 0:
            raise ValueError("Travel cost can't be negative")

        return travel_cost + self._ticket_price


    # Checks if the event can fit within the given budget
    # Raises TypeError if budget is not a number
    # Raises ValueError if budget is negative
    # Returns True if the budget covers the travel cost and False otherwise
    def is_affordable(self, budget: int, travel_cost: int) -> bool:

        if not isinstance(budget, (int, float)):
            raise TypeError("Budget has to be a number")

        if not isinstance(travel_cost, int):
            raise TypeError("Travel cost has to be an integer")

        if budget < 0:
            raise ValueError("Budget can't be negative")

        if travel_cost < 0:
            raise ValueError("Travel cost can't be negative")

        return budget >= travel_cost


    # Changes the event venue to a new venue
    # Raises TypeError if new_venue is not a string
    # Raises ValueError if new_venue is empty
    # Returns True if the venue is changed successfully
    def change_venue(self, new_venue: str):
        if not isinstance(new_venue, str):
            raise TypeError("new_venue must be a string")

        if new_venue == "":
            raise ValueError("new_venue cannot be empty")

        self._venue = new_venue
        return True


    # Creates a string that shows all the music event information
    # Returns a string containing the event details, artist, venue, ticket price, and playlist tags
    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"Artist: {self._artist}, "
            f"Venue: {self._venue}, "
            f"Ticket Price: ${self._ticket_price:.2f}, "
            f"Playlist Tags: {self._playlist_tags}"
        )


'''
____________________________________________________________________________
____________________________________________________________________________
                                GamingEsportsEvent
____________________________________________________________________________
____________________________________________________________________________
'''
# Class: GamingEsportsEvent
#
# Purpose:
#      Represents a gaming or esports event by storing the game title teams or
#      creators prize pool platforms and estimated viewers along with the
#      general event information inherited from TrendEvent. The class provides
#      functions for adding platforms checking if the event is major updating
#      the prize pool and calculating the hype index
#
# Relationships:
#      GamingEsportsEvent inherits from TrendEvent and uses its common event
#      information and functions. It adds gaming and esports specific
#      information such as the game title teams or creators prize pool
#      platforms and estimated viewers
#
# Data Hiding:
#      The game title teams or creators prize pool platforms and estimated
#      viewers are stored in private instance data members. These values are
#      accessed and changed through member functions such as add_platform and
#      update_prize_pool
class GamingEsportsEvent(TrendEvent):
    # Initializes a GamingEsportsEvent with gaming event information
    # Raises TypeError if an argument has the wrong type
    # Raises ValueError if a required string or list is empty or a number is invalid
    # Returns None
    def __init__(
        self,
        title,
        source_name,
        event_date,
        interest_score,
        game_title,
        teams_or_creators,
        prize_pool,
        platforms,
        estimated_viewers
    ):
        super().__init__(
            title,
            source_name,
            event_date,
            interest_score
        )

        # Game title validation
        if not isinstance(game_title, str):
            raise TypeError("game_title must be a string")

        if game_title == "":
            raise ValueError("game_title cannot be empty")

        # Teams or creators validation
        if not isinstance(teams_or_creators, list):
            raise TypeError("teams_or_creators must be a list")

        if len(teams_or_creators) == 0:
            raise ValueError("teams_or_creators cannot be empty")

        for entry in teams_or_creators:
            if not isinstance(entry, str):
                raise TypeError(
                    "each team or creator must be a string"
                )

            if entry == "":
                raise ValueError(
                    "team or creator cannot be empty"
                )

        # Prize pool validation
        if not isinstance(prize_pool, int):
            raise TypeError("prize_pool must be an integer")

        if prize_pool < 0:
            raise ValueError("prize_pool cannot be negative")

        # Platforms validation and normalization
        if not isinstance(platforms, list):
            raise TypeError("platforms must be a list")

        if len(platforms) == 0:
            raise ValueError("platforms cannot be empty")

        normalized_platforms = []

        for platform in platforms:
            if not isinstance(platform, str):
                raise TypeError(
                    "each platform must be a string"
                )

            if not platform.strip():
                raise ValueError(
                    "platform cannot be empty"
                )

            normalized_platforms.append(
                platform.strip().lower()
            )

        # Estimated viewers validation
        if not isinstance(estimated_viewers, int):
            raise TypeError(
                "estimated_viewers must be an integer"
            )

        if estimated_viewers <= 0:
            raise ValueError(
                "estimated_viewers must be greater than 0"
            )

        self._game_title = game_title
        self._teams_or_creators = teams_or_creators
        self._prize_pool = prize_pool
        self._platforms = normalized_platforms
        self._estimated_viewers = estimated_viewers


    # Adds a new platform to the list of platforms
    # Raises TypeError if platform is not a string
    # Raises ValueError if platform is empty or already exists
    # Returns True if the platform is added successfully
    def add_platform(self, platform: str):
        if not isinstance(platform, str):
            raise TypeError("Platform must be a string")

        platform = platform.strip().lower()

        if platform == "":
            raise ValueError("platform cannot be empty")

        if platform in self._platforms:
            raise ValueError("Platform already exists")

        self._platforms.append(platform)
        return True


    # Checks if the prize pool meets the given threshold for a major event
    # Raises TypeError if threshold is not an integer
    # Raises ValueError if threshold is not greater than 0
    # Returns True if the prize pool meets or exceeds the threshold and False otherwise
    def qualifies_as_major(self, threshold: int):
        if not isinstance(threshold, int):
            raise TypeError("threshold must be an integer")

        if threshold <= 0:
            raise ValueError("threshold must be greater than 0")

        return self._prize_pool >= threshold


    # Updates the prize pool to a new amount
    # Raises TypeError if amount is not an integer
    # Raises ValueError if amount is negative
    # Returns True if the prize pool is updated successfully
    def update_prize_pool(self, amount: int):
        if not isinstance(amount, int):
            raise TypeError("Amount must be an int")

        if amount < 0:
            raise ValueError("Amount can't be negative")

        self._prize_pool = amount
        return True


    # Calculates the hype index based on the estimated number of viewers
    # Returns the hype index as a number
    def calculate_hype_index(self):
        return math.log10(self._estimated_viewers)


    # Creates a string that shows all the gaming event information
    # Returns a string containing the event details, game title, teams or 
    # creators, prize pool, platforms, and estimated viewers
    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"Game Title: {self._game_title}, "
            f"Teams/Creators: {self._teams_or_creators}, "
            f"Prize Pool: ${self._prize_pool}, "
            f"Platforms: {self._platforms}, "
            f"Estimated Viewers: {self._estimated_viewers}"
        )


'''
____________________________________________________________________________
____________________________________________________________________________
                                StreamingCreatorEvent
____________________________________________________________________________
____________________________________________________________________________
'''
# Class: StreamingCreatorEvent
#
# Purpose:
#      Represents a streaming or creator event by storing the creator or studio
#      content format episode count and runtime along with the general event
#      information inherited from TrendEvent. The class provides functions for
#      calculating the total binge time adding episodes and changing the
#      content format
#
# Relationships:
#      StreamingCreatorEvent inherits from TrendEvent and uses its common event
#      information and functions. It adds streaming and creator specific
#      information such as the creator or studio content format episode count
#      and runtime
#
# Data Hiding:
#      The creator or studio content format episode count and runtime are stored
#      in private instance data members. These values are accessed and changed
#      through member functions such as add_episode and change_format
class StreamingCreatorEvent(TrendEvent):
    # Initializes a StreamingCreatorEvent with creator or studio,
    # content format, episode count, and runtime information
    # Raises TypeError if an argument has the wrong type
    # Raises ValueError if a string is empty or a number is not greater than 0
    def __init__(
        self,
        title,
        source_name,
        event_date,
        interest_score,
        creator_or_studio,
        content_format,
        episode_count,
        runtime_minutes
    ):
        super().__init__(
            title,
            source_name,
            event_date,
            interest_score
        )

        # Creator or studio validation
        if not isinstance(creator_or_studio, str):
            raise TypeError("creator_or_studio must be a string")
        if creator_or_studio == "":
            raise ValueError("creator_or_studio cannot be empty")

        # Content format validation
        if not isinstance(content_format, str):
            raise TypeError("content_format must be a string")
        if content_format == "":
            raise ValueError("content_format cannot be empty")

        # Episode count validation
        if not isinstance(episode_count, int):
            raise TypeError("episode_count must be an integer")
        if episode_count <= 0:
            raise ValueError("episode_count must be greater than 0")

        # Runtime validation
        if not isinstance(runtime_minutes, int):
            raise TypeError("runtime_minutes must be an integer")
        if runtime_minutes <= 0:
            raise ValueError("runtime_minutes must be greater than 0")

        self._creator_or_studio = creator_or_studio
        self._content_format = content_format
        self._episode_count = episode_count
        self._runtime_minutes = runtime_minutes

    # Calculates the total time needed to watch all episodes
    # Returns a timedelta showing the total binge time
    def calc_binge_time(self):
        total_minutes = self._runtime_minutes * self._episode_count
        #could probably just return an int but this is more future proof
        return timedelta(minutes = total_minutes)


    # Adds one episode to the episode count
    # Returns True if the episode count is increased successfully
    def add_episode(self):
        self._episode_count += 1
        return True


    # Changes the content format to a new format
    # Raises TypeError if new_format is not a string
    # Raises ValueError if new_format is empty
    # Returns True if the content format is changed successfully
    def change_format(self, new_format):
        if not isinstance(new_format, str):
            raise TypeError("new_format must be a string")

        if new_format == "":
            raise ValueError("new_format cannot be empty")

        self._content_format = new_format
        return True


# Creates a string that shows all the streaming creator event information
# Returns a string containing the event details, 
# creator or studio, content format, episode count, runtime, and binge time
    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"Creator/Studio: {self._creator_or_studio}, "
            f"Content Format: {self._content_format}, "
            f"Episode Count: {self._episode_count}, "
            f"Runtime: {self._runtime_minutes} minutes, "
            f"Binge Time: {self.calc_binge_time()}"
        )


'''
____________________________________________________________________________
____________________________________________________________________________
                                Operator Overloads
____________________________________________________________________________
____________________________________________________________________________
'''

#will be implemented to add an event to the tree in prog5
def __add__(self, other):
    pass
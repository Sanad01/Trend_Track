#trend_track_app.py
#Sanad Samara
#CS302-001
#program 5 and 4
#08/21/2026

from trend_events_samara import TrendEvent, MusicEvent, GamingEsportsEvent, StreamingCreatorEvent, PastDateError
from TwoThreeTree_samara import TwoThreeTree
from datetime import datetime


# Class: TrendTrackApp
#
# Purpose:
#      Manages the TrendTrack application by storing events in the 2-3 tree
#      and providing functions to create find edit and display events. The
#      class also controls the application menu and allows the user to exit
#
# Relationships:
#      TrendTrackApp contains a TwoThreeTree to store TrendEvent objects. It
#      works with MusicEvent GamingEsportsEvent and StreamingCreatorEvent
#      objects to create and manage different types of events
#
# Data Hiding:
#      The event collection and running status are hidden using private
#      instance data members. These values are managed through member
#      functions such as run create_event edit_event and exit
class TrendTrackApp:
    # Initializes the app with an empty event collection and sets the app to not running
    def __init__(self):
        self._event_collection = TwoThreeTree()
        self._running = False

    # Starts the application and keeps showing the menu until the user exits
    def run(self):
        # Start the application
        self._running = True

        # Continue showing the menu until the user exits
        while self._running:
            self.display_menu()

        return True

    # Displays the menu and handles the user's choice
    def display_menu(self):
        print("\n--- TrendTrack ---")
        print("1- Display all events")
        print("2- Create an event")
        print("3- Find an event")
        print("4- Edit event")
        print("5- Exit")

        try:
            # Get the user's menu choice
            choice = int(input("Enter your choice: "))

            if choice == 1:
                self.display_all_events()

            elif choice == 2:
                self.create_event()

            elif choice == 3:
                title = input("Enter event title: ")

                date_input = input(
                    "Enter event date and time (YYYY-MM-DD HH:MM): "
                )

                date = datetime.strptime(
                    date_input,
                    "%Y-%m-%d %H:%M"
                )

                self.find_event(title, date)

            elif choice == 4:
                self.edit_event()

            elif choice == 5:
                self.exit()

            else:
                print("Invalid choice. Please choose 1-5.")

        except (ValueError, TypeError) as error:
            print(f"Invalid input: {error}")

    # Displays all events in order or shows a message if there are no events
    def display_all_events(self):
        if self._event_collection.count() == 0:
            print("There are no events to display.")
            return

        self._event_collection.display_in_order()

    # Finds an event using its title and date
    # Returns True if the event is found and False if it is not found
    def find_event(self, title: str, date: datetime):
        if not isinstance(title, str):
            raise TypeError("title must be a string")

        if not isinstance(date, datetime):
            raise TypeError("date must be a datetime")

        if title.strip() == "":
            raise ValueError("title cannot be empty")

        current_hour = datetime.now().replace(
            minute=0,
            second=0,
            microsecond=0
        )

        if date <= current_hour:
            raise PastDateError(
                "Event date must be after the current hour"
            )

        event = self._event_collection.retrieve(title, date)

        if event is None:
            return False

        print(event)
        return True

    # Creates a new event by getting the required information from the user
    # Creates the selected event type and adds it to the 2-3 tree
    # Returns True if the event is created successfully and False if it fails
    def create_event(self):
        # Display the available event types
        print("\nChoose an event type:")
        print("1- Music Event")
        print("2- Gaming/Esports Event")
        print("3- Streaming Creator Event")

        # Get the user's event type choice
        choice = input("Enter your choice: ")

        # Get information shared by all event types
        title = input("Title: ")
        source_name = input("Source name: ")

        # Get the event date and convert it from a string to a datetime
        date_input = input(
            "Event date and time (YYYY-MM-DD HH:MM): "
        )

        event_date = datetime.strptime(
            date_input,
            "%Y-%m-%d %H:%M"
        )

        # Interest score must be an integer
        interest_score = int(
            input("Interest score: ")
        )

        # Create a MusicEvent
        if choice == "1":

            # Get music event information
            artist = input("Artist: ")
            venue = input("Venue: ")

            ticket_price = float(
                input("Ticket price: ")
            )

            # Get playlist tags as a comma-separated string
            tags_input = input(
                "Playlist tags (separated by commas): "
            )

            # Convert the string into a list of tags
            playlist_tags = [
                tag.strip()
                for tag in tags_input.split(",")
            ]

            # Create the MusicEvent object
            event = MusicEvent(
                title,
                source_name,
                event_date,
                interest_score,
                artist,
                venue,
                ticket_price,
                playlist_tags
            )

        # Create a GamingEsportsEvent
        elif choice == "2":

            # Get gaming event information
            game_title = input("Game title: ")

            # Get teams or creators as a comma-separated list
            teams_input = input(
                "Teams or creators (separated by commas): "
            )

            # Convert the string into a list
            teams_or_creators = [
                team.strip()
                for team in teams_input.split(",")
            ]

            # Get the prize pool
            prize_pool = int(
                input("Prize pool: ")
            )

            # Get platforms as a comma-separated list
            platforms_input = input(
                "Platforms (separated by commas): "
            )

            # Convert the string into a list of platforms
            platforms = [
                platform.strip()
                for platform in platforms_input.split(",")
            ]

            # Get the estimated number of viewers
            estimated_viewers = int(
                input("Estimated viewers: ")
            )

            # Create the GamingEsportsEvent object
            event = GamingEsportsEvent(
                title,
                source_name,
                event_date,
                interest_score,
                game_title,
                teams_or_creators,
                prize_pool,
                platforms,
                estimated_viewers
            )

        # Create a StreamingCreatorEvent
        elif choice == "3":

            # Get streaming event information
            creator_or_studio = input(
                "Creator or studio: "
            )

            content_format = input(
                "Content format: "
            )

            # Get the number of episodes
            episode_count = int(
                input("Episode count: ")
            )

            # Get the runtime of each episode
            runtime_minutes = int(
                input("Runtime in minutes: ")
            )

            # Create the StreamingCreatorEvent object
            event = StreamingCreatorEvent(
                title,
                source_name,
                event_date,
                interest_score,
                creator_or_studio,
                content_format,
                episode_count,
                runtime_minutes
            )

        # Handle an invalid event type
        else:
            print("Invalid event type.")
            return False

        # Try to add the event to the 2-3 tree
        try:
            self._event_collection.insert(event)

        # A duplicate date and title cannot be inserted
        except ValueError:
            print(
                "An event with the same date and title "
                "already exists."
            )
            return False

        # Event was successfully created and inserted
        print("Event created successfully.")
        return True

    # Finds an event and lets the user edit information based on its event type
    # Returns True if the edit is completed and False if the event is not found or the input is invalid
    def edit_event(self):
        # Get the title of the event to edit
        title = input("Enter the event title: ")

        # Get the date of the event
        date_input = input(
            "Enter the event date and time (YYYY-MM-DD HH:MM): "
        )

        try:
            # Convert the user's date input into a datetime
            date = datetime.strptime(
                date_input,
                "%Y-%m-%d %H:%M"
            )

            # Find the event in the tree
            event = self._event_collection.retrieve(
                title,
                date
            )

            # Check if the event exists
            if event is None:
                print("Event not found.")
                return False

            # Display the MusicEvent submenu
            if isinstance(event, MusicEvent):
                while True:
                    print("\n--- Music Event ---")
                    print("1- Add playlist tag")
                    print("2- Change venue")
                    print("3- Display")
                    print("4- Back")

                    choice = input("Enter your choice: ")

                    try:
                        if choice == "1":
                            tag = input("Enter playlist tag: ")
                            event.add_playlist_tag(tag)
                            print("Playlist tag added.")

                        elif choice == "2":
                            venue = input("Enter new venue: ")
                            event.change_venue(venue)
                            print("Venue changed.")

                        elif choice == "3":
                            print(event)

                        elif choice == "4":
                            return True

                        else:
                            print("Invalid choice. Please choose 1-4.")

                    except (TypeError, ValueError) as error:
                        print(f"Invalid input: {error}")

            # Display the GamingEsportsEvent submenu
            elif isinstance(event, GamingEsportsEvent):
                while True:
                    print("\n--- Gaming/Esports Event ---")
                    print("1- Update prize pool")
                    print("2- Add platform")
                    print("3- Display")
                    print("4- Back")

                    choice = input("Enter your choice: ")

                    try:
                        if choice == "1":
                            prize_pool = int(
                                input("Enter new prize pool: ")
                            )

                            event.update_prize_pool(prize_pool)
                            print("Prize pool updated.")

                        elif choice == "2":
                            platform = input(
                                "Enter platform: "
                            )

                            event.add_platform(platform)
                            print("Platform added.")

                        elif choice == "3":
                            print(event)

                        elif choice == "4":
                            return True

                        else:
                            print("Invalid choice. Please choose 1-4.")

                    except (TypeError, ValueError) as error:
                        print(f"Invalid input: {error}")

            # Display the StreamingCreatorEvent submenu
            elif isinstance(event, StreamingCreatorEvent):
                while True:
                    print("\n--- Streaming Creator Event ---")
                    print("1- Add episode")
                    print("2- Change format")
                    print("3- Display")
                    print("4- Back")

                    choice = input("Enter your choice: ")

                    try:
                        if choice == "1":
                            event.add_episode()
                            print("Episode added.")

                        elif choice == "2":
                            content_format = input(
                                "Enter new content format: "
                            )

                            event.change_format(content_format)
                            print("Format changed.")

                        elif choice == "3":
                            print(event)

                        elif choice == "4":
                            return True

                        else:
                            print("Invalid choice. Please choose 1-4.")

                    except (TypeError, ValueError) as error:
                        print(f"Invalid input: {error}")

            return True

        except (TypeError, ValueError) as error:
            print(f"Invalid input: {error}")
            return False


    # Adds an event to the event collection
    # Returns True if the event is added and False if it is a duplicate
    def __add__(self, event):
        # Make sure the value being added is a TrendEvent
        if not isinstance(event, TrendEvent):
            raise TypeError("event must be a TrendEvent")

        # Try to add the event to the tree
        try:
            self._event_collection.insert(event)

        # Duplicate date and title
        except ValueError:
            return False

        return True

    # Stops the application from running
    # Returns True when the application is stopped
    def exit(self):
        self._running = False
        return True
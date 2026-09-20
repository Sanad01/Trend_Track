import pytest
from datetime import datetime, timedelta
from trend_events_samara import TrendEvent, MusicEvent, GamingEsportsEvent, StreamingCreatorEvent, PastDateError
from trend_track_app_samara import TrendTrackApp

'''
-------------------------------------------------------
-------------------------------------------------------
            tests for TrendEvent
-------------------------------------------------------
-------------------------------------------------------
'''

# constructor tests
@pytest.fixture
def sample_date():
    return datetime(2026, 12, 30, 6, 10, 0)

@pytest.fixture
def next_hour():
        current_time = datetime.now()
    #set current time to hour:0:0 then add one to hour to that
        next_hour = current_time.replace(
            minute=0, second=0) + timedelta(hours=1)

        return next_hour

@pytest.fixture
def past_date():
        current_time = datetime.now()
        #subtract one from current day
        date = current_time.replace() - timedelta(days=1)
        return date

def test_trend_event_constructor(sample_date):
    event = TrendEvent("test event", "test source", sample_date, 2)
    assert event._title == "test event"
    assert event._source_name == "test source"
    assert event._date == sample_date
    assert event._interest_score == 2

def test_trend_event_constructor_empty_title(sample_date):
    with pytest.raises(ValueError):
        TrendEvent("", "test source", sample_date, 2)

def test_trend_event_constructor_empty_source(sample_date):
    with pytest.raises(ValueError):
        TrendEvent("test event", "", sample_date, 2)



def test_trend_event_constructor_next_hour(next_hour):
    event = TrendEvent(
        "test event",
        "test source",
        next_hour,
        5
    )
    assert event._date == next_hour

def test_trend_event_constructor_score_not_in_range(sample_date):
    with pytest.raises(ValueError):
        TrendEvent("test event", "test source", sample_date, 0)

    with pytest.raises(ValueError):
        TrendEvent("test event", "test source", sample_date, 11)


#test reschedule
@pytest.fixture
def sample_event(sample_date):
    event = TrendEvent("test event", "test source", sample_date, 2)
    return event

def test_reschedule_valid_date(sample_event):
    new_date = datetime(2026, 12, 30, 7, 10, 0)
    assert sample_event.reschedule(new_date) == True
    assert sample_event._date == new_date


def test_reschedule_current_hour(sample_event, past_date):
    original_date = sample_event._date

    with pytest.raises(PastDateError):
        sample_event.reschedule(past_date)

    # make sure date didn't change
    assert sample_event._date == original_date


#test update_interest
@pytest.mark.parametrize("score", [1, 10])
def test_update_interest_boundary(sample_event, score):
    assert sample_event.update_interest(score) == True
    assert sample_event._interest_score == score

@pytest.mark.parametrize("score", [0, 11])
def test_update_interest_out_of_range(sample_event, score):
    original_score = sample_event._interest_score

    with pytest.raises(ValueError):
        sample_event.update_interest(score)
    # make sure score didn't change
    assert sample_event._interest_score == original_score

@pytest.mark.parametrize("score", [5.5, "5"])
def test_update_interest_not_integer(sample_event, score):
    original_score = sample_event._interest_score

    with pytest.raises(TypeError):
        sample_event.update_interest(score)
    # make sure score didn't change
    assert sample_event._interest_score == original_score

def test_update_interest_valid(sample_event):
    assert sample_event.update_interest(7) == True
    assert sample_event._interest_score == 7


#test time_until_event
def test_time_until_event_valid(sample_event):
    reference_date = datetime(2026, 12, 30, 5, 10, 0) #hour before event
    expected = timedelta(hours=1)

    # checks if the difference is one hour
    assert sample_event.time_until_event(reference_date) == expected

def test_time_until_event_past_event(sample_event):
    reference_date = datetime(2026, 12, 30, 7, 10, 0) # hour after

    with pytest.raises(PastDateError):
        sample_event.time_until_event(reference_date)

@pytest.mark.parametrize("reference_date", [
    "2026-12-30 5:10",
    123,
    None
])
def test_time_until_event_invalid_type(sample_event, reference_date):
    with pytest.raises(TypeError):
        sample_event.time_until_event(reference_date)
    
def test_time_until_event_same_date(sample_event, sample_date):
    reference_date = sample_date

    assert sample_event.time_until_event(reference_date) == timedelta(0)


#test __str__()
def test_trend_event_str(sample_event, sample_date):
    expected = (
        f"Title: test event, "
        f"Source: test source, "
        f"Date: {sample_date}, "
        f"Interest Score: 2"
    )

    assert str(sample_event) == expected


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for MusicEvent
-------------------------------------------------------
-------------------------------------------------------
'''

@pytest.fixture
def sample_music_event(sample_date):
    return MusicEvent(
        "test event",
        "test source",
        sample_date,
        5,
        "Test Artist",
        "Test Venue",
        25,
        ["rock", "indie"]
    )

def test_music_event_constructor(sample_date):
    event = MusicEvent(
        "test event",
        "test source",
        sample_date,
        5,
        "Test Artist",
        "Test Venue",
        25,
        ["rock", "indie"]
    )

    assert event._title == "test event"
    assert event._source_name == "test source"
    assert event._date == sample_date
    assert event._interest_score == 5
    assert event._artist == "Test Artist"
    assert event._venue == "Test Venue"
    assert event._ticket_price == 25.00
    assert event._playlist_tags == ["rock", "indie"]

def test_music_event_empty_artist(sample_date):
    with pytest.raises(ValueError):
        event = MusicEvent(
            "test event",
            "test source",
            sample_date,
            5,
            "",
            "Test Venue",
            25,
            ["rock", "indie"]
        )

def test_music_event_empty_venue(sample_date):
    with pytest.raises(ValueError):
        event = MusicEvent(
            "test event",
            "test source",
            sample_date,
            5,
            "Test Artist",
            "",
            25,
            ["rock", "indie"]
        )

def test_music_event_free_ticket(sample_date):
    event = MusicEvent(
        "test event",
        "test source",
        sample_date,
        5,
        "Test Artist",
        "Test Venue",
        0.00,
        ["rock", "indie"]
    )

def test_music_event_negative_ticket_price(sample_date):
    with pytest.raises(ValueError):
        event = MusicEvent(
            "test event",
            "test source",
            sample_date,
            5,
            "Test Artist",
            "Test Venue",
            -1.00,
            ["rock", "indie"]
        )

def test_music_event_empty_playlist_tags(sample_date):
    event = MusicEvent(
        "test event",
        "test source",
        sample_date,
        5,
        "Test Artist",
        "Test Venue",
        25.00,
        []
    )

@pytest.mark.parametrize("tags", [
    ["rock", ""],
    ["", "indie"],
    [""]
])
def test_music_event_invalid_playlist_tags(sample_date, tags):
    with pytest.raises(ValueError):
        MusicEvent(
            "test event",
            "test source",
            sample_date,
            5,
            "Test Artist",
            "Test Venue",
            25.00,
            tags
        )

def test_music_event_constructor_normalizes_tags(sample_date):
    event = MusicEvent(
        "test event",
        "test source",
        sample_date,
        5,
        "Test Artist",
        "Test Venue",
        25.00,
        [" Rock ", "INDIE", "  POP  "]
    )

    assert event._playlist_tags == ["rock", "indie", "pop"]

#add_playlist_tag tests
def test_add_playlist_tag_valid_tag(sample_music_event):
    assert sample_music_event.add_playlist_tag("test") == True
    assert "test" in sample_music_event._playlist_tags

def test_add_playlist_tag_empty_tag(sample_music_event):
    with pytest.raises(ValueError):
        sample_music_event.add_playlist_tag("")

@pytest.mark.parametrize("tags", [1, 2.0, None])
def test_add_playlist_tag_invalid_tag(sample_music_event, tags):
    with pytest.raises(TypeError):
        sample_music_event.add_playlist_tag(tags)

def test_add_playlist_tag_duplicate(sample_music_event):
    sample_music_event.add_playlist_tag("test")

    with pytest.raises(ValueError):
        sample_music_event.add_playlist_tag("test")

def test_add_playlist_tag_normalized(sample_music_event):
    assert sample_music_event.add_playlist_tag("  TEST  ") == True
    assert "test" in sample_music_event._playlist_tags


#estimate_total_cost tests
def test_estimate_total_cost(sample_music_event):
    assert sample_music_event.estimate_total_cost(10.00) == 35.00

def test_estimate_total_cost_zero_travel(sample_music_event):
    assert sample_music_event.estimate_total_cost(0.00) == 25.00

@pytest.mark.parametrize("travel_cost", [-1.00, -10.50])
def test_estimate_total_cost_negative(sample_music_event, travel_cost):
    with pytest.raises(ValueError):
        sample_music_event.estimate_total_cost(travel_cost)

@pytest.mark.parametrize("travel_cost", ["10", "free", None, [10]])
def test_estimate_total_cost_not_number(sample_music_event, travel_cost):
    with pytest.raises(TypeError):
        sample_music_event.estimate_total_cost(travel_cost)


#is_affordable tests
def test_is_affordable(sample_music_event):
    assert sample_music_event.is_affordable(40, 10) == True


def test_is_affordable_exact_budget(sample_music_event):
    assert sample_music_event.is_affordable(35, 35) == True


def test_is_not_affordable(sample_music_event):
    assert sample_music_event.is_affordable(30, 31) == False


@pytest.mark.parametrize("budget", [-1, -10])
def test_is_affordable_negative_budget(sample_music_event, budget):
    with pytest.raises(ValueError):
        sample_music_event.is_affordable(budget, 10)


@pytest.mark.parametrize("budget", ["40", None, [40]])
def test_is_affordable_invalid_budget(sample_music_event, budget):
    with pytest.raises(TypeError):
        sample_music_event.is_affordable(budget, 10)


@pytest.mark.parametrize("travel_cost", ["10", None, [10]])
def test_is_affordable_invalid_travel_cost(sample_music_event, travel_cost):
    with pytest.raises(TypeError):
        sample_music_event.is_affordable(40, travel_cost)


@pytest.mark.parametrize("travel_cost", [-1, -10])
def test_is_affordable_negative_travel_cost(sample_music_event, travel_cost):
    with pytest.raises(ValueError):
        sample_music_event.is_affordable(40.00, travel_cost)

#change_venue tests
def test_change_venue(sample_music_event):
    assert sample_music_event.change_venue("New Venue") == True
    assert sample_music_event._venue == "New Venue"

def test_change_venue_empty(sample_music_event):
    original_venue = sample_music_event._venue

    with pytest.raises(ValueError):
        sample_music_event.change_venue("")

    assert sample_music_event._venue == original_venue

@pytest.mark.parametrize("venue", [1, 2.0, None])
def test_change_venue_invalid_type(sample_music_event, venue):
    original_venue = sample_music_event._venue

    with pytest.raises(TypeError):
        sample_music_event.change_venue(venue)

    assert sample_music_event._venue == original_venue

#__str__() tests
def test_music_event_str(sample_music_event, sample_date):
    expected = (
        f"Title: test event, "
        f"Source: test source, "
        f"Date: {sample_date}, "
        f"Interest Score: 5, "
        f"Artist: Test Artist, "
        f"Venue: Test Venue, "
        f"Ticket Price: $25.00, "
        f"Playlist Tags: ['rock', 'indie']"
    )

    assert str(sample_music_event) == expected


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for GamingEsportsEvent
-------------------------------------------------------
-------------------------------------------------------
'''

#constructor tests
@pytest.fixture
def sample_gaming_event(sample_date):
    return GamingEsportsEvent(
        "Regional Valorant Cup",
        "GameSpot",
        sample_date,
        7,
        "Valorant",
        ["Sentinels", "NRG"],
        37500,
        ["Twitch", "YouTube"],
        68420
    )

def test_gaming_event_constructor(sample_date):
    event = GamingEsportsEvent(
        "Regional Valorant Cup",
        "GameSpot",
        sample_date,
        7,
        "Valorant",
        ["Sentinels", "NRG"],
        37500,
        ["Twitch", "YouTube"],
        68420
    )

    assert event._title == "Regional Valorant Cup"
    assert event._source_name == "GameSpot"
    assert event._date == sample_date
    assert event._interest_score == 7
    assert event._game_title == "Valorant"
    assert event._teams_or_creators == ["Sentinels", "NRG"]
    assert event._prize_pool == 37500
    assert event._platforms == ["twitch", "youtube"]
    assert event._estimated_viewers == 68420

def test_gaming_event_empty_game_title(sample_date):
    with pytest.raises(ValueError):
        GamingEsportsEvent(
            "Regional Valorant Cup",
            "GameSpot",
            sample_date,
            7,
            "",
            ["Sentinels", "NRG"],
            37500,
            ["Twitch", "YouTube"],
            68420
        )

@pytest.mark.parametrize("teams", [
    [],
    [""],
    ["Sentinels", ""]
])
def test_gaming_event_invalid_teams_or_creators(sample_date, teams):
    with pytest.raises(ValueError):
        GamingEsportsEvent(
            "Regional Valorant Cup",
            "GameSpot",
            sample_date,
            7,
            "Valorant",
            teams,
            37500,
            ["Twitch", "YouTube"],
            68420
        )

def test_gaming_event_zero_prize_pool(sample_date):
    event = GamingEsportsEvent(
        "Regional Valorant Cup",
        "GameSpot",
        sample_date,
        7,
        "Valorant",
        ["Sentinels", "NRG"],
        0,
        ["Twitch", "YouTube"],
        68420
    )

    assert event._prize_pool == 0

@pytest.mark.parametrize("prize_pool", [-1, -37500])
def test_gaming_event_negative_prize_pool(sample_date, prize_pool):
    with pytest.raises(ValueError):
        GamingEsportsEvent(
            "Regional Valorant Cup",
            "GameSpot",
            sample_date,
            7,
            "Valorant",
            ["Sentinels", "NRG"],
            prize_pool,
            ["Twitch", "YouTube"],
            68420
        )

@pytest.mark.parametrize("platforms", [
    [],
    [""],
    ["Twitch", ""]
])
def test_gaming_event_invalid_platforms(sample_date, platforms):
    with pytest.raises(ValueError):
        GamingEsportsEvent(
            "Regional Valorant Cup",
            "GameSpot",
            sample_date,
            7,
            "Valorant",
            ["Sentinels", "NRG"],
            37500,
            platforms,
            68420
        )

def test_gaming_event_one_estimated_viewer(sample_date):
    event = GamingEsportsEvent(
        "Regional Valorant Cup",
        "GameSpot",
        sample_date,
        7,
        "Valorant",
        ["Sentinels", "NRG"],
        37500,
        ["Twitch", "YouTube"],
        1
    )

    assert event._estimated_viewers == 1

@pytest.mark.parametrize("viewers", [0, -1])
def test_gaming_event_invalid_estimated_viewers(sample_date, viewers):
    with pytest.raises(ValueError):
        GamingEsportsEvent(
            "Regional Valorant Cup",
            "GameSpot",
            sample_date,
            7,
            "Valorant",
            ["Sentinels", "NRG"],
            37500,
            ["Twitch", "YouTube"],
            viewers
        )

#add_platform_tests
def test_add_platform_valid(sample_gaming_event):
    assert sample_gaming_event.add_platform("Discord") == True
    assert "discord" in sample_gaming_event._platforms

def test_add_platform_normalized(sample_gaming_event):
    assert sample_gaming_event.add_platform("  DISCORD  ") == True
    assert "discord" in sample_gaming_event._platforms

def test_add_platform_duplicate(sample_gaming_event):
    sample_gaming_event.add_platform("Discord")

    with pytest.raises(ValueError):
        sample_gaming_event.add_platform("Discord")

def test_add_platform_empty(sample_gaming_event):
    with pytest.raises(ValueError):
        sample_gaming_event.add_platform("")

@pytest.mark.parametrize("platform", [1, 2.5, None])
def test_add_platform_invalid_type(sample_gaming_event, platform):
    with pytest.raises(TypeError):
        sample_gaming_event.add_platform(platform)


#qualifies_as_major tests
#_prize_pool is 37500
def test_qualifies_as_major(sample_gaming_event):
    assert sample_gaming_event.qualifies_as_major(30000) == True


def test_qualifies_as_major_equal_threshold(sample_gaming_event):
    assert sample_gaming_event.qualifies_as_major(37500) == True


def test_does_not_qualify_as_major(sample_gaming_event):
    assert sample_gaming_event.qualifies_as_major(40000) == False


@pytest.mark.parametrize("threshold", [0, -1, -100])
def test_qualifies_as_major_invalid_threshold(sample_gaming_event, threshold):
    with pytest.raises(ValueError):
        sample_gaming_event.qualifies_as_major(threshold)


@pytest.mark.parametrize("threshold", [30000.0, "30000", None])
def test_qualifies_as_major_invalid_type(sample_gaming_event, threshold):
    with pytest.raises(TypeError):
        sample_gaming_event.qualifies_as_major(threshold)


#calculate_hype_index tests
from math import log10

def test_calculate_hype_index(sample_gaming_event):
    expected = log10(68420)

    assert sample_gaming_event.calculate_hype_index() == expected

def test_calculate_hype_index_one_viewer(sample_date):
    event = GamingEsportsEvent(
        "Regional Valorant Cup",
        "GameSpot",
        sample_date,
        7,
        "Valorant",
        ["Sentinels", "NRG"],
        37500,
        ["Twitch", "YouTube"],
        1
    )

    assert event.calculate_hype_index() == 0


#update_prize_pool tests
def test_update_prize_pool(sample_gaming_event):
    assert sample_gaming_event.update_prize_pool(42000) == True
    assert sample_gaming_event._prize_pool == 42000

def test_update_prize_pool_zero(sample_gaming_event):
    assert sample_gaming_event.update_prize_pool(0) == True
    assert sample_gaming_event._prize_pool == 0

@pytest.mark.parametrize("amount", [-1, -5000])
def test_update_prize_pool_negative(sample_gaming_event, amount):
    original_prize_pool = sample_gaming_event._prize_pool

    with pytest.raises(ValueError):
        sample_gaming_event.update_prize_pool(amount)

    assert sample_gaming_event._prize_pool == original_prize_pool

@pytest.mark.parametrize("amount", [42000.0, "42000", None])
def test_update_prize_pool_invalid_type(sample_gaming_event, amount):
    original_prize_pool = sample_gaming_event._prize_pool

    with pytest.raises(TypeError):
        sample_gaming_event.update_prize_pool(amount)

    assert sample_gaming_event._prize_pool == original_prize_pool


#__str__() tests
def test_gaming_event_str(sample_gaming_event, sample_date):
    expected = (
        f"Title: Regional Valorant Cup, "
        f"Source: GameSpot, "
        f"Date: {sample_date}, "
        f"Interest Score: 7, "
        f"Game Title: Valorant, "
        f"Teams/Creators: ['Sentinels', 'NRG'], "
        f"Prize Pool: $37500, "
        f"Platforms: ['twitch', 'youtube'], "
        f"Estimated Viewers: 68420"
    )

    assert str(sample_gaming_event) == expected


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for StreamingCreatorEvent
-------------------------------------------------------
-------------------------------------------------------
'''

#constructor tests
@pytest.fixture
def sample_streaming_event(sample_date):
    return StreamingCreatorEvent(
        "test",
        "Netflix",
        sample_date,
        6,
        "Netflix Studios",
        "Highlander",
        8,
        47
    )


def test_streaming_event_constructor(sample_date):
    event = StreamingCreatorEvent(
        "test",
        "Netflix",
        sample_date,
        6,
        "Netflix Studios",
        "Highlander",
        8,
        47
    )

    assert event._title == "test"
    assert event._source_name == "Netflix"
    assert event._date == sample_date
    assert event._interest_score == 6
    assert event._creator_or_studio == "Netflix Studios"
    assert event._content_format == "Highlander"
    assert event._episode_count == 8
    assert event._runtime_minutes == 47


def test_streaming_event_empty_creator(sample_date):
    with pytest.raises(ValueError):
        StreamingCreatorEvent(
            "test",
            "Netflix",
            sample_date,
            6,
            "",
            "Highlander",
            8,
            47
        )


def test_streaming_event_empty_content_format(sample_date):
    with pytest.raises(ValueError):
        StreamingCreatorEvent(
            "test",
            "Netflix",
            sample_date,
            6,
            "Netflix Studios",
            "",
            8,
            47
        )


def test_streaming_event_one_episode(sample_date):
    event = StreamingCreatorEvent(
        "test",
        "Netflix",
        sample_date,
        6,
        "Netflix Studios",
        "Highlander",
        1,
        47
    )

    assert event._episode_count == 1


@pytest.mark.parametrize("episode_count", [0, -1])
def test_streaming_event_invalid_episode_count(sample_date, episode_count):
    with pytest.raises(ValueError):
        StreamingCreatorEvent(
            "test",
            "Netflix",
            sample_date,
            6,
            "Netflix Studios",
            "Highlander",
            episode_count,
            47
        )


def test_streaming_event_one_minute_runtime(sample_date):
    event = StreamingCreatorEvent(
        "test",
        "Netflix",
        sample_date,
        6,
        "Netflix Studios",
        "Highlander",
        8,
        1
    )

    assert event._runtime_minutes == 1


@pytest.mark.parametrize("runtime", [0, -1])
def test_streaming_event_invalid_runtime(sample_date, runtime):
    with pytest.raises(ValueError):
        StreamingCreatorEvent(
            "test",
            "Netflix",
            sample_date,
            6,
            "Netflix Studios",
            "Highlander",
            8,
            runtime
        )


#calc_binge_time tests
def test_calc_binge_time(sample_streaming_event):
    expected = timedelta(minutes=8 * 47)

    assert sample_streaming_event.calc_binge_time() == expected


#add_episode tests
def test_add_episode(sample_streaming_event):
    original_count = sample_streaming_event._episode_count
    original_runtime = sample_streaming_event._runtime_minutes

    assert sample_streaming_event.add_episode() == True

    assert sample_streaming_event._episode_count == original_count + 1
    assert sample_streaming_event._runtime_minutes == original_runtime


#change_format tests
def test_change_format(sample_streaming_event):
    assert sample_streaming_event.change_format("Documentary") == True
    assert sample_streaming_event._content_format == "Documentary"

def test_change_format_empty(sample_streaming_event):
    original_format = sample_streaming_event._content_format

    with pytest.raises(ValueError):
        sample_streaming_event.change_format("")

    assert sample_streaming_event._content_format == original_format

@pytest.mark.parametrize("new_format", [1, 2.5, None])
def test_change_format_invalid_type(sample_streaming_event, new_format):
    original_format = sample_streaming_event._content_format

    with pytest.raises(TypeError):
        sample_streaming_event.change_format(new_format)

    assert sample_streaming_event._content_format == original_format


#__str__() test
def test_streaming_event_str(sample_streaming_event, sample_date):
    expected = (
        f"Title: test, "
        f"Source: Netflix, "
        f"Date: {sample_date}, "
        f"Interest Score: 6, "
        f"Creator/Studio: Netflix Studios, "
        f"Content Format: Highlander, "
        f"Episode Count: 8, "
        f"Runtime: 47 minutes, "
        f"Binge Time: {timedelta(minutes=8 * 47)}"
    )

    assert str(sample_streaming_event) == expected


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for TrendTrackApp
-------------------------------------------------------
-------------------------------------------------------
'''

@pytest.fixture
def app():
    return TrendTrackApp()


#constructor test
def test_trend_track_app_constructor(app):
    assert app._running == False
    assert app._event_collection.count() == 0


#find_event test
def test_find_event_found(app, sample_date):
    event = TrendEvent("test", "test source", sample_date, 5)
    app._event_collection.insert(event)

    assert app.find_event("test", sample_date) == True

def test_find_event_not_found(app, sample_date):
    assert app.find_event("test", sample_date) == False

def test_find_event_empty_title(app, sample_date):
    with pytest.raises(ValueError):
        app.find_event("", sample_date)

def test_find_event_past_date(app):
    past_date = datetime.now() - timedelta(hours=1)

    with pytest.raises(PastDateError):
        app.find_event("test", past_date)

@pytest.mark.parametrize("title", [1, 2.5, None])
def test_find_event_invalid_title_type(app, sample_date, title):
    with pytest.raises(TypeError):
        app.find_event(title, sample_date)

@pytest.mark.parametrize("date", ["2026-12-30", 123, None])
def test_find_event_invalid_date_type(app, sample_date, date):
    with pytest.raises(TypeError):
        app.find_event("test", date)

'''
Don't know how test methods that require user input like create event
and edit event, and run. I have heard of something called monkeypatch but there
wasn't enough time to learn that
'''


#exit test
def test_exit(app):
    app._running = True

    assert app.exit() == True
    assert app._running == False


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for Opertator Overloading
-------------------------------------------------------
-------------------------------------------------------
'''

# __lt__() tests
def test_trend_event_less_than():
    earlier = TrendEvent(
        "Event A",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    later = TrendEvent(
        "Event B",
        "source",
        datetime(2026, 10, 11, 12, 0),
        5
    )

    assert earlier < later
    assert not later < earlier

def test_trend_event_less_than_same_date():
    first = TrendEvent(
        "Alpha",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    second = TrendEvent(
        "Beta",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    assert (first < second) is False

@pytest.mark.parametrize("other", [1, "event", None, 2.5])
def test_trend_event_less_than_invalid_type(other):
    event = TrendEvent(
        "Event",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    with pytest.raises(TypeError):
        event < other


#__eq__() tests
def test_trend_event_equal():
    event1 = TrendEvent(
        "Test Event",
        "source1",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    event2 = TrendEvent(
        "Test Event",
        "source2",
        datetime(2026, 10, 10, 12, 0),
        8
    )

    assert event1 == event2

def test_trend_event_not_equal():
    event1 = TrendEvent(
        "Test Event",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    event2 = TrendEvent(
        "Different Event",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    assert event1 != event2

@pytest.mark.parametrize("other", [1, "event", None, 2.5])
def test_trend_event_equal_invalid_type(other):
    event = TrendEvent(
        "Test Event",
        "source",
        datetime(2026, 10, 10, 12, 0),
        5
    )

    assert event != other


# __add__() tests
def test_add_event(app, sample_date):
    event = TrendEvent(
        "Test Event",
        "Test Source",
        sample_date,
        5
    )

    assert (app + event) == True
    assert app._event_collection.count() == 1


def test_add_duplicate_event(app, sample_date):
    event = TrendEvent(
        "Test Event",
        "Test Source",
        sample_date,
        5
    )

    assert (app + event) == True
    assert (app + event) == False
    assert app._event_collection.count() == 1


@pytest.mark.parametrize("event", [1, 2.5, "event", None, []])
def test_add_invalid_event_type(app, event):
    with pytest.raises(TypeError):
        app + event


'''
-------------------------------------------------------
-------------------------------------------------------
            tests for TwoThreeTree
-------------------------------------------------------
-------------------------------------------------------
'''
from TwoThreeTree_samara import TwoThreeTreeNode, TwoThreeTree

@pytest.fixture
def tree_sample_date():
    return datetime(2026, 12, 30, 6, 10, 0)


@pytest.fixture
def tree_sample_event(tree_sample_date):
    return TrendEvent(
        "Tree Test Event",
        "Tree Test Source",
        tree_sample_date,
        5
    )


def test_two_three_tree_node_constructor(tree_sample_event):
    node = TwoThreeTreeNode(tree_sample_event)

    assert node.events == [tree_sample_event]
    assert node.children == []


def test_two_three_tree_constructor():
    tree = TwoThreeTree()

    assert tree._root is None


def test_two_three_tree_count_empty():
    tree = TwoThreeTree()

    assert tree.count() == 0

def test_two_three_tree_count_one_event(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    assert tree.count() == 1


def test_two_three_tree_count_multiple_events(tree_sample_event, tree_sample_date):
    tree = TwoThreeTree()

    second_event = TrendEvent(
        "Second Event",
        "source",
        datetime(2027, 1, 1, 12, 0, 0),
        5
    )

    third_event = TrendEvent(
        "Third Event",
        "source",
        datetime(2027, 2, 1, 12, 0, 0),
        5
    )

    tree.insert(tree_sample_event)
    tree.insert(second_event)
    tree.insert(third_event)

    assert tree.count() == 3


def test_two_three_tree_insert_empty(tree_sample_event):
    tree = TwoThreeTree()

    assert tree.insert(tree_sample_event) is True
    assert tree.count() == 1


def test_two_three_tree_insert_multiple(tree_sample_event):
    tree = TwoThreeTree()

    second_event = TrendEvent(
        "Second Event",
        "Tree Test Source",
        datetime(2027, 1, 1, 12, 0),
        5
    )

    tree.insert(tree_sample_event)
    tree.insert(second_event)

    assert tree.count() == 2


def test_two_three_tree_insert_split(tree_sample_event):
    tree = TwoThreeTree()

    second_event = TrendEvent(
        "Second Event",
        "Tree Test Source",
        datetime(2027, 1, 1, 12, 0),
        5
    )

    third_event = TrendEvent(
        "Third Event",
        "Tree Test Source",
        datetime(2027, 2, 1, 12, 0),
        5
    )

    tree.insert(tree_sample_event)
    tree.insert(second_event)
    tree.insert(third_event)

    assert tree.count() == 3
    assert tree.height() == 2


def test_two_three_tree_insert_duplicate(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    with pytest.raises(ValueError):
        tree.insert(tree_sample_event)

    assert tree.count() == 1


def test_two_three_tree_retrieve_existing_event(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    result = tree.retrieve(
        "Tree Test Event",
        tree_sample_event._date
    )

    assert result is tree_sample_event


def test_two_three_tree_retrieve_missing_event(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    result = tree.retrieve(
        "Does Not Exist",
        tree_sample_event._date
    )

    assert result is None


def test_two_three_tree_retrieve_normalized_title(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    result = tree.retrieve(
        "  TREE TEST EVENT  ",
        tree_sample_event._date
    )

    assert result is tree_sample_event


def test_two_three_tree_height_empty():
    tree = TwoThreeTree()

    assert tree.height() == 0


def test_two_three_tree_height_one_event(tree_sample_event):
    tree = TwoThreeTree()

    tree.insert(tree_sample_event)

    assert tree.height() == 1
#TwoThreeTree.py
#Sanad Samara
#CS302-001
#program 5 and 4
#08/21/2026

# Stores the event in the node and keeps track of its child nodes
class TwoThreeTreeNode:
    def __init__(self, event):
        self.events = [event]
        self.children = []

# Class: TwoThreeTree
#
# Purpose:
#      Stores TrendEvent objects in a 2-3 tree and keeps the events ordered
#      by date and title. The class provides functions to insert retrieve
#      count and display events and to calculate the height of the tree
#
# Relationships:
#      TwoThreeTree stores TrendEvent objects using TwoThreeTreeNode objects
#      as the nodes of the tree. It is used by TrendTrackApp to store and
#      manage the events created by the user
#
# Data Hiding:
#      The root of the tree is hidden using a private instance data member
#      The tree uses member functions to insert retrieve count display and
#      calculate the height of the stored events
class TwoThreeTree:

    # Initializes the tree with an empty root node
    def __init__(self):
        self._root = None

    # Creates the key used to order events
    # Events are ordered first by date, then by title
    def _get_key(self, event):
        return (
            event._date,
            event._title.strip().lower()
        )

    # Recursively counts the number of events in the tree
    #return the count
    def count(self):
        return self._count(self._root)

    def _count(self, node):
        if node is None:
            return 0

        total = len(node.events)

        for child in node.children:
            total += self._count(child)

        return total

    # Inserts an event into the tree
    #return true on success
    def insert(self, event):
        if self._root is None:
            self._root = TwoThreeTreeNode(event)
            return True

        result = self._insert(self._root, event)

        if result is not None:
            promoted_event, left_child, right_child = result

            new_root = TwoThreeTreeNode(promoted_event)
            new_root.children = [
                left_child,
                right_child
            ]

            self._root = new_root

        return True

    # Recursive insertion
    def _insert(self, node, event):
        new_key = self._get_key(event)

        # Check for duplicate
        for existing_event in node.events:
            if new_key == self._get_key(existing_event):
                raise ValueError(
                    "An event with the same date and title already exists"
                )

        # Leaf node
        if len(node.children) == 0:
            node.events.append(event)

            node.events.sort(
                key=self._get_key
            )

            # Node has become a 3-node
            if len(node.events) == 3:
                return self._split(node)

            return None

        # Determine which child to recursively insert into
        if new_key < self._get_key(node.events[0]):
            child_index = 0

        elif (
            len(node.events) == 1
            or new_key < self._get_key(node.events[1])
        ):
            child_index = 1

        else:
            child_index = 2

        result = self._insert(
            node.children[child_index],
            event
        )

        # Child did not split
        if result is None:
            return None

        # Child split and promoted an event
        promoted_event, left_child, right_child = result

        node.events.append(promoted_event)

        node.events.sort(
            key=self._get_key
        )

        # Replace the split child with its two children
        old_child = node.children[child_index]

        node.children.pop(child_index)

        node.children.insert(
            child_index,
            right_child
        )

        node.children.insert(
            child_index,
            left_child
        )

        # Current node is now too large
        if len(node.events) == 3:
            return self._split(node)

        return None

    # Splits a 3-node into two nodes and promotes the middle event
    def _split(self, node):
        node.events.sort(
            key=self._get_key
        )

        middle_event = node.events[1]

        left = TwoThreeTreeNode(
            node.events[0]
        )

        right = TwoThreeTreeNode(
            node.events[2]
        )

        # If the node had children, distribute them
        if len(node.children) == 4:
            left.children = [
                node.children[0],
                node.children[1]
            ]

            right.children = [
                node.children[2],
                node.children[3]
            ]

        return (
            middle_event,
            left,
            right
        )

    # Displays all events in chronological order
    def display_in_order(self):
        self._display_in_order(self._root)

    # Recursive in-order traversal
    def _display_in_order(self, node):
        if node is None:
            return

        # Leaf
        if len(node.children) == 0:
            for event in node.events:
                print(event)
            return

        # 2-node
        if len(node.events) == 1:
            self._display_in_order(
                node.children[0]
            )

            print(node.events[0])

            self._display_in_order(
                node.children[1]
            )

        # 3-node
        else:
            self._display_in_order(
                node.children[0]
            )

            print(node.events[0])

            self._display_in_order(
                node.children[1]
            )

            print(node.events[1])

            self._display_in_order(
                node.children[2]
            )

    def retrieve(self, title, date):
        return self._retrieve(self._root, title, date)


    def _retrieve(self, node, title, date):
        if node is None:
            return None

        key = (date, title.strip().lower())

        # Check the events stored in this node
        for event in node.events:
            event_key = self._get_key(event)

            if key == event_key:
                return event

        # Leaf node and event wasn't found
        if len(node.children) == 0:
            return None

        # Decide which child to search
        if key < self._get_key(node.events[0]):
            return self._retrieve(
                node.children[0],
                title,
                date
            )

        if len(node.events) == 1:
            return self._retrieve(
                node.children[1],
                title,
                date
            )

        if key < self._get_key(node.events[1]):
            return self._retrieve(
                node.children[1],
                title,
                date
            )

        return self._retrieve(
            node.children[2],
            title,
            date
        )

    # Returns the height of the tree
    def height(self):
        return self._height(self._root)


    # Recursively calculates the height of the tree
    def _height(self, node):
        if node is None:
            return 0

        # A leaf node has a height of 1
        if len(node.children) == 0:
            return 1

        # All children of a 2-3 tree have the same height,
        # so we only need to check one child
        return 1 + self._height(node.children[0])
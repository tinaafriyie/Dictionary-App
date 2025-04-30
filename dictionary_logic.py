import json

# Node class representing each node in the BST
class Node:
    def __init__(self, word, meaning):
        self.word = word.title()
        self.meaning = meaning
        self.left = None
        self.right = None

# BSTDictionary class implementing a binary search tree dictionary
class BSTDictionary:
    def __init__(self):
        self.root = None
        self.favorites = set()   # Store favorite words
        self.history = []        # Recently searched words

    # Insert a word and its meaning into the BST
    def insert(self, word, meaning):
        self.root = self._insert_recursive(self.root, word, meaning)

    # Helper method for recursive insertion
    def _insert_recursive(self, node, word, meaning):
        if node is None:
            return Node(word, meaning)
        if word.title() < node.word:
            node.left = self._insert_recursive(node.left, word, meaning)
        elif word.title() > node.word:
            node.right = self._insert_recursive(node.right, word, meaning)
        else:
            node.meaning = meaning
        return node

    # Search for a word in the BST
    def search(self, word):
        result = self._search_recursive(self.root, word.title())
        if result and isinstance(result, Node):
            if result.word not in self.history:
                self.history.append(result.word)
            return f"{result.word}: {result.meaning}"
        else:
            return None

    # Helper method for recursive search
    def _search_recursive(self, node, word):
        if node is None:
            return None
        if word == node.word:
            return node
        elif word < node.word:
            return self._search_recursive(node.left, word)
        else:
            return self._search_recursive(node.right, word)

    # Delete a word from the BST
    def delete(self, word):
        self.root, deleted = self._delete_recursive(self.root, word.title())
        if deleted:
            return f"'{word.title()}' deleted successfully."
        else:
            return f"'{word.title()}' not found in dictionary."

    # Helper method for recursive deletion
    def _delete_recursive(self, node, word):
        if node is None:
            return node, False
        if word < node.word:
            node.left, deleted = self._delete_recursive(node.left, word)
            return node, deleted
        elif word > node.word:
            node.right, deleted = self._delete_recursive(node.right, word)
            return node, deleted
        else:
            # Found node to delete
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            successor = self._min_value_node(node.right)
            node.word, node.meaning = successor.word, successor.meaning
            node.right, _ = self._delete_recursive(node.right, successor.word)
            return node, True

    # Find the node with the minimum value in the BST
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Perform an inorder traversal of the BST
    def inorder_traversal(self):
        words = []
        self._inorder_recursive(self.root, words)
        return words

    # Helper method for recursive inorder traversal
    def _inorder_recursive(self, node, words):
        if node:
            self._inorder_recursive(node.left, words)
            words.append((node.word, node.meaning))
            self._inorder_recursive(node.right, words)

    # Save the BST to a file in JSON format
    def save_to_file(self, filename="dictionary.json"):
        words = {}
        self._build_dict(self.root, words)
        with open(filename, "w") as file:
            json.dump(words, file, indent=4)

    # Helper method to build a dictionary from the BST
    def _build_dict(self, node, words):
        if node:
            words[node.word] = node.meaning
            self._build_dict(node.left, words)
            self._build_dict(node.right, words)

    # Load the BST from a file in JSON format
    def load_from_file(self, filename="dictionary.json"):
        try:
            with open(filename, "r") as file:
                words = json.load(file)
                self.root = None
                for word, meaning in words.items():
                    self.insert(word, meaning)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    # Add a word to the favorites list
    def add_favorite(self, word):
        node = self._search_recursive(self.root, word.title())
        if node:
            self.favorites.add(node.word)
            return f"'{node.word}' added to favorites."
        else:
            return f"'{word.title()}' not found."

    # Remove a word from the favorites list
    def remove_favorite(self, word):
        if word.title() in self.favorites:
            self.favorites.remove(word.title())
            return f"'{word.title()}' removed from favorites."
        else:
            return f"'{word.title()}' is not in favorites."

    # Clear the search history
    def clear_history(self):
        self.history = []


    #Test the dictionary logic
if __name__ == '__main__':
    dictionary = BSTDictionary()
    dictionary.load_from_file()
    print("Dictionary loaded successfully.")
    while True:
        print("\n1. Search for a word")
        print("2. Add a new word")
        print("3. Delete a word")
        print("4. Display favorites")
        print("5. Add to favorites")
        print("6. Remove from favorites")
        print("7. Clear search history")
        print("8. Save and exit dictionary \n")
        choice = input("Enter your choice: ")

        if choice == "1":
            word = input("Enter the word to search: ")
            result = dictionary.search(word)
            if result:
                print(result)
            else:
                print("Word not found.")
        elif choice == "2":
            word = input("Enter the word to add: ")
            meaning = input("Enter the meaning: ")
            dictionary.insert(word, meaning)
            print(f"'{word}' added successfully.")
        elif choice == "3":
            word = input("Enter the word to delete: ")
            result = dictionary.delete(word)
            print(result)
        elif choice == "4":
            favorites = dictionary.favorites
            if favorites:
                print("Favorites:")
                for word in favorites:
                    print(word)
            else:
                print("No favorites added.")
        elif choice == "5":
            word = input("Enter the word to add to favorites: ")
            result = dictionary.add_favorite(word)
            print(result)
        elif choice == "6":
            word = input("Enter the word to remove from favorites: ")
            result = dictionary.remove_favorite(word)
            print(result)
        elif choice == "7":
            dictionary.clear_history()
            print("Search history cleared.")
        elif choice == "8":
            dictionary.save_to_file()
            print("Dictionary saved successfully.")
            break
        else:
            print("Invalid choice. Please try again.")
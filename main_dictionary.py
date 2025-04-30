import flet as ft
import random
import time
import threading
import colours_theme as ct
from dictionary_logic import BSTDictionary

# Initialize timers and theme
delete_timer = None
overwrite_timer = None
current_theme = "default"


# Helper function to show snackbars
def show_snackbar(page, message, icon=None, bgcolor=None, action=None, on_action=None):
    """
    Displays a snackbar with a message, icon, and optional action.
    """
    snackbar = ft.SnackBar(
        content=ft.Row(
            [
                ft.Icon(icon, color="white") if icon else None,
                ft.Text(message, color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=bgcolor or ct.AppColors.PRIMARY.value,
        duration=1500,
        action=action,
        on_action=on_action,
        show_close_icon=True,
    )
    page.open(snackbar)

# Helper function to start countdowns
def start_countdown(page, duration, callback, interval=1.0):
    """
    Starts a countdown timer that calls a callback function every `interval` seconds.
    """
    def countdown():
        for i in range(duration, 0, -1):
            callback(i)
            time.sleep(interval)
        callback(0)  # Final callback

    threading.Thread(target=countdown, daemon=True).start()
    page.update()

def main(page: ft.Page):
    # Initialize BST Dictionary
    dictionary = BSTDictionary()
    dictionary.load_from_file("dictionary.json")

    # At the beginning of the main function, after initializing the dictionary
    current_theme = "default"
    current_colors = ct.AppColors.get_colors(current_theme)

    # Page Setup
    page.title = "GROUP 3 | Lexis"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.spacing = 0
    page.window.width = 400
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False

    # Create theme
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ct.AppColors.PRIMARY.value,
            secondary=ct.AppColors.SECONDARY.value,
            surface=ct.AppColors.SURFACE.value,
            error=ct.AppColors.ERROR.value,
        )
    )

    def change_theme(theme_name):
        nonlocal current_theme
        current_theme = theme_name
        theme_colors = ct.AppColors.get_colors(theme_name)
        
        # Update theme
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=theme_colors["primary"],
                secondary=theme_colors["secondary"],
                surface=theme_colors["surface"],
                error=theme_colors["error"],
            )
        )
        
        # Update the app bar
        app_bar.bgcolor = theme_colors["primary"]
        
        # Update the word of day container gradient
        word_of_day_container.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[theme_colors["primary"], theme_colors["gradient_end"]],
        )
        
        # Update other UI elements with theme colors
        result_container.bgcolor = theme_colors["secondary"]
        result_word.color = theme_colors["primary"]
        result_meaning.color = theme_colors["text"]
        
        edit_container.bgcolor = theme_colors["secondary"]
        edit_result_title.color = theme_colors["primary"]
        edit_result_message.color = theme_colors["text"]
           
        page.update()
        
    def change_theme_mode(theme_mode: str):
        """Change the theme mode (light/dark/system)"""
        if theme_mode == "system":
            page.theme_mode = ft.ThemeMode.SYSTEM
        elif theme_mode == "light":
            page.theme_mode = ft.ThemeMode.LIGHT
        elif theme_mode == "dark":
            page.theme_mode = ft.ThemeMode.DARK
        
        page.update()

    # +---------------+
    # | UI Components |
    # +---------------+

    # Text Field for word input
    word_input = ft.TextField(
        label="Word",
        hint_text="Enter word...",
        expand=True,
        border_radius=8,
        text_size=16,
        on_submit=lambda _: search_word(),
    )

    # Text Field for meaning input
    meaning_input = ft.TextField(
        label="Meaning",
        hint_text="Enter meaning...",
        expand=True,
        border_radius=8,
        multiline=True,
        min_lines=3,
        max_lines=6,
        text_size=16,
    )

    # Result container
    result_container = ft.Container(
        padding=ft.padding.all(16),
        border_radius=ft.border_radius.all(12),
        bgcolor=ct.AppColors.SECONDARY.value,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        visible=False,
    )

    result_word = ft.Text(
        "",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ct.AppColors.PRIMARY.value,
    )

    result_meaning = ft.Text(
        "",
        size=16,
        color=ct.AppColors.TEXT.value,
        selectable=True,
    )

    result_container.content = ft.Column([
        result_word,
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        result_meaning,
    ], spacing=0)

    # Edit container for add_view tab
    edit_container = ft.Container(
        padding=ft.padding.all(16),
        border_radius=ft.border_radius.all(12),
        bgcolor=ct.AppColors.SECONDARY.value,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        visible=False,
    )

    edit_result_title = ft.Text(
        "",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ct.AppColors.PRIMARY.value,
    )

    edit_result_message = ft.Text(
        "",
        size=16,
        color=ct.AppColors.TEXT.value,
        selectable=True,
    )

    edit_container.content = ft.Column([
        edit_result_title,
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        edit_result_message,
    ], spacing=0)

    # History and Favorites Lists
    history_list = ft.ListView(expand=True, spacing=10, padding=10)
    favorites_list = ft.ListView(expand=True, spacing=10, padding=10)

    # Word of the Day
    def get_word_of_the_day():
        """Returns a random word and its meaning from the dictionary."""
        all_words = dictionary.inorder_traversal()
        if all_words:
            return random.choice(all_words)
        return ("No words yet", "Add some words to your dictionary!")

    word_of_day_container = ft.Container(
        padding=ft.padding.all(20),
        margin=ft.margin.only(bottom=20),
        border_radius=ft.border_radius.all(16),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ct.AppColors.PRIMARY.value, "#9A82DB"],
        ),
    )

    word_of_day = get_word_of_the_day()
    word_of_day_container.content = ft.Column([
        ft.Text("Word of the Day", size=14, color=ct.AppColors.SECONDARY.value),
        ft.Text(word_of_day[0], size=24, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text(word_of_day[1], size=16, color="white", opacity=0.9),
    ])

    # Shake animation for errors
    def shake_widget(widget):
        """Shakes a widget to draw attention."""
        original_margin = widget.margin or ft.margin.all(0)
        shake_offsets = [
            ft.margin.only(left=10),
            ft.margin.only(left=-10),
            ft.margin.only(left=6),
            ft.margin.only(left=-6),
            original_margin,
        ]
        for offset in shake_offsets:
            widget.margin = offset
            page.update()
            time.sleep(0.05)

    # Function: Search Word
    def search_word(e=None):
        """Searches for a word in the dictionary and displays the result."""
        word = word_input.value.strip()
        if not word:
            result_word.value = "Error"
            result_meaning.value = "Please enter a word to search"
            result_container.visible = True
            result_container.bgcolor = ft.Colors.ERROR_CONTAINER
            result_container.opacity = 0
            page.update()
            result_container.opacity = 1
            shake_widget(result_container)
            return

        result = dictionary.search(word)
        if result:
            parts = result.split(": ", 1)
            if len(parts) == 2:
                result_word.value = parts[0]
                result_meaning.value = parts[1]
                result_container.visible = True
                result_container.bgcolor = ct.AppColors.SECONDARY.value
                result_container.opacity = 0
                page.update()
                result_container.opacity = 1
        else:
            result_word.value = word
            result_meaning.value = "Not found in dictionary"
            result_container.visible = True
            result_container.bgcolor = ft.Colors.ERROR_CONTAINER
            result_container.opacity = 0
            page.update()
            result_container.opacity = 1
            shake_widget(result_container)
        update_history()
        page.update()

    # Function: Insert Word
    def insert_word(e=None):
        """Inserts or updates a word in the dictionary."""
        global overwrite_timer
        word = word_input.value.strip()
        meaning = meaning_input.value.strip()

        if word and meaning:
            search_result = dictionary.search(word)
            if not search_result:
                # New word: Insert immediately
                dictionary.insert(word, meaning)
                dictionary.save_to_file()
                word_input.value = ""
                meaning_input.value = ""
                edit_result_title.value = "Success!"
                edit_result_message.value = f"'{word}' added successfully."
                edit_container.bgcolor = ct.AppColors.SUCCESS.value
            elif edit_result_title.value == "Confirm Overwrite":
                # Overwrite confirmed
                dictionary.insert(word, meaning)
                dictionary.save_to_file()
                word_input.value = ""
                meaning_input.value = ""
                edit_result_title.value = "Success!"
                edit_result_message.value = f"'{word}' edited successfully."
                edit_container.bgcolor = ct.AppColors.SUCCESS.value

                # Cancel the overwrite timer
                if overwrite_timer:
                    overwrite_timer.cancel()
                    overwrite_timer = None
            else:
                # Word exists: Ask for confirmation
                edit_result_title.value = "Confirm Overwrite"
                edit_result_message.value = f"'{word}' already exists.\nPress SAVE WORD again within 5 seconds to modify."
                edit_container.bgcolor = ft.Colors.AMBER_200

                # Start countdown timer
                if overwrite_timer:
                    overwrite_timer.cancel()
                overwrite_timer = threading.Timer(5.0, reset_overwrite_confirmation)
                overwrite_timer.start()

            # Update UI
            edit_container.visible = True
            edit_container.opacity = 0
            page.update()
            edit_container.opacity = 1
        else:
            # Error case: Missing word or meaning
            edit_result_title.value = "Error"
            edit_result_message.value = "Both word and meaning are required."
            edit_container.bgcolor = ft.Colors.ERROR_CONTAINER
            edit_container.visible = True
            edit_container.opacity = 0
            page.update()
            edit_container.opacity = 1
            shake_widget(edit_container)

        page.update()

    # Function: Reset Overwrite Confirmation
    def reset_overwrite_confirmation():
        """Resets the overwrite confirmation UI after countdown expires."""
        global overwrite_timer
        edit_result_title.value = ""
        edit_result_message.value = ""
        edit_container.visible = False
        overwrite_timer = None
        page.update()

    # Function: Delete Word
    def delete_word(e=None):
        """Deletes a word from the dictionary."""
        global delete_timer
        word = word_input.value.strip()
        if word:
            if edit_result_title.value == "Confirm Delete":
                message = dictionary.delete(word)
                dictionary.save_to_file()
                edit_result_title.value = "Deleted" if "deleted successfully" in message else "Error"
                edit_result_message.value = message
                edit_container.bgcolor = ct.AppColors.SUCCESS.value if "deleted successfully" in message else ft.Colors.ERROR_CONTAINER
                word_input.value = ""
                if delete_timer:
                    delete_timer.cancel()
                    delete_timer = None
            else:
                edit_result_title.value = "Confirm Delete"
                edit_result_message.value = f"Press DELETE again within 5 seconds to confirm deletion of '{word}'."
                edit_container.bgcolor = ft.Colors.AMBER_200

                # Start countdown timer
                if delete_timer:
                    delete_timer.cancel()
                delete_timer = threading.Timer(5.0, reset_delete_confirmation)
                delete_timer.start()

            edit_container.visible = True
            edit_container.opacity = 0
            page.update()
            edit_container.opacity = 1
        else:
            edit_result_title.value = "Error"
            edit_result_message.value = "Please enter a word to delete."
            edit_container.visible = True
            edit_container.bgcolor = ft.Colors.ERROR_CONTAINER
            edit_container.opacity = 0
            page.update()
            edit_container.opacity = 1
            shake_widget(edit_container)

        page.update()

    # Function: Reset Delete Confirmation
    def reset_delete_confirmation():
        """Resets the delete confirmation UI after countdown expires."""
        global delete_timer
        edit_result_title.value = ""
        edit_result_message.value = ""
        edit_container.visible = False
        delete_timer = None
        page.update()

    # Function: Add to Favorites
    def add_favorite(word=None):
        """Adds a word to the favorites list."""
        if not word:
            word = word_input.value.strip()

        message = dictionary.add_favorite(word)
        if "added to favorites" in message:
            show_snackbar(
                page,
                f"Added '{word}' to favorites",
                icon=ft.Icons.FAVORITE,
                bgcolor=ft.Colors.PINK_ACCENT,
                action="Undo",
                on_action=lambda e: remove_favorite(word),
            )

        update_favorites()
        page.update()

    # Function: Remove from Favorites
    def remove_favorite(word):
        """Removes a word from the favorites list."""
        dictionary.remove_favorite(word)
        update_favorites()
        show_snackbar(
            page,
            f"Removed '{word}' from favorites",
            icon=ft.Icons.DELETE,
            bgcolor=ft.Colors.RED_ACCENT,
            action="Undo",
            on_action=lambda e: add_favorite(word),
        )
        page.update()

    # Function: Update History
    def update_history():
        """Updates the recent searches list."""
        history_list.controls.clear()
        if not dictionary.history:
            history_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.HISTORY, size=48, color=ct.AppColors.TEXT_SECONDARY.value, opacity=0.5),
                        ft.Text("No search history yet", color=ct.AppColors.TEXT_SECONDARY.value, opacity=0.7),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        else:
            for word in dictionary.history[-10:][::-1]:  # Show last 10 searches
                history_list.controls.append(create_history_item(word))
        page.update()

    # Function: Update Favorites
    def update_favorites():
        """Updates the favorites list."""
        favorites_list.controls.clear()
        if not dictionary.favorites:
            favorites_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.STAR, size=48, color=ct.AppColors.TEXT_SECONDARY.value, opacity=0.5),
                        ft.Text("No favorites yet", color=ct.AppColors.TEXT_SECONDARY.value, opacity=0.7),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        else:
            for word in sorted(list(dictionary.favorites)):
                favorites_list.controls.append(create_favorite_item(word))
        page.update()

    # Function: Create History Item
    def create_history_item(word):
        """Creates a history item card for the given word."""
        return ft.Card(
            elevation=2,
            content=ft.Container(
                content=ft.Row([
                    ft.Text(word, size=16, weight=ft.FontWeight.W_500),
                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        tooltip="Search",
                        icon_color=ct.AppColors.PRIMARY.value,
                        on_click=lambda _: search_and_go_home(word),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.STAR_BORDER,
                        tooltip="Add to favorites",
                        icon_color=ct.AppColors.PRIMARY.value,
                        on_click=lambda _: add_favorite(word),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(12),
            ),
        )

    # Function: Create Favorite Item
    def create_favorite_item(word):
        """Creates a favorite item card for the given word."""
        return ft.Card(
            elevation=2,
            content=ft.Container(
                content=ft.Row([
                    ft.Text(word, size=16, weight=ft.FontWeight.W_500),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.SEARCH,
                            tooltip="Search",
                            icon_color=ct.AppColors.PRIMARY.value,
                            on_click=lambda _: search_and_go_home(word),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Remove from favorites",
                            icon_color=ct.AppColors.ERROR.value,
                            on_click=lambda _: remove_favorite(word),
                        ),
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(12),
            ),
        )

    # Function: Search and Go Home
    def search_and_go_home(word):
        """Searches for a word and switches to the home tab."""
        word_input.value = word
        navigation.selected_index = 0
        content_area.content = home_view
        search_word()
        page.update()

    # Function: Clear History
    def clear_history(e=None):
        """Clears the search history."""
        dictionary.clear_history()
        update_history()
        show_snackbar(
            page,
            "Search history cleared",
            icon=ft.Icons.HISTORY,
            bgcolor=ft.Colors.BLUE,
            action="Undo",
            on_action=lambda e: page.open(
                ft.SnackBar(
                    content=ft.Text("History restore is not available yet!", color="white"),
                    bgcolor="red",
                    duration=1500,
                )
            ),
        )
        page.update()

    # Function: Display All Words
    def display_all_words(page, dictionary, navigation, content_area):
        """Displays all words in the dictionary in a scrollable list."""
        theme_colors = ct.AppColors.get_colors(current_theme)
        all_words = dictionary.inorder_traversal()
        if not all_words:
            show_snackbar(page, "Dictionary is empty.", bgcolor=theme_colors["error"])
            return

        # Create a back button to restore the main app layout
        def go_back(e):
            page.clean()
            page.add(app_bar, content_area, navigation)
            page.update()

        # Function to handle search and go back
        def search_and_go_back(word):
            go_back(None)
            search_and_go_home(word)

        # Create a sticky top bar with back button and title
        top_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=go_back,
                        icon_color=theme_colors["primary"],
                    ),
                    ft.Text("ALL WORDS", weight=ft.FontWeight.BOLD, size=20, color=theme_colors["primary"]),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            bgcolor=theme_colors["secondary"],
            border_radius=8,
        )

        # Create list items instead of DataTable for better scrolling
        word_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )
        
        for word, meaning in all_words:
            word_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    word, 
                                    weight=ft.FontWeight.BOLD,
                                    color=theme_colors["text"],
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.SEARCH,
                                    tooltip="Search this word",
                                    icon_color=theme_colors["primary"],
                                    on_click=lambda e, w=word: search_and_go_back(w),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10,
                    )
                )
            )

        # Main layout using Column with scroll
        main_content = ft.Column(
            [
                top_bar,
                ft.Container(height=10),
                ft.Container(content=word_list,expand=True,),
            ],
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

        # Clear the page and add the new content
        page.clean()
        page.add(main_content)
        page.update()

    # Function: Load Custom Dictionary
    def load_custom_dictionary():
        # Create a file picker for JSON files
        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                selected_file = e.files[0].path
                if selected_file.endswith('.json'):
                    try:
                        # Clear current dictionary and load new one
                        dictionary.load_from_file(selected_file)
                        # Update word of the day
                        word_of_day = get_word_of_the_day()
                        word_of_day_container.content.controls[1].value = word_of_day[0]
                        word_of_day_container.content.controls[2].value = word_of_day[1]
                        
                        # Show success message
                        page.open(
                            ft.SnackBar(
                                content=ft.Text(f"Loaded dictionary from {e.files[0].name}", color="white"),
                                bgcolor=ft.Colors.GREEN,
                                duration=1500,
                            )
                        )
                        
                        # Update lists
                        update_history()
                        update_favorites()
                        
                    except Exception as ex:
                        page.open(
                            ft.SnackBar(
                                content=ft.Text(f"Error loading file: {str(ex)}", color="white"),
                                bgcolor=ft.colors.RED,
                                duration=1500,
                            )
                        )
                else:
                    page.open(
                        ft.SnackBar(
                            content=ft.Text("Please select a JSON file", color="white"),
                            bgcolor=ft.Colors.RED,
                            duration=2000,
                        )
                    )
            page.update()

        # Create and open file picker
        file_picker = ft.FilePicker(on_result=pick_files_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(
            dialog_title="Select Dictionary JSON File",
            allowed_extensions=["json"],
            file_type=ft.FilePickerFileType.CUSTOM,
        )


    # App bar
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU_BOOK),
        leading_width=40,
        title=ft.Text("GROUP 3 | Lexicon", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ct.AppColors.PRIMARY.value,
        color=ct.AppColors.SURFACE.value,
    )

    # Home tab content
    home_view = ft.Column(
        [
            word_of_day_container,
            ft.Text("Search Dictionary", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                word_input,
                ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    icon_color=ct.AppColors.PRIMARY.value,
                    on_click=search_word,
                ),
            ]),
            result_container,
            ft.Container(height=20),
            ft.Row([
                ft.FilledButton(
                    "Random Word",
                    icon=ft.Icons.SHUFFLE,
                    on_click=lambda _: (
                        setattr(word_input, "value", get_word_of_the_day()[0]),
                        search_word()
                    ),
                ),
                ft.FilledTonalButton(
                    "Add to Favorites",
                    icon=ft.Icons.STAR,
                    on_click=lambda _: add_favorite(),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # Add Word tab content
    add_view = ft.Column(
        [
            ft.Text("Add New Word", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            word_input,
            ft.Container(height=10),
            meaning_input,
            ft.Container(height=20),
            edit_container,
            ft.Container(height=20),
            ft.Row([
                ft.FilledButton(
                    "Save Word",
                    icon=ft.Icons.SAVE,
                    on_click=insert_word,
                ),
                ft.OutlinedButton(
                    "Delete Word",
                    icon=ft.Icons.DELETE,
                    on_click=delete_word,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # History tab content
    history_view = ft.Column(
        [
            ft.Row([
                ft.Text("Recent Searches", size=18, weight=ft.FontWeight.BOLD),
                ft.OutlinedButton(
                    "Clear All",
                    icon=ft.Icons.DELETE_SWEEP,
                    on_click=clear_history,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.Container(
                content=history_list,
                expand=True,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # Favorites tab content
    favorites_view = ft.Column(
        [
            ft.Text("Your Favorites", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Container(
                content=favorites_list,
                expand=True,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # Settings tab content
    settings_view = ft.Column(
        [
            ft.Text("Settings", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Theme Mode", size=16, weight=ft.FontWeight.W_500),
                        ft.Container(height=10),
                        ft.Dropdown(
                            label="Select theme mode",
                            value="system",
                            options=[
                                ft.dropdown.Option(text="System", key="system"),
                                ft.dropdown.Option(text="Light", key="light"),
                                ft.dropdown.Option(text="Dark", key="dark"),
                            ],
                            on_change=lambda e: change_theme_mode(e.control.value),
                        ),
                    ]),
                    padding=16,
                ),
            ),
            ft.Container(height=20),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Colour Theme", size=16, weight=ft.FontWeight.W_500),
                        ft.Container(height=10),
                        ft.RadioGroup(
                            content=ft.Column([
                                ft.Radio(value="default", label="Default Theme (Purple)"),
                                ft.Radio(value="blue", label="Blue Theme"),
                                ft.Radio(value="cream", label="Cream Theme"),
                                ft.Radio(value="green", label="Green Theme"),
                                ft.Radio(value="brown", label="Brown Theme"),
                                ft.Radio(value="red", label="Red Theme"),
                                ft.Radio(value="ocean", label="Ocean Theme"),
                                ft.Radio(value="sunset", label="Sunset Theme"),
                                ft.Radio(value="Custum Colour", label="Custom Theme", disabled=True),
                            ]),
                            value="default",
                            on_change=lambda e: change_theme(e.control.value),
                        ),
                    ]),
                    padding=16,
                ),
            ),
            ft.Container(height=20),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Dictionary Options", size=16, weight=ft.FontWeight.W_500),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Show All Words",
                            icon=ft.Icons.LIST,
                            on_click=lambda _: display_all_words(page, dictionary, navigation, content_area),
                        ),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "Load Custom Dictionary",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=lambda _: load_custom_dictionary(),
                        ),
                    ]),
                    padding=16,
                ),
            ),
            ft.Text("More settings coming soon...", color=ct.AppColors.TEXT_SECONDARY.value),
        ],
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
    )

    # Container for all views
    content_area = ft.Container(
        padding=ft.padding.all(16),
        expand=True,
        content=home_view,
    )

    # Bottom Navigation Tabs
    def change_tab(e):
        """Changes the active tab and updates the content area."""
        selected_tab = e.control.selected_index
        content_area.opacity = 0
        page.update()
        time.sleep(0.1)

        if selected_tab == 0:  # Home
            word_of_day = get_word_of_the_day()
            word_of_day_container.content.controls[1].value = word_of_day[0]
            word_of_day_container.content.controls[2].value = word_of_day[1]
            content_area.content = home_view
        elif selected_tab == 1:  # Add
            content_area.content = add_view
        elif selected_tab == 2:  # History
            update_history()
            content_area.content = history_view
        elif selected_tab == 3:  # Favorites
            update_favorites()
            content_area.content = favorites_view
        elif selected_tab == 4:  # Settings
            content_area.content = settings_view

        content_area.opacity = 1
        page.update()

    # Create navigation bar
    navigation = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, selected_icon=ft.Icons.ADD_CIRCLE, label="Add"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY_OUTLINED, selected_icon=ft.Icons.HISTORY, label="History"),
            ft.NavigationBarDestination(icon=ft.Icons.STAR_OUTLINE, selected_icon=ft.Icons.STAR, label="Favorites"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
        ],
        selected_index=0,
        on_change=change_tab,
    )

    # Main layout
    page.add(
        app_bar,
        content_area,
        navigation,
    )
    page.update()

# Run App
if __name__ == "__main__":
    ft.app(target=main)
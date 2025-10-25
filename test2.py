from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import Label, TextArea, Button
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings

def main():
    # Create fields
    name_field = TextArea(height=1, prompt='', multiline=False)
    age_field = TextArea(height=1, prompt='', multiline=False)
    birthday_field = TextArea(height=1, prompt='', multiline=False)
    result_field = TextArea(height=1, style="class:output", read_only=True)

    # Submit handler
    def on_submit():
        name = name_field.text.strip()
        age = age_field.text.strip()
        birthday = birthday_field.text.strip()
        info = [name, age, birthday]
        result_field.text = f"Collected info: {info}"
        get_app().exit()

    # Key bindings: press Enter to move to next field
    kb = KeyBindings()

    @kb.add('enter')
    def _(event):
        event.app.layout.focus_next()

    # Layout
    layout = HSplit([
        VSplit([Label("name:     ", width=10), name_field]),
        VSplit([Label("age:      ", width=10), age_field]),
        VSplit([Label("birthday: ", width=10), birthday_field]),
        VSplit([Button(text="Submit", handler=on_submit)], align ="LEFT"),
        result_field,
    ])

    # App
    app = Application(layout=Layout(layout), key_bindings=kb, full_screen=True)
    app.run()

if __name__ == "__main__":
    main()

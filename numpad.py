from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class NumPadPopUp(TextInput):
    """
    This Numeric pad popup is a TextInput focused to show numeric keyboard in a popup
    To define the popup dimensions use pop_height and pop_width (set to 0.7 and 0.4 by default) or pop_size
    For example in kv file:
    NumPadPopUp:
        pop_size: 0.7, 0.4
    would result in a size_hint of 0.7, 0.4 being used to create the popup
    """
    pop_height = NumericProperty(0.7)
    pop_width = NumericProperty(0.4)
    pop_size = ReferenceListProperty(pop_height, pop_width)

    def __init__(self, touch_switch=False, **kwargs):
        super(NumPadPopUp, self).__init__(**kwargs)
        self.touch_switch = touch_switch
        self.init_ui()

    def init_ui(self):
        self.text = ""
        self.num = NumPadWidget(as_popup=True, touch_switch=self.touch_switch)

        # Popup
        self.popup = Popup(content=self.num, on_dismiss=self.update_value, title="")
        self.num.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, inst, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint = self.pop_size
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = self.num.active_text
        self.focus = False


class NumPadWidget(RelativeLayout):
    """ Basic NumPad (Numeric pad) widget """
    active_text = StringProperty()

    def __init__(self, as_popup=False, touch_switch=False, **kwargs):
        super(NumPadWidget, self).__init__(**kwargs)
        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.init_ui()

    def init_ui(self):
        self.create_num_scr()

    def create_num_scr(self):
        """ Screen with Numeric pad and screen"""

        scr = Screen()

        vert_layout = BoxLayout(orientation='vertical')  # BoxLayout with all the Buttons and TextInput

        bx = BoxLayout(orientation='horizontal')
        self.numpad_scr = TextInput(input_type="number", input_filter="float", font_size=25)
        bx.add_widget(self.numpad_scr)
        vert_layout.add_widget(bx)

        bx1 = BoxLayout(orientation='horizontal')
        for i in range(7, 10):
            btn = Button(text=str(i))
            btn.bind(on_press=self.get_btn_value)
            bx1.add_widget(btn)
        vert_layout.add_widget(bx1)

        bx2 = BoxLayout(orientation='horizontal')
        for i in range(4, 7):
            btn = Button(text=str(i))
            btn.bind(on_press=self.get_btn_value)
            bx2.add_widget(btn)
        vert_layout.add_widget(bx2)

        bx3 = BoxLayout(orientation='horizontal')
        for i in range(1, 4):
            btn = Button(text=str(i))
            btn.bind(on_press=self.get_btn_value)
            bx3.add_widget(btn)
        vert_layout.add_widget(bx3)

        bx4 = BoxLayout(orientation='horizontal')
        for i in ['<--', 0, '.']:
            btn = Button(text=str(i))
            btn.bind(on_press=self.get_btn_value)
            bx4.add_widget(btn)
        vert_layout.add_widget(bx4)

        bx5 = BoxLayout(orientation='horizontal')
        for i in ['AC', 'OK']:
            btn = Button(text=str(i))
            btn.bind(on_press=self.get_btn_value)
            bx5.add_widget(btn)
        vert_layout.add_widget(bx5)

        scr.add_widget(vert_layout)
        self.add_widget(scr)

    def get_btn_value(self, inst):
        """ Get the value from pressed button """
        previous_text = self.active_text
        self.active_text += inst.text
        # print(self.active_text)
        if "OK" in self.active_text:
            self.active_text = previous_text
            self.parent_popup.dismiss()
            self.active_text = ""
            previous_text = ""

        if "<--" in self.active_text:
            self.active_text = previous_text[:-1]
        if "AC" in self.active_text:
            self.active_text = ""
        self.numpad_scr.text = self.active_text


if __name__ == "__main__":
    from kivy.base import runTouchApp
    c = NumPadPopUp(size_hint=[0.25, 0.04], pos_hint={'center_x': 0.5, 'center_y': 0.5})
    runTouchApp(c)

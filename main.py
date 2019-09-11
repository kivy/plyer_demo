from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import StringProperty


KV = r'''
#:import Clock kivy.clock.Clock
#:import mainthread kivy.clock.mainthread
#:import Permission android.permissions.Permission
#:import accelerometer plyer.accelerometer
#:import audio plyer.audio
#:import barometer plyer.barometer
#:import battery plyer.battery
#:import brightness plyer.brightness
#:import gps plyer.gps

RootWidget:
    current: app.current_screen or self.current

    Menu:
    Accelerometer:
    Audio:
    Barometer:
    Battery:
    Brightness:
    Call:
    # Camera:
    Compass:
    Email:
    Flash:
    GPS:
    Gravity:
    Gyroscope:
    Humidity:
    IRBlaster:
    Light:
    # FileChooser:
    Notification:
    Orientation:
    Proximity:
    # ScreenShot:
    SMS:
    SpatialOrientation:
    SpeechToText:
    StoragePath:
    Temperature:
    UniqueID:
    Vibrator:

<RootWidget@ScreenManager>:
    canvas.before:
        Color:
            rgba: rgba('FFFFFF')
        Rectangle:
            pos: self.pos
            size: self.size

<MenuButton@Button>:
    on_press: app.switch_screen(self.text)
    font_size: sp(25)

<AppLabel@Label>:
    color: rgba('#000000FF')
    font_size: sp(25)

<Menu@Screen>:
    RecycleView:
        viewclass: 'MenuButton'
        data:
            [
            {
            'text': screen
            }
            for screen in root.manager.screen_names
            if screen not in ('Menu', '')
            ]

        RecycleBoxLayout:
            padding: 20
            spacing: 10
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            default_size_hint: 1, None
            default_size: 0, dp(38)

<Accelerometer@Screen>:
    name: 'Accelerometer'
    values: [0, 0, 0]
    update_values: lambda x: setattr(self, 'values', accelerometer.acceleration)

    on_enter:
        accelerometer.enable()
        self.event = Clock.schedule_interval(self.update_values, 0)

    on_leave:
        self.event.cancel()
        accelerometer.disable()

    AppLabel:
        text: 'Acceleration:\n' + '\n'.join(str(v) for v in root.values)
        text_size: self.width, None
        padding: 10, 0
        halign: 'left'

<Audio@Screen>:
    name: 'Audio'
    on_enter: app.ask_nicely(Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE)
    BoxLayout:
        orientation: 'vertical'
        padding: 20, 20
        Button:
            text: 'hold to record'
            on_press: audio.start()
            on_release: audio.stop()

        Button:
            text: 'tap to replay'
            on_press: audio.play()

<Barometer@Screen>:
    name: 'Barometer'
    value: 0
    update_value: lambda x: setattr(self, 'value', barometer.pressure or 0)

    on_enter:
        barometer.enable()
        self.event = Clock.schedule_interval(self.update_value, 0)

    on_leave:
        self.event.cancel()
        barometer.disable()

    AppLabel:
        text: 'pressure: {}'.format(root.value)

<Battery@Screen>:
    name: 'Battery'
    value: ''
    update_value: lambda x: setattr(self, 'value', str(battery.status) or '')

    on_enter:
        self.event = Clock.schedule_interval(self.update_value, 1)

    on_leave:
        self.event.cancel()

    AppLabel:
        text: root.value or ''

<Brightness@Screen>:
    name: 'Brightness'

    value: -1
    update_value: lambda x: setattr(self, 'value', brightness.current_level() or -1)

    on_pre_enter:
        app.ask_nicely(Permission.WRITE_SETTINGS)
        self.event = Clock.schedule_interval(self.update_value, 0)

    on_leave:
        self.event.cancel()

    BoxLayout:
        Slider:
            min: 0
            max: 100
            value: max(root.value, 0)
            disabled: root.value < 0
            on_value:
                if not self.disabled: brighness.set_level(self.value)

        AppLabel:
            text: str(root.value or '')

<Call@Screen>:
    name: 'Call'

<Camera@Screen>:
    name: 'Camera'

<Compass@Screen>:
    name: 'Compass'

<Email@Screen>:
    name: 'Email'

<Flash@Screen>:
    name: 'Flash'

<GPS@Screen>:
    name: 'GPS'
    location: {}
    update_location:
        mainthread(lambda **kwargs: self.location.update(kwargs))

    status: []
    update_status: mainthread(self.status.append)

    on_enter:
        app.ask_nicely(Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION)
        gps.configure(self.update_location, self.update_status)
        gps.start()

    on_leave:
        gps.stop()

    BoxLayout:
        orientation: 'vertical'
        AppLabel:
            text:
                '\n'.join(
                '{}: {}'.format(key, value)
                for key, value in (root.location).items()
                )
        AppLabel:
            text: '\n'.join(root.status)

<Gravity@Screen>:
    name: 'Gravity'

<Gyroscope@Screen>:
    name: 'Gyroscope'

<Humidity@Screen>:
    name: 'Humidity'

<IRBlaster@Screen>:
    name: 'IRBlaster'

<Light@Screen>:
    name: 'Light'

<FileChooser@Screen>:
    name: 'FileChooser'

<Notification@Screen>:
    name: 'Notification'

<Orientation@Screen>:
    name: 'Orientation'

<Proximity@Screen>:
    name: 'Proximity'

<SMS@Screen>:
    name: 'SMS'

<SpatialOrientation@Screen>:
    name: 'SpatialOrientation'

<SpeechToText@Screen>:
    name: 'SpeechToText'

<StoragePath@Screen>:
    name: 'StoragePath'

<Temperature@Screen>:
    name: 'Temperature'

<UniqueID@Screen>:
    name: 'UniqueID'

<Vibrator@Screen>:
    name: 'Vibrator'

'''

class Application(App):
    current_screen = StringProperty()

    def build(self):
        return Builder.load_string(KV)

    def switch_screen(self, screen_name):
        self.current_screen = screen_name


    def ask_nicely(self, *permissions):
        from android.permissions import (
            check_permission, request_permission, request_permissions
        )
        request_permissions(
            [
                permission
                for permission in permissions
                if not check_permission(permission)
            ]
        )


    def on_stop(self):
        if self.current_screen == 'Menu':
            return True
        self.current_screen = 'Menu'


if __name__ == "__main__":
    Application().run()

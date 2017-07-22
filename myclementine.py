import dbus

bus = dbus.SessionBus()
player = bus.get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')
property_interface = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')

STRING_UNAVAILABLE = ''
STRING_ERROR = ''


class Py3status:
    """
    """
    cache_timeout = 5
    format = u'♫ {current}'

    def myclementine(self):
        """
        Get metadata of currently playing song
        """
        if not self.py3.check_commands(['/home/atrament/oss-projects/Clementine/bin/clementine']):
            return {
                'cached_until': self.py3.CACHE_FOREVER,
                'color': self.py3.COLOR_BAD,
                'full_text': STRING_UNAVAILABLE
            }
        
        try:
            metadata = player.Get('org.mpris.MediaPlayer2.Player','Metadata', dbus_interface='org.freedesktop.DBus.Properties')
            artist = metadata['xesam:artist'][0] if 'xesam:artist' in metadata else ''
            title = metadata['xesam:title'] if 'xesam:title' in metadata else ''
            now_playing = artist + " - " + title 
        except:
            return {
                "cached_until" : self.py3.time_in(self.cache_timeout),
                "full_text" : STRING_ERROR
            }
            
        return {
            'cached_until' : self.py3.time_in(self.cache_timeout),
            'full_text' : self.py3.safe_format(self.format, {'current': now_playing})
        }

if __name__ == "__main__":
     from py3status.module_test import module_test
     module_test(Py3status)



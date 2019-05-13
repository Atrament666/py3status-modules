class Py3status:

    
    format = 'Dnes má svátek: {name}'
    cache_timeout = 3600
    url = ''


    def svatky(self):
        import json
        from datetime import datetime

        with open('/usr/share/svatky.json') as json_data:
            data = json.load(json_data)
            events = data["VCALENDAR"][0]["VEVENT"]
            today = datetime.now().strftime('%m%d')
            for event in events:
                event_date = datetime.strptime(event["DTSTART;Europe/Prague;VALUE=DATE"], '%Y%m%d')
                day = event_date.strftime('%m%d')
                if today == day:
                    name = event["DESCRIPTION"]
                    self.url = event["URL"]

        return {
           'full_text': self.py3.safe_format(self.format, {'name': name}),
           'cached_until': self.py3.time_in(self.cache_timeout),
           'url' : self.url
        }

    def on_click(self, event):
        import subprocess
        subprocess.run(["xdg-open",self.url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)        

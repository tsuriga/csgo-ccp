"""
The MIT License (MIT)

Copyright (c) 2016 Tsuri Kamppuri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from subprocess import call
from configparser import ConfigParser
from threading import Timer
from datetime import datetime, timedelta
import sys
import os.path
import time
import json


class PotatoException(Exception):
    pass


class PotatoConfig(ConfigParser):
    def __init__(self, config_file):
        super(PotatoConfig, self).__init__()

        self.read(config_file)
        self.validate_config()

    def validate_config(self):
        required_values = {
            'potato': {
                'game_modes': ('casual', 'competitive'),
                'death_rite': None,
                'respawn_beckon': None,
                'wakeup_phase_round': ('over', 'freezetime'),
                'wakeup_phase_map': ('gameover', 'warmup', 'freezetime'),
                'action_delay': None
            },
            'server': {'name': None, 'port': None}
        }

        for section, keys in required_values.items():
            if section not in self:
                raise PotatoException(
                    'Your config file is missing section %s, ' +
                    'where did you put it? Bring it back!' % section)

            for key, accepted_values in keys.items():
                if key not in self[section] or self[section][key] == '':
                    raise PotatoException(
                        'Your config file is missing value ' +
                        'for %s under section %s, why? Fix that!' %
                        (key, section))

                if accepted_values:
                    entered_values = []

                    if ',' in self[section][key]:
                        entered_values = self[section][key].split(',')
                    else:
                        entered_values = [self[section][key]]

                    for value in entered_values:
                        if value.strip() not in accepted_values:
                            raise PotatoException((
                                'Your config file has crazy value for %s ' +
                                'under section %s. Use a sane value!') %
                                (key, section))


class PotatoServer(HTTPServer):
    def set_monitored_game_modes(self, modes):
        self.monitored_game_modes = modes

    def set_wakeup_phase_after_round(self, phase):
        self.wakeup_phase_round_end = phase

    def set_wakeup_phase_after_map(self, phase):
        self.wakeup_phase_map_end = phase

    def set_death_potato(self, potato):
        self.death_potato = potato

    def set_respawn_potato(self, potato):
        self.respawn_potato = potato

    def set_action_delay(self, delay):
        self.action_delay = int(delay)

    def init_state(self):
        self.waiting_for = 'start'
        self.break_announced = True
        self.death_initiated_at = datetime.now()
        # self.previous_payload = ''


class PotatoRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode('utf-8')

            self.parse_payload(json.loads(body))

            self.send_header('Content-type', 'text/html')
            self.send_response(200)
            self.end_headers()
        except KeyboardInterrupt:
            raise

    def parse_payload(self, payload):
        def method_not_found(payload):
            raise PotatoException(
                'State machine broke, how did that even happen?')

        if payload and self.is_connected_to_server(payload):
            game_mode = self.get_game_mode(payload)

            if game_mode in self.server.monitored_game_modes:
                method_name = 'detect_' + self.server.waiting_for
                method = getattr(self, method_name, method_not_found)
                method(payload)

            # if payload != self.server.previous_payload:
                # self.server.previous_payload = payload
                # print(payload)

        else:
            self.reset_detection()

    def is_connected_to_server(self, payload):
        return 'map' in payload

    def get_game_mode(self, payload):
        if 'map' in payload and 'mode' in payload['map']:
            return payload['map']['mode']
        else:
            return None

    def get_player_activity(self, payload):
        if 'player' in payload and 'activity' in payload['player']:
            return payload['player']['activity']
        else:
            return None

    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None

    def get_round_number(self, payload):
        if 'map' in payload and 'round' in payload['map']:
            return int(payload['map']['round'])
        else:
            return None

    def get_map_phase(self, payload):
        if 'map' in payload and 'phase' in payload['map']:
            return payload['map']['phase']
        else:
            return None

    def get_player_health(self, payload):
        if ('player' in payload and
                'state' in payload['player'] and
                'health' in payload['player']['state']):
            return int(payload['player']['state']['health'])
        else:
            return None

    def get_player_steamid(self, payload):
        if 'player' in payload and 'steamid' in payload['player']:
            return payload['player']['steamid']
        else:
            return None

    def get_own_steamid(self, payload):
        if 'provider' in payload and 'steamid' in payload['provider']:
            return payload['provider']['steamid']
        else:
            return None

    def player_is_you(self, payload):
        player = self.get_player_steamid(payload)
        you = self.get_own_steamid(payload)

        return player and you and player == you

    def detect_start(self, payload):
        map_phase = self.get_map_phase(payload)
        round_phase = self.get_round_phase(payload)
        health = self.get_player_health(payload)

        # Assume that the user is the game already if they've chosen to tab
        # back for the map change
        if (map_phase == 'warmup' and
                self.server.wakeup_phase_map_end != 'gameover'):
            # Wake up for warmup or when warmup is ending
            self.start_detection('respawn')

        elif self.player_is_you(payload):
            # Connected to join a live round
            if health > 0:
                self.start_detection('death')

            # Connected to spectate a live round
            else:
                self.start_detection('respawn')

    def detect_death(self, payload):
        # Only inspect our own state, not other players
        if not self.player_is_you(payload):
            return

        # Skip events that are not related to playing
        if self.get_player_activity(payload) != 'playing':
            return

        round_phase = self.get_round_phase(payload)
        health = self.get_player_health(payload)

        if round_phase == 'live' and health == 0:
            self.drop_dead()

    def drop_dead(self):
        print('You died like a sack of potatoes')

        self.server.waiting_for = 'respawn'

        t = Timer(self.server.action_delay / 1000, self.call_death_potato)
        t.start()

        self.server.death_initiated_at = datetime.now()

    def call_death_potato(self):
        try:
            call(os.path.join('potatoes', self.server.death_potato))
        except OSError:
            raise PotatoException(
                'Could not run potato program %s' %
                self.server.death_potato)

    def detect_respawn(self, payload):
        round_phase = self.get_round_phase(payload)
        map_phase = self.get_map_phase(payload)
        round_number = self.get_round_number(payload)

        # Round ends
        if round_phase == self.server.wakeup_phase_round_end:
            self.respawn()
        # Map has ended (either before or after the map changes)
        elif map_phase == self.server.wakeup_phase_map_end:
            self.respawn()
        # The warmup is ending
        elif (round_number == 0 and
                round_phase == self.server.wakeup_phase_map_end):
            self.respawn()

    def start_detection(self, phase):
        self.server.waiting_for = phase

        print('Farming for potatoes, waiting for %s' % phase)

        self.server.break_announced = False

    def reset_detection(self):
        self.server.waiting_for = 'start'

        if not self.server.break_announced:
            print('Taking a break from potato farming')

            self.server.break_announced = True

    def respawn(self):
        self.server.waiting_for = 'death'

        d = datetime.now() - self.server.death_initiated_at
        ms = int(d.total_seconds() * 1000)

        delay = 0
        if ms < self.server.action_delay:
            delay = ms

        t = Timer(delay, self.call_respawn_potato)
        t.start()

    def call_respawn_potato(self):
        try:
            call(os.path.join('potatoes', self.server.respawn_potato))
        except OSError:
            raise PotatoException(
                'Could not run potato program %s' %
                self.server.respawn_potato)

        print('The dream is alive')

    def log_message(self, format, *args):
        return


cfg = {}

try:
    cfg = PotatoConfig('../config.ini')
except PotatoException as e:
    print(e)
    sys.exit(1)

server = PotatoServer(
    (cfg['server']['name'], int(cfg['server']['port'])), PotatoRequestHandler)

server.init_state()
server.set_monitored_game_modes(cfg['potato']['game_modes'])
server.set_death_potato(cfg['potato']['death_rite'])
server.set_respawn_potato(cfg['potato']['respawn_beckon'])
server.set_wakeup_phase_after_round(cfg['potato']['wakeup_phase_round'])
server.set_wakeup_phase_after_map(cfg['potato']['wakeup_phase_map'])
server.set_action_delay(cfg['potato'].getint('action_delay'))

print(time.asctime(), '-', 'CS:GO Casual Couch Potato server starting')

try:
    server.serve_forever()
except PotatoException as e:
    print(e)
except KeyboardInterrupt:
    pass

server.server_close()
print(time.asctime(), '-', 'CS:GO Casual Couch Potato server stopped')

from lettuce import step, world

from brewgearpi import fakeio, logger

DEFAULT_TEMP = 20.0

@step(u'Given a running system')
def a_running_system(step):
    fakeio.time = 0
    fakeio.temperature = DEFAULT_TEMP
    fakeio.heater = Off
    world.log_lines = []
    world.logger = logger.Logger(fakeio, world.log_lines.append)

@step(u'When a line is logged')
def a_line_is_logged(step):
    world.log_line = world.logger()

@step(u'Then it contains information about time, temperature and heater')
def it_contains_information_about_temperature_temperature_heater_and_time(step):
    assert str(world.log_line.time) == '1970-01-01 00:00:00', 'Time is %s' % world.log_line.time
    assert world.log_line.temperature == DEFAULT_TEMP, 'Temperature is %s' % world.log_line.temperature
    assert world.log_line.heater == Off, 'Heater is %s' % world.log_line.heater

@step(u'And a second line with the same state')
def a_second_line_with_the_same_state(step):
    world.logger()

@step(u'And a second line with a temparature T plus (-?\d+\.\d+) degrees')
def a_second_line_with_a_temparature_t_plus_d_degrees(step, delta_t):
    fakeio.temperature = DEFAULT_TEMP + float(delta_t)
    world.logger()

@step(u'And a minute expires')
def when_a_minute_expires(step):
    fakeio.time = fakeio.time + 60
    world.logger()

@step(u'Then (no|one) new line is logged')
def no_one_new_line_is_logged(step, s):
    if s == 'one':
        assert len(world.log_lines) == 2, world.logger.lines
    else:
        assert len(world.log_lines) == 1, world.logger.lines

# vim: sw=4:et:ai
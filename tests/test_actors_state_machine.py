
from brewberry.actors import spawn, with_self_address, monitor, actor_info
import gevent.queue


@with_self_address
def ping(self, queue, i):
    queue.put('ping %d' % i)
    if i == 0: return
    self(queue, i - 1)
    return pong


@with_self_address
def pong(self, queue, i):
    queue.put('pong %d' % i)
    if i == 0: return
    self(queue, i - 1)
    return ping


def test_state_machine():

    def my_monitor(q):
        def catcher(f, e):
            q.put((f, e))
        return catcher

    response = gevent.queue.Queue()
    monitor_response = gevent.queue.Queue()

    state_machine = spawn(ping, response, 5)
    mon = spawn(my_monitor, monitor_response)
    monitor(state_machine, mon)

    assert response.get() == 'ping 5'
    assert response.get() == 'pong 4'
    assert response.get() == 'ping 3'
    assert response.get() == 'pong 2'
    assert response.get() == 'ping 1'

    assert monitor_response.get() == (ping, None)

    assert not actor_info(state_machine).running
    assert not actor_info(mon).running
# vim:sw=4:et:ai
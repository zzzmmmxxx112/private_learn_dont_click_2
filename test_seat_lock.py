from seat_lock import SeatLockSystem
import time
def test_lock_and_expire():
    s = SeatLockSystem()
    assert s.lock("A1", "user1")
    s.locked_seats["A1"]["expire"] = time.time() - 1
    assert s.is_locked("A1") is False

def test_relock_after_expire():
    s = SeatLockSystem()
    s.lock("A1", "user1")
    s.locked_seats["A1"]["expire"] = time.time() - 1
    s.lock("A1", "user2")
    assert s.is_locked("A1")

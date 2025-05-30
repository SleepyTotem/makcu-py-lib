# tests/test_lock_state.py
from makcu import MouseButton

def test_lock_state(makcu):
    print("Locking LEFT button...")
    makcu.lock_left(True)

    print("Querying lock state while LEFT is locked...")
    assert makcu.is_button_locked(MouseButton.LEFT)

    print("Querying all lock states...")
    all_states = makcu.get_all_lock_states()
    print(f"All lock states: {all_states}")

    assert all_states["LEFT"] is True
    assert isinstance(all_states["RIGHT"], bool)

    print("Unlocking LEFT button...")
    makcu.lock_left(False)

    print("Rechecking LEFT lock state after unlock...")
    assert not makcu.is_button_locked(MouseButton.LEFT)
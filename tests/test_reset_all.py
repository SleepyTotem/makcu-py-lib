# test_reset_all.py

def test_reset_all(makcu):
    # Unlock all buttons
    makcu.mouse.lock_left(False)
    makcu.mouse.lock_right(False)
    makcu.mouse.lock_middle(False)
    makcu.mouse.lock_side1(False)
    makcu.mouse.lock_side2(False)
    makcu.mouse.lock_x(False)
    makcu.mouse.lock_y(False)

    # Check lock states to confirm everything is clean
    states = makcu.mouse.get_all_lock_states()

    assert all(state is False for state in states.values() if state is not None), \
        f"Expected all unlocked, got: {states}"

    # Optionally disable monitoring
    makcu.enable_button_monitoring(False)
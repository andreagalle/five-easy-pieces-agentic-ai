import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from worlds import Action, Percept, VacuumWorld, WorldConfig, run_episode

from agent.programs import ModelBasedReflexAgent, State, choose_action, update_state
from agent.run import GRID, main

BLIND_GRID = WorldConfig(width=4, height=4, sense_location=False)


def percept(dirty=False, bumped=False):
    return Percept(None, dirty, bumped)


def sweep(start=(0, 0), steps=200):
    return run_episode(VacuumWorld(BLIND_GRID, start, GRID), ModelBasedReflexAgent(), steps)


def run_quietly(*args):
    with redirect_stdout(io.StringIO()):
        return main(list(args))


class InternalStateTest(unittest.TestCase):
    def test_transition_model_moves_the_believed_position(self):
        state = State(last_action=Action.RIGHT)
        update_state(state, percept())
        self.assertEqual(state.position, (1, 0))

    def test_sensor_model_reads_a_bump_as_a_failed_move_and_a_wall(self):
        state = State(position=(3, 0), last_action=Action.RIGHT)
        update_state(state, percept(bumped=True))
        self.assertEqual(state.position, (3, 0))
        self.assertEqual(state.walls, {"right": 3})

    def test_a_bump_it_didnt_cause_teaches_it_nothing(self):
        state = State()
        update_state(state, percept(bumped=True))
        self.assertEqual(state.walls, {})

    def test_it_remembers_clean_squares_and_forgets_them_if_they_turn_dirty(self):
        state = State()
        update_state(state, percept())
        self.assertIn((0, 0), state.clean)
        update_state(state, percept(dirty=True))
        self.assertNotIn((0, 0), state.clean)

    def test_state_survives_a_trip_through_json(self):
        state = State(position=(2, 1), last_action=Action.LEFT, clean={(0, 0), (1, 0)}, walls={"left": 0, "top": 0})
        restored = State.from_json(json.loads(json.dumps(state.to_json())))
        self.assertEqual(restored, state)


class RulesTest(unittest.TestCase):
    def test_turns_before_a_wall_it_already_knows(self):
        state = State(position=(3, 0), clean={(3, 0)}, walls={"left": 0, "top": 0, "right": 3})
        self.assertEqual(choose_action(state), Action.DOWN)

    def test_stops_once_the_map_is_complete_and_clean(self):
        walls = {"left": 0, "right": 1, "top": 0, "bottom": 0}
        self.assertEqual(choose_action(State(position=(1, 0), clean={(0, 0), (1, 0)}, walls=walls)), Action.NOOP)


class SweepTest(unittest.TestCase):
    def test_cleans_the_grid_from_any_start_and_then_stops(self):
        for start in GRID:
            with self.subTest(start=start):
                episode = sweep(start)
                self.assertEqual(episode.final_dirty, ())
                self.assertEqual(episode.steps[-1].action, Action.NOOP)

    def test_on_the_same_grid_it_beats_every_agent_of_piece_1(self):
        episode = sweep()
        self.assertEqual((episode.all_clean_at, episode.score), (34, 2918))
        self.assertGreater(episode.score, 2666)  # the random agent of piece 1

    def test_bumps_into_each_wall_once(self):
        self.assertEqual(sum(step.percept.bumped for step in sweep().steps), 4)

    def test_needs_no_coin_where_the_blind_agent_of_piece_1_looped(self):
        world = VacuumWorld(WorldConfig(sense_location=False), (1, 0), [(0, 0), (1, 0)])
        self.assertEqual(run_episode(world, ModelBasedReflexAgent(), 10).score, 18)


class ReportTest(unittest.TestCase):
    def run_and_read(self, directory, *route):
        run_quietly("--out", directory, *route)
        return (Path(directory) / "results.json").read_bytes()

    def test_stopping_and_resuming_changes_nothing(self):
        with tempfile.TemporaryDirectory() as whole:
            expected = self.run_and_read(whole)
        for step in (1, 18, 34, 199):
            with self.subTest(step=step), tempfile.TemporaryDirectory() as halves:
                run_quietly("--out", halves, "--stop-at", str(step))
                self.assertFalse((Path(halves) / "results.json").exists())
                self.assertEqual(self.run_and_read(halves, "--resume"), expected)

    def test_losing_the_state_costs_time_but_the_grid_still_gets_clean(self):
        with tempfile.TemporaryDirectory() as out:
            scenarios = json.loads(self.run_and_read(out))["scenarios"]
        by_name = {scenario["name"]: scenario for scenario in scenarios}
        self.assertEqual(by_name["grid-amnesia"]["final_dirty"], [])
        self.assertGreater(by_name["grid-amnesia"]["all_clean_at"], by_name["grid-model"]["all_clean_at"])
        self.assertLess(by_name["grid-amnesia"]["score"], by_name["grid-model"]["score"])

    def test_resume_without_a_saved_state_says_so(self):
        with tempfile.TemporaryDirectory() as out, redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit):
                main(["--out", out, "--resume"])
        self.assertIn("nothing to resume", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

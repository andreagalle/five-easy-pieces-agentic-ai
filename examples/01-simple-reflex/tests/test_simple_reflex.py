import io
import itertools
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from worlds import Action, VacuumWorld, WorldConfig, run_episode

from agent.programs import RandomizedReflexAgent, blind_reflex_agent, reflex_vacuum_agent
from agent.run import main

A, B = (0, 0), (1, 0)
DIRT_CONFIGS = [[], [A], [B], [A, B]]


class SightedAgentTest(unittest.TestCase):
    def test_cleans_two_squares_from_any_start_within_three_steps(self):
        for start, dirty in itertools.product([A, B], DIRT_CONFIGS):
            with self.subTest(start=start, dirty=dirty):
                world = VacuumWorld(WorldConfig(), start, dirty)
                episode = run_episode(world, reflex_vacuum_agent, steps=3)
                self.assertEqual(episode.final_dirty, ())


class BlindAgentTest(unittest.TestCase):
    def test_loops_forever_when_dirt_is_behind_it(self):
        world = VacuumWorld(WorldConfig(sense_location=False), start=B, dirty=[A, B])
        episode = run_episode(world, blind_reflex_agent, steps=100)
        self.assertEqual(episode.final_dirty, (A,))
        last = episode.steps[-10:]
        self.assertTrue(all(s.action is Action.RIGHT and s.percept.bumped for s in last))


class RandomizedAgentTest(unittest.TestCase):
    def test_escapes_the_loop(self):
        for seed in range(20):
            with self.subTest(seed=seed):
                world = VacuumWorld(WorldConfig(sense_location=False), start=B, dirty=[A, B])
                episode = run_episode(world, RandomizedReflexAgent(seed), steps=30)
                self.assertEqual(episode.final_dirty, ())


class ReportTest(unittest.TestCase):
    def test_report_is_byte_identical_across_runs(self):
        outputs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(main(["--out", tmp]), 0)
                outputs.append((stdout.getvalue(), (Path(tmp) / "results.json").read_bytes()))
        self.assertEqual(outputs[0], outputs[1])


if __name__ == "__main__":
    unittest.main()

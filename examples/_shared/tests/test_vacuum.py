import random
import unittest

from worlds import Action, Percept, VacuumWorld, WorldConfig, pick, run_episode


class PerceptTest(unittest.TestCase):
    def test_location_sensor_on(self):
        world = VacuumWorld(WorldConfig(), start=(1, 0), dirty=[(1, 0)])
        self.assertEqual(world.percept(), Percept(location=(1, 0), dirty=True, bumped=False))

    def test_location_sensor_off(self):
        world = VacuumWorld(WorldConfig(sense_location=False), start=(1, 0))
        self.assertIsNone(world.percept().location)

    def test_rejects_squares_outside_the_grid(self):
        with self.assertRaises(ValueError):
            VacuumWorld(WorldConfig(width=2, height=1), dirty=[(2, 0)])


class DynamicsTest(unittest.TestCase):
    def test_suck_cleans_the_current_square_only(self):
        world = VacuumWorld(WorldConfig(), start=(0, 0), dirty=[(0, 0), (1, 0)])
        world.execute(Action.SUCK)
        self.assertEqual(world.dirty, {(1, 0)})

    def test_move_and_bump(self):
        world = VacuumWorld(WorldConfig(width=2, height=2), start=(0, 0))
        world.execute(Action.RIGHT)
        self.assertEqual(world.location, (1, 0))
        world.execute(Action.RIGHT)
        self.assertEqual(world.location, (1, 0))
        self.assertTrue(world.percept().bumped)
        world.execute(Action.DOWN)
        self.assertEqual(world.location, (1, 1))
        self.assertFalse(world.percept().bumped)

    def test_certain_slip_never_moves(self):
        world = VacuumWorld(WorldConfig(width=3, slip=1.0), start=(0, 0))
        for _ in range(5):
            world.execute(Action.RIGHT)
        self.assertEqual(world.location, (0, 0))

    def test_certain_dirt_refills_every_square(self):
        world = VacuumWorld(WorldConfig(width=3, height=2, dirt_rate=1.0))
        world.execute(Action.NOOP)
        self.assertEqual(world.dirty, set(world.squares))


class EpisodeTest(unittest.TestCase):
    def test_score_counts_clean_squares_per_step(self):
        world = VacuumWorld(WorldConfig(), dirty=[(0, 0)])
        episode = run_episode(world, lambda p: Action.SUCK if p.dirty else Action.NOOP, steps=3)
        self.assertEqual(episode.score, 6)
        self.assertEqual(episode.max_score, 6)
        self.assertEqual(episode.all_clean_at, 1)
        self.assertEqual(episode.final_dirty, ())

    def test_episode_records_path_and_clean_counts(self):
        world = VacuumWorld(WorldConfig(width=3), start=(0, 0), dirty=[(1, 0), (2, 0)])
        episode = run_episode(world, lambda p: Action.SUCK if p.dirty else Action.RIGHT, steps=5)
        self.assertEqual(episode.start, (0, 0))
        self.assertEqual(episode.dirty_start, ((1, 0), (2, 0)))
        self.assertEqual([s.location for s in episode.steps], [(1, 0), (1, 0), (2, 0), (2, 0), (2, 0)])
        self.assertEqual([s.clean for s in episode.steps], [1, 2, 2, 3, 3])
        self.assertEqual(episode.score, sum(s.clean for s in episode.steps))

    def test_same_seed_same_episode(self):
        def run():
            config = WorldConfig(width=4, height=3, slip=0.3, dirt_rate=0.05, seed=7)
            world = VacuumWorld(config, dirty=[(3, 2)])
            rng = random.Random(7)
            return run_episode(world, lambda p: pick(rng, list(Action)), steps=50)

        self.assertEqual(run(), run())

    def test_pick_uses_random_only(self):
        # The sequence of random() for a seed is fixed across platforms and Python 3 versions.
        rng = random.Random(1)
        self.assertEqual([pick(rng, "ab") for _ in range(6)], ["a", "b", "b", "a", "a", "a"])


if __name__ == "__main__":
    unittest.main()

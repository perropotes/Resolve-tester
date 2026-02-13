import unittest

from src.clip_helpers import (
    CUBIC_SPLINE,
    SidePushConfig,
    apply_side_push_to_clip,
    build_side_push_keyframes,
)


class ClipDouble:
    def __init__(self):
        self.keyframes = []
        self.values = {}

    def set_keyframe(self, parameter, frame, value, in_spline, out_spline):
        self.keyframes.append((parameter, frame, value, in_spline, out_spline))

    def set_value(self, parameter, value):
        self.values[parameter] = value


class ClipHelpersTest(unittest.TestCase):
    def test_build_side_push_keyframes_matches_requested_timing(self):
        keyframes = build_side_push_keyframes(clip_start_frame=100, clip_duration_frames=80)

        self.assertEqual(keyframes["crop_left"][0].frame, 100)
        self.assertEqual(keyframes["crop_left"][0].value, 1920)
        self.assertEqual(keyframes["crop_left"][1].frame, 112)
        self.assertEqual(keyframes["crop_left"][1].value, 0)

        self.assertEqual(keyframes["crop_right"][0].frame, 167)
        self.assertEqual(keyframes["crop_right"][0].value, 0)
        self.assertEqual(keyframes["crop_right"][1].frame, 179)
        self.assertEqual(keyframes["crop_right"][1].value, 1920)

        all_splines = {
            spline
            for side in ("crop_left", "crop_right", "blur")
            for kf in keyframes[side]
            for spline in (kf.in_spline, kf.out_spline)
        }
        self.assertEqual(all_splines, {CUBIC_SPLINE})
        self.assertEqual(keyframes["blur"][0].value, 0.2)

    def test_apply_side_push_to_clip_writes_values_and_keyframes(self):
        clip = ClipDouble()
        apply_side_push_to_clip(clip, clip_start_frame=0, clip_duration_frames=30)

        self.assertEqual(clip.values["blur"], 0.2)
        self.assertEqual(len(clip.keyframes), 5)

    def test_raises_when_clip_cannot_fit_both_transitions(self):
        with self.assertRaises(ValueError):
            build_side_push_keyframes(
                clip_start_frame=0,
                clip_duration_frames=24,
                config=SidePushConfig(transition_frames=12),
            )

    def test_accepts_clip_longer_than_both_transitions(self):
        keyframes = build_side_push_keyframes(
            clip_start_frame=0,
            clip_duration_frames=25,
            config=SidePushConfig(transition_frames=12),
        )

        self.assertEqual(keyframes["crop_left"][1].frame, 12)
        self.assertEqual(keyframes["crop_right"][0].frame, 12)


if __name__ == "__main__":
    unittest.main()

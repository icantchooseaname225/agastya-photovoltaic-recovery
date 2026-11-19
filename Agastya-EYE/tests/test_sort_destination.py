import unittest

from inference.triage import sort_destination, sort_lane_decision


class SortDestinationTests(unittest.TestCase):
    def test_routes_map_to_explicit_non_actuating_line_destinations(self):
        self.assertEqual(sort_destination("SECOND_LIFE_REVIEW"), "REUSE_ASSESSMENT")
        self.assertEqual(sort_destination("STAGE_2_CSI"), "STAGE_2_RECYCLING_INTAKE")
        self.assertEqual(sort_destination("LICENSED_THIN_FILM_HANDLER"), "LICENSED_HANDLER")
        self.assertEqual(sort_destination("SAFETY_HOLD"), "QUARANTINE")

    def test_unknown_routes_fail_closed_to_manual_review(self):
        self.assertEqual(sort_destination("unrecognized"), "MANUAL_REVIEW")

    def test_reuse_candidate_goes_left_only_after_documented_pass(self):
        result = sort_lane_decision("SECOND_LIFE_REVIEW", panel_technology="c_si", electrical_test="pass")
        self.assertEqual(result["lane"], "LEFT")
        self.assertEqual(result["decision"], "REUSE_CANDIDATE")
        self.assertFalse(result["actuator_commanded"])

    def test_recycling_route_goes_right_only_after_isolation_confirmation(self):
        waiting = sort_lane_decision("STAGE_2_CSI", panel_technology="c_si")
        ready = sort_lane_decision(
            "STAGE_2_CSI", panel_technology="c_si", stage2_isolation_confirmed=True
        )
        self.assertEqual(waiting["lane"], "HOLD")
        self.assertEqual(ready["lane"], "RIGHT")
        self.assertEqual(ready["decision"], "RECYCLE_CANDIDATE")

    def test_missing_electrical_pass_or_structural_damage_holds_reuse(self):
        no_test = sort_lane_decision("SECOND_LIFE_REVIEW", panel_technology="c_si")
        damaged = sort_lane_decision(
            "SECOND_LIFE_REVIEW", panel_technology="c_si", electrical_test="pass",
            confirmed_visual_label="broken",
        )
        self.assertEqual(no_test["lane"], "HOLD")
        self.assertEqual(damaged["lane"], "HOLD")

    def test_unknown_and_thin_film_routes_never_enter_two_lane_demo(self):
        self.assertEqual(sort_lane_decision("HUMAN_REVIEW")["lane"], "HOLD")
        self.assertEqual(sort_lane_decision("LICENSED_THIN_FILM_HANDLER")["lane"], "HOLD")


if __name__ == "__main__":
    unittest.main()

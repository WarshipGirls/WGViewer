import unittest


class FunctionalTests(unittest.TestCase):

    def test_data_init_generator(self):
        from src.data.__auto_gen__ import start_data_generator
        self.assertEqual(start_data_generator(), True)

    def test_utils_init_generator(self):
        from src.utils.__auto_gen__ import start_utils_generator
        self.assertEqual(start_utils_generator(), True)

    # def test_english_names(self):
    # TODO: ensure no repeated names in names.eng_name
    # self.assertEqual()

    def test_get_repair_type_full_hp_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 32}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 0)

    def test_get_repair_type_full_hp_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 31}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 0)

    def test_get_repair_type_slightly_damaged_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 31}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 30}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 29}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 28}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 26}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 25}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 24}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 23}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 22}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 21}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 20}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 19}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 18}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 17}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 16}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 1)

    def test_get_repair_type_slightly_damaged_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 30}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 29}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 28}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 26}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 25}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 24}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 23}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 22}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 21}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 20}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 19}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 18}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 17}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 16}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 1)

    def test_get_repair_type_moderately_damaged_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 15}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 14}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 13}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 12}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 10}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 9}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 8}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 2)

    def test_get_repair_type_moderately_damaged_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 15}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 14}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 13}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 12}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 10}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 9}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)
        d = {'battleProps': {'hp': 8}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 2)

    def test_get_repair_type_hevaily_damaged_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 7}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 6}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 5}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 4}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 3}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 2}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 1}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 3)

    def test_get_repair_type_hevaily_damaged_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 7}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 6}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 5}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 4}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 3}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 2}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 1}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 3)

    def test_get_repair_type_sunken_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 0}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), 4)

    def test_get_repair_type_sunken_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 0}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), 4)

    def test_get_repair_type_abnormality_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': -1}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), -1)
        d = {'battleProps': {'hp': 33}, 'battlePropsMax': {'hp': 32}}
        self.assertEqual(get_repair_type(d), -1)

    def test_get_repair_type_abnormality_non_quadruple(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': -1}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), -1)
        d = {'battleProps': {'hp': 32}, 'battlePropsMax': {'hp': 31}}
        self.assertEqual(get_repair_type(d), -1)

    def test_get_repair_type_random(self):
        from src.utils.game.combat import get_repair_type
        d = {'battleProps': {'hp': 19}, 'battlePropsMax': {'hp': 77}}
        self.assertEqual(get_repair_type(d), 3)
        d = {'battleProps': {'hp': 51}, 'battlePropsMax': {'hp': 101}}
        self.assertEqual(get_repair_type(d), 1)
        d = {'battleProps': {'hp': 50}, 'battlePropsMax': {'hp': 101}}
        self.assertEqual(get_repair_type(d), 2)


if __name__ == '__main__':
    unittest.main()

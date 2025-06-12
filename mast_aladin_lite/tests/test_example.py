from mast_aladin_lite import MastAladin


def test_instance_creation(MastAladin_helper):
    assert isinstance(MastAladin_helper, MastAladin)

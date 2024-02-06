from connect_toolbox import validate


def test_dx():

    def fun(dx):
        validate.dx(dx)
        return dx

    assert fun("adhd") == "adhd"
    assert fun("alzheimer") == "alzheimer"
    assert fun("anxiety") == "anxiety"
    assert fun("autism") == "autism"
    assert fun("bipolar") == "bipolar"
    assert fun("dementia_other") == "dementia_other"
    assert fun("depression") == "depression"
    assert fun("ftd") == "ftd"
    assert fun("insomnia") == "insomnia"
    assert fun("mci") == "mci"
    assert fun("ocd") == "ocd"
    assert fun("pain") == "pain"
    assert fun("parkinson") == "parkinson"
    assert fun("schizophrenia") == "schizophrenia"
    try:
        fun("test")
        assert False
    except AssertionError as e:
        assert (
            str(e)
            == "Unrecognized diagnosis test - no disease map available for this diagnosis."
        )


def test_check_modality_and_metric():
    def fun(modality, metric):
        validate.modality_and_metric(modality, metric)
        return modality, metric

    assert fun("functional-connectivity", "gmean_scrubbed_0.01-0.1") == (
        "functional-connectivity",
        "gmean_scrubbed_0.01-0.1",
    )
    assert fun("functional-connectivity", "scrubbed_0.01-0.1") == (
        "functional-connectivity",
        "scrubbed_0.01-0.1",
    )
    assert fun("structural-connectivity", "mean_fa") == (
        "structural-connectivity",
        "mean_fa",
    )
    assert fun("morphology", "thickness") == ("morphology", "thickness")
    assert fun("morphology", "volume") == ("morphology", "volume")
    assert fun("morphology", "surface_area") == ("morphology", "surface_area")

    try:
        fun("test", "test")
        assert False
    except AssertionError as e:
        assert str(e) == "Unrecognized modality test."

    try:
        fun("functional-connectivity", "mean_fa")
        assert False
    except AssertionError as e:
        assert (
            str(e)
            == "Unrecognized metric mean_fa (available metrics: ['gmean_scrubbed_0.01-0.1', 'scrubbed_0.01-0.1'])."
        )


def test_atlas():
    def fun(atlas):
        validate.atlas(atlas)
        return atlas

    assert fun("aparc+aseg") == "aparc+aseg"
    assert fun("aparc") == "aparc"
    try:
        fun("test")
        assert False
    except AssertionError as e:
        assert str(e) == "Unrecognized atlas test."

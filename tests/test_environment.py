import arviz
import jax
import numpyro


def test_inference_environment_has_a_device():
    assert jax.devices()
    assert numpyro.__version__ == "0.21.0"
    assert hasattr(arviz, "InferenceData")

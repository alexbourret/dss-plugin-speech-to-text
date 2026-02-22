import whisper
from safe_logger import SafeLogger
from dss_selector_choice import DSSSelectorChoices


logger = SafeLogger("speech-to-text plugin")


def do(payload, config, plugin_config, inputs):
    choices = DSSSelectorChoices()
    try:
        for model_name in whisper._MODELS:
            logger.info("found {}".format(model_name))
            choices.append(model_name, model_name)
    except Exception as error:
        logger.error("Could not retrieve model list", error)
        choices.append("turbo", "turbo")
    return choices.to_dss()

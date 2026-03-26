from dotenv import load_dotenv
import os
from enum import Enum

# --- CONFIGURAÇÃO DA IA ---
load_dotenv()
API_KEY = os.environ.get("API_KEY")

class Modelos(Enum):
    DeepSeek = "tngtech/deepseek-r1t2-chimera:free"
    Nemotron_3_Super = "arcee-ai/trinity-large-preview:free"
    StepFun_35_FLASH = "stepfun/step-3.5-flash:free"

    @property
    def valor(self):
        modelos = {
            "DeepSeek": {
                "name": "deepseek-r1t2-chimera",
                "model": "tngtech/deepseek-r1t2-chimera:free",
                "provider": "deepseek"
            },
            "Nemotron_3_Super": {
                "name": "Nemotron_3_Super",
                "model": "nvidia/nemotron-3-super-120b-a12b:free",
                "provider": "NVIDIA"
            },
            "StepFun_35_FLASH": {
                "name": "Step-3.5-flash",
                "model": "stepfun/step-3.5-flash:free",
                "provider": "StepFun"
            }
        }
        return modelos[self.name]

# --- CONFIGURAÇÃO DA SERIAL ---
porta_arduino = 'COM24' 
baud_rate = 9600
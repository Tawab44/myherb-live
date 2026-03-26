import torch
from torchvision import transforms
from PIL import Image
import gradio as gr

# Load model
model = torch.jit.load("model.pt", map_location="cpu")
model.eval()

# -------------------------
# CLASS NAMES
# -------------------------

CLASS_NAMES = [
    "Aerva lanata (Mountain Knotgrass)",
    "Aloe vera (Ghritkumari)",
    "Andrographis paniculata (Kalmegh)",
    "Bacopa monnieri (Brahmi)",
    "Calotropis gigantea (Aak, Madar)",
    "Centella asiatica (Gotu Kola)",
    "Chromolaena odorata (Siam Weed)",
    "Cissus quadrangularis (Hadjod)",
    "Clerodendrum infortunatum (Bharangi)",
    "Clitoria ternatea (Aparajita, Shankhpushpi Blue variety)",
    "Coccinia grandis (Kundru, Ivy Gourd)",
    "Curcuma longa (Haldi, Turmeric)",
    "Datura metel Linn (Dhatura)",
    "Desmodium gangeticum (Shalaparni)",
    "Hemigraphis colorata (Red Flame Ivy)",
    "Kaempferia galanga Linn (Kachur, Aromatic Ginger)",
    "Mentha spicata (Pudina, Spearmint)",
    "Not a herb",
    "Ocimum gratissimum (Ram Tulsi, Vana Tulsi)",
    "Ocimum tenuiflorum (Krishna Tulsi, Holy Basil)",
    "Oxalis corniculata (Changeri, Indian Sorrel)",
    "Peperomia pellucida (Shiny Bush, Rat’s Ear)",
    "Phyllanthus niruri (Bhumi Amla, Stonebreaker)",
    "Piper betle (Paan)",
    "Piper longum (Pippali, Long Pepper)",
    "Piper nigrum (Kali Mirch, Black Pepper)",
    "Plectranthus barbatus (Patharchur, Indian Coleus)",
    "Plumbago indica (Red Chitrak)",
    "Pseudarthria viscida (Salaparni)",
    "Ricinus communis Linn (Arandi, Castor Plant)",
    "Tinospora cordifolia (Giloy, Guduchi)"
]

# Transforms
transform_resnet = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

transform_inception = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
])

# Prediction function
def predict(image):
    img = image.convert("RGB")

    img_res = transform_resnet(img).unsqueeze(0)
    img_inc = transform_inception(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_res, img_inc)
        probs = torch.softmax(outputs, dim=1)
        probability, predicted_index = torch.max(probs, 1)

    return {
        "class": CLASS_NAMES[predicted_index.item()],
        "probability": float(probability.item())
    }

# Gradio interface
iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="json",
    title="Herb AI 🌿"
)

iface.launch()
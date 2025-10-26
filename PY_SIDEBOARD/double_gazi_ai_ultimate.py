# ==========================================
# Double Gazi AI Ultimate 2.6 - Komplett lauffähig
# ==========================================

import os, copy, tempfile, pickle, numpy as np, json
from PIL import Image as PILImage
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
# ==========================================
# Double Gazi AI Ultimate 2.6 - Komplett lauffähig
# ==========================================

import os, copy, tempfile, pickle, numpy as np, json
from PIL import Image as PILImage
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionInpaintPipeline
from scipy.ndimage import gaussian_filter
from threading import Thread

# ==========================================
# 1) Layer Management
# ==========================================
class LayeredGraphic:
    def __init__(self, width=512, height=512):
        self.width, self.height = width, height
        self.layers = [{'image': np.zeros((height, width, 3), dtype=np.uint8),
                        'opacity':1.0, 'visible':True, 'name':'Hintergrund'}]
        self.selected_layer_index = 0
        self.history = [self._snapshot()]
        self.redo_stack = []

    def _snapshot(self):
        return copy.deepcopy(self.layers)

    def blend_layers(self):
        final = np.zeros((self.height, self.width, 3), dtype=np.float64)
        for layer in reversed(self.layers):
            if layer['visible']:
                alpha = layer['opacity']
                img_float = layer['image'].astype(np.float64)/255.0
                final = final*(1-alpha) + img_float*alpha
        return np.clip(final*255,0,255).astype(np.uint8)

    def add_layer(self, image=None, name="Neue Ebene"):
        if image is None:
            image = np.zeros((self.height, self.width,3), dtype=np.uint8)
        self.layers.append({'image':image, 'opacity':1.0, 'visible':True,
                            'name':f'{name} {len(self.layers)}'})
        self.selected_layer_index = len(self.layers)-1
        self.add_history()

    def delete_layer(self):
        if len(self.layers) > 1:
            del self.layers[self.selected_layer_index]
            self.selected_layer_index = max(0,self.selected_layer_index-1)
            self.add_history()

    def add_history(self):
        self.history.append(self._snapshot())
        self.redo_stack.clear()
        if len(self.history) > 50:
            self.history.pop(0)

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.layers = copy.deepcopy(self.history[-1])
            return True
        return False

    def redo(self):
        if self.redo_stack:
            self.history.append(self.redo_stack.pop())
            self.layers = copy.deepcopy(self.history[-1])
            return True
        return False

# ==========================================
# 2) KI Logo Generator
# ==========================================
class LogoGenerator:
    def __init__(self, model_name="runwayml/stable-diffusion-v1-5",
                 inpaint_model="runwayml/stable-diffusion-inpainting"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.inpaint_pipe = None
        self.model_name = model_name
        self.inpaint_model = inpaint_model

    def load_models(self, progress_callback=None):
        try:
            if progress_callback: progress_callback("Lade Stable Diffusion...")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device=="cuda" else torch.float32
            ).to(self.device)
            if progress_callback: progress_callback("Lade Inpainting-Modell...")
            self.inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
                self.inpaint_model,
                torch_dtype=torch.float16 if self.device=="cuda" else torch.float32
            ).to(self.device)
            return True,None
        except Exception as e:
            return False,f"Fehler beim Laden der Modelle: {e}"

    def generate(self, prompt, num_images=1, height=256, width=256):
        if self.pipe is None:
            return [], "Modell nicht geladen."
        results = []
        try:
            for _ in range(num_images):
                image = self.pipe(prompt, height=height, width=width).images[0]
                temp_png = os.path.join(tempfile.gettempdir(), f"logo_{np.random.randint(0,10000)}.png")
                image.save(temp_png)
                results.append(temp_png)
        except Exception as e:
            return [], f"Generierungsfehler: {e}"
        return results,None

    def inpaint(self, image: PILImage.Image, mask: PILImage.Image, prompt: str):
        if self.inpaint_pipe is None:
            return image, "Modell nicht geladen."
        try:
            result = self.inpaint_pipe(prompt=prompt, image=image.convert("RGB"), mask_image=mask.convert("RGB")).images[0]
            return result, None
        except Exception as e:
            return image, f"Inpainting fehlgeschlagen: {e}"

# ==========================================
# 3) Terminal Sicherheitsplan
# ==========================================
def load_security_plan(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fehler beim Laden der Datei: {e}")
        return None

def display_roadmap(plan):
    if not plan: return
    print("=" * 50)
    print(f"Projekt: {plan['project_name']}")
    print(f"Beschreibung: {plan['description']}")
    print("=" * 50)
    print("\nRoadmap für den Aufbau des Sicherheitsteams:\n")
    for phase in plan['roadmap']:
        print(f"--- {phase['phase_name']} ({phase['duration']}) ---")
        print(f"Ziel: {phase['goal']}")
        print("\n  Rollen:")
        for role in phase['components']['roles']:
            print(f"    - {role}")
        print("\n  Prozesse:")
        for process in phase['components']['processes']:
            print(f"    - {process}")
        print("\n" + "-" * 20 + "\n")

def find_in_roadmap(plan, search_term):
    if not plan: print("Plan konnte nicht geladen werden."); return
    found = False
    print(f"\nSuche nach '{search_term}' im Plan...")
    for phase in plan['roadmap']:
        roles = [r for r in phase['components']['roles'] if search_term.lower() in r.lower()]
        processes = [p for p in phase['components']['processes'] if search_term.lower() in p.lower()]
        if roles or processes:
            print(f"\n--- Gefunden in: {phase['phase_name']} ({phase['duration']}) ---")
            if roles: print("Rollen:\n  " + "\n  ".join(roles))
            if processes: print("Prozesse:\n  " + "\n  ".join(processes))
            found = True
    if not found: print(f"Keine Ergebnisse für '{search_term}' gefunden.")

# ==========================================
# 4) Haupt-App
# ==========================================
class DoubleGaziAIUltimateApp(App):
    def build(self):
        self.graphic = LayeredGraphic()
        self.logo_gen = LogoGenerator()
        self.active_tool = "Pinsel"
        self.brush_color = (255,0,0)
        self.brush_size = 10
        self.last_touch_pos = None
        self.clone_source = None
        self.drawing_mask = np.zeros((self.graphic.height,self.graphic.width),dtype=np.uint8)

        Window.bind(on_key_down=self.on_keyboard)

        root_layout = BoxLayout(orientation='vertical')
        self.status_label = Label(text="", size_hint_y=0.05)
        root_layout.add_widget(self.status_label)
        main_layout = BoxLayout(orientation='horizontal', spacing=5)
        root_layout.add_widget(main_layout)

        # Canvas
        self.canvas_tab = FloatLayout()
        self.canvas_img = Image(allow_stretch=True, keep_ratio=True)
        self.canvas_tab.add_widget(self.canvas_img)
        self.canvas_img.bind(on_touch_down=self.on_touch_down,
                             on_touch_move=self.on_touch_move,
                             on_touch_up=self.on_touch_up)
        main_layout.add_widget(self.canvas_tab)

        # Sidebar
        sidebar = BoxLayout(orientation='vertical', size_hint_x=0.25, spacing=5, padding=5)
        main_layout.add_widget(sidebar)

        # Tools
        tool_grid = GridLayout(cols=2, spacing=5, size_hint_y=0.35)
        tools = ["Pinsel","Airbrush","Weichzeichner","Radierer","Kopierstempel","Füllwerkzeug","Formen",
                 "3D Verschieben","3D Rotieren","3D Skalieren","Inpainting"]
        self.tool_buttons = {}
        for t in tools:
            btn = Button(text=t)
            btn.bind(on_press=lambda inst, tool=t: self.set_tool(tool, inst))
            tool_grid.add_widget(btn)
            self.tool_buttons[t] = btn
        sidebar.add_widget(tool_grid)
        self.set_tool("Pinsel", self.tool_buttons["Pinsel"])

        # Brush & Color
        brush_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        brush_layout.add_widget(Label(text="Pinselgröße:"))
        self.brush_slider = Slider(min=1,max=100,value=self.brush_size,step=1)
        self.brush_slider.bind(value=self.update_brush_size)
        brush_layout.add_widget(self.brush_slider)
        color_btn = Button(text="Pinsel-Farbe", size_hint_y=None, height=40)
        color_btn.bind(on_press=self.show_color_picker)
        brush_layout.add_widget(color_btn)
        sidebar.add_widget(brush_layout)

        # Layers
        layer_panel = BoxLayout(orientation='vertical', size_hint_y=0.5)
        layer_panel.add_widget(Label(text="Ebenen", size_hint_y=None, height=30))
        self.layer_list = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.layer_list.bind(minimum_height=self.layer_list.setter('height'))
        layer_scroll = ScrollView(do_scroll_x=False)
        layer_scroll.add_widget(self.layer_list)
        layer_panel.add_widget(layer_scroll)
        layer_controls = BoxLayout(size_hint_y=None, height=40)
        layer_controls.add_widget(Button(text="+", on_press=lambda x: self.graphic.add_layer() or self.update_layer_list()))
        layer_controls.add_widget(Button(text="–", on_press=lambda x: self.graphic.delete_layer() or self.update_layer_list()))
        layer_panel.add_widget(layer_controls)
        sidebar.add_widget(layer_panel)
        self.update_layer_list()

        # Undo/Redo
        sidebar.add_widget(Button(text="Undo", on_press=lambda x: self.graphic.undo() and self.update_canvas()))
        sidebar.add_widget(Button(text="Redo", on_press=lambda x: self.graphic.redo() and self.update_canvas()))

        # Save/Load
        save_layout = BoxLayout(size_hint_y=0.05)
        save_layout.add_widget(Button(text="Canvas speichern", on_press=self.save_canvas))
        save_layout.add_widget(Button(text="Projekt speichern", on_press=self.save_project))
        save_layout.add_widget(Button(text="Projekt laden", on_press=self.load_project))
        root_layout.add_widget(save_layout)

        # KI Prompt
        self.logo_prompt_input = TextInput(hint_text="Prompt für KI-Generierung...", multiline=False, size_hint_y=0.08)
        root_layout.add_widget(self.logo_prompt_input)
        self.logo_gallery = GridLayout(cols=2, spacing=5, size_hint_y=None)
        self.logo_gallery.bind(minimum_height=self.logo_gallery.setter("height"))
        scroll = ScrollView(size_hint=(1,0.3))
        scroll.add_widget(self.logo_gallery)
        root_layout.add_widget(scroll)
        ki_buttons_layout = BoxLayout(size_hint_y=0.07)
        logo_btn = Button(text="2D Logo generieren")
        logo_btn.bind(on_press=self.generate_logo)
        inpaint_btn = Button(text="Inpainting ausführen")
        inpaint_btn.bind(on_press=self.show_inpaint_popup)
        ki_buttons_layout.add_widget(logo_btn)
        ki_buttons_layout.add_widget(inpaint_btn)
        root_layout.add_widget(ki_buttons_layout)

        self.update_canvas()
        Clock.schedule_once(lambda dt: self.load_models_popup(),0.1)
        return root_layout

    # -----------------------------
    # Tool-Funktionen
    # -----------------------------
    def set_tool(self, tool, instance):
        self.active_tool = tool
        for btn_tool, btn_inst in self.tool_buttons.items():
            btn_inst.background_color = [1,1,1,1]
        instance.background_color = [0,1,0,1]
        self.status_label.text = f"Werkzeug: {tool}"

    def update_brush_size(self, instance, value):
        self.brush_size = int(value)

    def show_color_picker(self, instance):
        cp = ColorPicker(color=[c/255.0 for c in self.brush_color]+[1])
        popup = Popup(title="Farbe wählen", content=cp, size_hint=(0.8,0.8))
        cp.bind(color=lambda inst,val: setattr(self,'brush_color', tuple(int(c*255) for c in val[:3])))
        popup.open()

    def get_canvas_coords(self,pos):
        x, y = pos
        img_x, img_y = self.canvas_img.pos
        img_w, img_h = self.canvas_img.size
        if img_w==0 or img_h==0:
            return 0,0
        canvas_x = int((x-img_x)/img_w*self.graphic.width)
        canvas_y = int((y-img_y)/img_h*self.graphic.height)
        canvas_x = max(0, min(self.graphic.width-1, canvas_x))
        canvas_y = max(0, min(self.graphic.height-1, canvas_y))
        return canvas_x, canvas_y

    # -----------------------------
    # Touch Events & Drawing
    # -----------------------------
    def on_touch_down(self, instance, touch):
        if self.canvas_img.collide_point(*touch.pos):
            self.last_touch_pos = self.get_canvas_coords(touch.pos)
            if self.active_tool=="Kopierstempel" and touch.button=='right':
                self.clone_source = self.last_touch_pos
            if self.active_tool=="Inpainting":
                self.drawing_mask = np.zeros_like(self.drawing_mask)
            self.graphic.add_history()
            return True

    def on_touch_move(self, instance, touch):
        if self.canvas_img.collide_point(*touch.pos) and self.last_touch_pos:
            x,y = self.get_canvas_coords(touch.pos)
            img = self.graphic.layers[self.graphic.selected_layer_index]['image']

            if self.active_tool=="Pinsel":
                self.draw_line(self.last_touch_pos,(x,y),img,self.brush_color)
            elif self.active_tool=="Airbrush":
                self.draw_line(self.last_touch_pos,(x,y),img,self.brush_color,blur=True)
            elif self.active_tool=="Weichzeichner":
                self.draw_line(self.last_touch_pos,(x,y),img,(0,0,0),blur=True)
            elif self.active_tool=="Radierer":
                self.draw_line(self.last_touch_pos,(x,y),img,(0,0,0),mask_update=True)
            elif self.active_tool=="Kopierstempel" and self.clone_source:
                self.clone_stamp(self.last_touch_pos,(x,y),self.clone_source,img)
            elif self.active_tool=="Inpainting":
                self.draw_line(self.last_touch_pos,(x,y),img,(255,0,0),mask_update=True)
            elif self.active_tool=="3D Verschieben":
                self.layer_translate(self.graphic.selected_layer_index, x-self.last_touch_pos[0], y-self.last_touch_pos[1])
            elif self.active_tool=="3D Rotieren":
                self.layer_rotate(self.graphic.selected_layer_index, 5)
            elif self.active_tool=="3D Skalieren":
                self.layer_scale(self.graphic.selected_layer_index, 1.01)
            self.last_touch_pos = (x,y)
            self.update_canvas()

    def on_touch_up(self, instance, touch):
        self.last_touch_pos = None
        self.graphic.add_history()

    # -----------------------------
    # Line / Stamp / Blur
    # -----------------------------
    def draw_line(self,start,end,img,color,blur=False,mask_update=False):
        x1,y1 = start
        x2,y2 = end
        dx = abs(x2-x1); dy=abs(y2-y1)
        sx=1 if x1<x2 else -1; sy=1 if y1<y2 else -1
        err = dx-dy
        while True:
            for i in range(max(0,x1-self.brush_size), min(self.graphic.width,x1+self.brush_size)):
                for j in range(max(0,y1-self.brush_size), min(self.graphic.height,y1+self.brush_size)):
                    if (i-x1)**2+(j-y1)**2<=self.brush_size**2:
                        if not blur and not mask_update:
                            img[j,i] = color
                        if mask_update:
                            self.drawing_mask[j,i]=255
            if x1==x2 and y1==y2: break
            e2=2*err
            if e2>-dy: err-=dy; x1+=sx
            if e2<dx: err+=dx; y1+=sy
        if blur:
            img[:] = np.clip(gaussian_filter(img.astype(np.float32), sigma=self.brush_size/4),0,255).astype(np.uint8)

    def clone_stamp(self,start,end,source,img):
        sx,sy = source
        ex,ey = end
        src_rect=(max(0,sx-self.brush_size),min(self.graphic.width,sx+self.brush_size),
                  max(0,sy-self.brush_size),min(self.graphic.height,sy+self.brush_size)) 

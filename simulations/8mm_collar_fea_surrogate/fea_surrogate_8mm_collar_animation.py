"""
FEA-style screening animation for an 8 mm steel collar on a 14B nut former.

This is a kinematic axisymmetric mesh animation and surrogate stress/strain field.
It is intended for concept screening and tooling communication, not validated
production nonlinear contact FEA.
"""

from pathlib import Path
import math, json, csv, os
from PIL import Image, ImageDraw, ImageFont

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

BASIS = {
    "collar": {
        "J_max_OD_mm": 10.31,
        "K_max_length_mm": 8.13,
        "target_OD_mm": 10.25,
        "target_length_mm": 8.06,
        "target_ID_from_punch_mm": 8.08,
        "raw_stock_dia_mm": 11.80,
    },
    "tooling": {
        "die_IV_land_dia_mm": 10.25,
        "die_IV_land_length_mm": 8.06,
        "punch_IV_land_dia_mm": 8.08,
        "punch_IV_land_length_mm": 8.05,
        "KO_pin_IV_face_dia_mm": 7.95,
    },
    "warning": "Screening animation only, not a validated nonlinear contact FEA solve."
}

W, H = 1400, 820
plot_left, plot_top, plot_w, plot_h = 160, 170, 880, 470
scale = 82
r_scale = 82
nx, nr = 38, 10

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE, F_H, F, F_SMALL, F_TINY, F_BOLD = font(36, True), font(25, True), font(19), font(15), font(13), font(18, True)

def stress_color(value):
    t = max(0, min(1, value))
    if t < 0.33:
        u = t/0.33
        return (int(40), int(90*(1-u)+170*u), int(190*(1-u)+120*u))
    if t < 0.66:
        u = (t-0.33)/0.33
        return (int(40*(1-u)+230*u), int(170*(1-u)+195*u), int(120*(1-u)+55*u))
    u = (t-0.66)/0.34
    return (int(230*(1-u)+210*u), int(195*(1-u)+60*u), int(55*(1-u)+45*u))

stage_defs = [
    {"name":"Stage I", "title":"Upset preform", "L":3.20, "Ro":5.82, "Ri":0.60, "progress":0.18},
    {"name":"Stage II", "title":"Backward extrusion starts bore", "L":5.20, "Ro":5.45, "Ri":2.50, "progress":0.45},
    {"name":"Stage III", "title":"Semi-finished collar", "L":7.20, "Ro":5.25, "Ri":3.70, "progress":0.72},
    {"name":"Stage IV", "title":"Final contour sizing", "L":8.06, "Ro":5.125, "Ri":4.04, "progress":1.00},
]

def interpolate_stage(stage_idx, frac):
    a = stage_defs[stage_idx]
    b = stage_defs[min(stage_idx+1, len(stage_defs)-1)]
    return {k: a[k] + (b[k]-a[k])*frac for k in ["L", "Ro", "Ri", "progress"]}

def mesh_elements(L, Ri, Ro):
    elems = []
    for i in range(nx):
        x0 = L*i/nx
        x1 = L*(i+1)/nx
        for j in range(nr):
            r0 = Ri + (Ro-Ri)*j/nr
            r1 = Ri + (Ro-Ri)*(j+1)/nr
            xc, rc = (x0+x1)/2, (r0+r1)/2
            die_contact = math.exp(-((Ro-rc)/(0.12+0.08*(Ro-Ri)))**2)
            punch_contact = math.exp(-((rc-Ri)/(0.10+0.07*(Ro-Ri)))**2)
            nose_contact = math.exp(-((L-xc)/(0.75+0.10*L))**2)
            flow_zone = math.exp(-((xc/L-0.55)/0.23)**2) if L else 0
            strain = 0.25 + 1.1*(die_contact*0.45 + punch_contact*0.35 + nose_contact*0.30 + flow_zone*0.25)
            strain *= (0.55 + 0.65*(L/BASIS["collar"]["target_length_mm"]))
            stress = min(1, 0.18 + 0.68*strain/1.5)
            elems.append((x0,x1,r0,r1,stress,strain))
    return elems

def draw_arrow(draw, p1, p2, fill=(60,60,60), width=4):
    x1,y1 = p1; x2,y2 = p2
    draw.line((x1,y1,x2,y2), fill=fill, width=width)
    ang = math.atan2(y2-y1, x2-x1)
    ah = 15
    draw.polygon([(x2,y2),(x2-ah*math.cos(ang-math.pi/6), y2-ah*math.sin(ang-math.pi/6)),(x2-ah*math.cos(ang+math.pi/6), y2-ah*math.sin(ang+math.pi/6))], fill=fill)

def frame(stage_idx, frac):
    d = interpolate_stage(stage_idx, frac)
    L, Ri, Ro, prog = d["L"], d["Ri"], d["Ro"], d["progress"]
    im = Image.new("RGB", (W,H), (248,248,246))
    draw = ImageDraw.Draw(im)
    draw.text((W/2,40), "FEA-Style Screening Animation — 8 mm Steel Collar", fill=(0,0,0), font=F_TITLE, anchor="mm")
    draw.text((W/2,78), BASIS["warning"], fill=(75,75,75), font=F_SMALL, anchor="mm")
    plot_cy = plot_top + plot_h/2
    final_x0 = plot_left + 70
    L_final = BASIS["collar"]["target_length_mm"]
    final_x1 = final_x0 + L_final*scale
    R_outer = BASIS["collar"]["target_OD_mm"]/2
    R_inner = BASIS["collar"]["target_ID_from_punch_mm"]/2
    top_y, bot_y = plot_cy - R_outer*r_scale, plot_cy + R_outer*r_scale
    inner_top, inner_bot = plot_cy - R_inner*r_scale, plot_cy + R_inner*r_scale
    draw.rectangle((final_x0-20, top_y-28, final_x1+45, bot_y+28), outline=(35,35,35), width=4)
    draw.line((final_x0,top_y,final_x1,top_y), fill=(20,20,20), width=5)
    draw.line((final_x0,bot_y,final_x1,bot_y), fill=(20,20,20), width=5)
    draw.text(((final_x0+final_x1)/2, top_y-48), "Die IV final cavity: Ø10.25 × 8.06", fill=(0,0,0), font=F_BOLD, anchor="mm")
    punch_x = final_x0 - 110 + 110*min(1, prog)
    draw.rectangle((punch_x-280, inner_top, final_x1, inner_bot), fill=(170,190,210), outline=(45,75,100), width=3)
    draw.text((punch_x-65, inner_top-35), "Punch IV Ø8.08", fill=(35,65,90), font=F_SMALL, anchor="mm")
    ko_x = final_x1 + 45
    eject_shift = int(max(0, (frac-0.55)/0.45)*80) if stage_idx == 3 else 0
    draw.rectangle((ko_x+eject_shift, plot_cy-38, ko_x+eject_shift+200, plot_cy+38), fill=(190,145,95), outline=(70,45,25), width=3)
    draw.text((ko_x+eject_shift+100, plot_cy+64), "KO Pin IV Ø7.95 face", fill=(75,45,20), font=F_SMALL, anchor="mm")
    x_offset = final_x0 + (L_final-L)*0.15*scale + (eject_shift if stage_idx == 3 else 0)
    for x0,x1,r0,r1,stress,strain in mesh_elements(L, Ri, Ro):
        c = stress_color(stress)
        px0, px1 = x_offset + x0*scale, x_offset + x1*scale
        draw.rectangle((px0, plot_cy-r1*r_scale, px1, plot_cy-r0*r_scale), fill=c, outline=(255,255,255), width=1)
        draw.rectangle((px0, plot_cy+r0*r_scale, px1, plot_cy+r1*r_scale), fill=c, outline=(255,255,255), width=1)
    draw.line((plot_left+20, plot_cy, plot_left+plot_w+40, plot_cy), fill=(100,100,100), width=1)
    draw.text((70,785), "Rule: Die controls OD; Punch controls bore; KO pin ejects only.", fill=(0,0,0), font=F, anchor="lm")
    return im

def main():
    frames = []
    records = []
    for s in range(4):
        for k in range(16):
            frac = k/15
            im = frame(s, frac)
            frames.append(im)
            d = interpolate_stage(s, frac)
            records.append({"frame": len(records), "stage": s+1, "fraction": round(frac,3), "length_mm": round(d["L"],3), "outer_dia_mm": round(2*d["Ro"],3), "bore_dia_mm": round(2*d["Ri"],3), "progress": round(d["progress"],3)})
    frames[0].save(OUT/"fea_surrogate_8mm_collar_14B.gif", save_all=True, append_images=frames[1:], optimize=True, duration=110, loop=0)
    frames[-1].save(OUT/"fea_surrogate_8mm_collar_final_frame.png")
    with (OUT/"fea_surrogate_8mm_collar_frames.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
    (OUT/"fea_surrogate_model_basis.json").write_text(json.dumps(BASIS, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()

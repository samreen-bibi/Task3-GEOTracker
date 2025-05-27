import requests
import folium
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser

def get_geolocation(ip=None):
    try:
        url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
        data = requests.get(url).json()

        if 'bogon' in data:
            raise ValueError("Invalid or private IP address.")

        lat, lon = map(float, data['loc'].split(','))
        return {
            'ip': data.get('ip', 'N/A'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'latitude': lat,
            'longitude': lon,
            'org': data.get('org', 'Unknown'),
            'timezone': data.get('timezone', 'Unknown')
        }
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data:\n{e}")
        return None

def show_map(geo):
    fmap = folium.Map(location=[geo['latitude'], geo['longitude']], zoom_start=12)
    folium.Marker([geo['latitude'], geo['longitude']],
                  popup=f"{geo['city']}, {geo['region']}, {geo['country']}\nIP: {geo['ip']}",
                  tooltip="📍 Location").add_to(fmap)
    fmap.save("map.html")
    webbrowser.open("map.html")

def update_display(geo):
    info = (
        f"🌐 IP: {geo['ip']}\n"
        f"📍 {geo['city']}, {geo['region']}, {geo['country']}\n"
        f"🛰 ISP: {geo['org']}\n"
    )
    info_text.config(state="normal")
    info_text.delete(1.0, tk.END)
    info_text.insert(tk.END, info)
    info_text.config(state="disabled")

def my_location():
    geo = get_geolocation()
    if geo:
        update_display(geo)
        show_map(geo)

def ip_location():
    ip = simpledialog.askstring("Enter IP", "Enter an IP address:")
    if ip:
        geo = get_geolocation(ip.strip())
        if geo:
            update_display(geo)
            show_map(geo)

# === GUI Setup ===

root = tk.Tk()
root.title("IP Geolocation App")
root.geometry("700x400")
root.configure(bg="#1a1a1a")

# Header bar
header = tk.Frame(root, bg="#2e0f4f", height=50)
header.pack(fill="x")

tk.Label(header, text="🌌 Geolocation Tracker", bg="#2e0f4f", fg="white",
         font=("Segoe UI", 16, "bold")).pack(pady=10)

# Body layout: Sidebar + Main panel
body = tk.Frame(root, bg="#1a1a1a")
body.pack(fill="both", expand=True)

# Sidebar
sidebar = tk.Frame(body, bg="#2c2c2c", width=200)
sidebar.pack(side="left", fill="y")

btn_style = {
    "font": ("Segoe UI", 12),
    "bg": "#6a0dad",
    "fg": "white",
    "activebackground": "#8b5cf6",
    "bd": 0,
    "relief": "flat",
    "width": 20,
    "height": 2,
    "cursor": "hand2"
}

tk.Button(sidebar, text="📍 Track My IP", command=my_location, **btn_style).pack(pady=(40, 15))
tk.Button(sidebar, text="🔍 Track Another IP", command=ip_location, **btn_style).pack(pady=10)

# Right panel (result area)
main_panel = tk.Frame(body, bg="#1a1a1a")
main_panel.pack(side="right", expand=True, fill="both", padx=20, pady=20)

tk.Label(main_panel, text="📄 Location Details", fg="white", bg="#1a1a1a",
         font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

info_text = tk.Text(main_panel, height=10, font=("Consolas", 11),
                    bg="#1f1f1f", fg="#f8f8f8", wrap="word", bd=2, relief="flat")
info_text.pack(expand=True, fill="both")
info_text.config(state="disabled")

# Footer
tk.Label(root, text="© Samreen Bibi | Rhombix Technologies", fg="#aaaaaa",
         bg="#1a1a1a", font=("Arial", 9)).pack(pady=5)

root.mainloop()
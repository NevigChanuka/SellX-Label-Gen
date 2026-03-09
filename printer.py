import os
import webbrowser

def generate_html_label(data, qty):
    # Single Label Template
    single_label = f"""
    <div class="label-container">
        <div class="header">
            <div><div class="brand">Sell-X</div><div class="sub-brand">COMPUTERS & ELECTRONICS</div></div>
            <div class="official">Official Delivery</div>
        </div>
        <div class="fragile">FRAGILE - HANDLE WITH CARE</div>
        <div class="box">
            <div class="label-title">DELIVER TO:</div>
            <div class="name">{data[0]}</div>
            <div class="address">{data[1]}</div>
            <div class="city">{data[2]}</div>
            <div class="phones"><span>📞 {data[3]}</span> &nbsp;&nbsp; <span>📱 {data[4]}</span></div>
        </div>
        <div class="footer">
            <div><strong>FROM: SELL-X GALLE</strong><br>12, Main Street, Galle.</div>
            <div style="text-align:right"><strong>ORIGIN: GALLE</strong></div>
        </div>
    </div>
    """

    # Create the repeated content based on 'qty'
    labels_html = single_label * qty

    full_html = f"""
    <html>
    <head>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&display=swap');
            @page {{ size: A4; margin: 10mm; }}
            body {{ font-family: 'Inter', Arial; margin: 0; padding: 0; background: #fff; }}
            .page {{ display: flex; flex-direction: column; gap: 30px; }}
            .label-container {{ 
                width: 170mm; border: 2px solid #000; padding: 15px; 
                position: relative; margin: 0 auto; background: white; 
            }}
            .label-container:not(:last-child)::after {{
                content: "----------------------------  CUT HERE  ----------------------------";
                position: absolute; bottom: -22px; left: 0; width: 100%; text-align: center;
                font-size: 10px; color: #aaa; font-weight: bold;
            }}
            .header {{ display: flex; justify-content: space-between; align-items: start; }}
            .brand {{ color: #e60000; font-size: 28px; font-weight: bold; margin: 0; }}
            .sub-brand {{ font-size: 9px; font-weight: bold; color: #555; }}
            .official {{ border: 1px solid #000; padding: 4px 8px; font-size: 11px; font-weight: bold; }}
            .fragile {{ background: #e60000; color: white; text-align: center; padding: 8px; margin: 10px 0; font-weight: bold; border: 3px dashed white; outline: 2px solid #e60000; }}
            .box {{ border: 1px solid #ccc; padding: 12px; border-radius: 10px; }}
            .name {{ font-size: 24px; font-weight: bold; }}
            .city {{ font-size: 20px; font-weight: 900; text-transform: uppercase; border-bottom: 3px solid black; display: inline-block; }}
            .footer {{ font-size: 9px; border-top: 1px solid #eee; margin-top: 15px; padding-top: 8px; display: flex; justify-content: space-between; }}
            @media print {{ body {{ -webkit-print-color-adjust: exact; }} }}
        </style>
    </head>
    <body>
        <div class="page">
            {labels_html}
        </div>
    </body>
    </html>
    """
    
    path = os.path.abspath("temp_label.html")
    with open(path, "w", encoding="utf-8") as f: f.write(full_html)
    webbrowser.open(f"file://{path}")